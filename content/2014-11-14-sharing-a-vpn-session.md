Title: Sharing a VPN session

Location: Santander, ES
Tags: iptables, linux, networking, security

Sometimes it may happen that we need to share the connection to a remote system
with another person who cannot connect directly.
In order to move on, there are quite a few options. Amongst others:

- Using a shared tmux session while the connection is established, which
requires the other person to feel comfortable with tmux.
- Setting up a VPN to my system.
- Setting up an <u>**SSH tunnel**</u> listening in our outbound interface.
- Setting up *a couple* of <u>**iptables**</u> rules.

On this article I'll describe **last two options**.

For completeness, let's summarize the components in the game:

- VPN session is established from my laptop, which has a private IP address
behind a NAT (actually behind 2 NATs, which is not relevant).
- Broadband router has a dynamically assigned public IP provided by my ISP.
- There already exist a port range forwarded from the router straight to my
laptop both for UDP and TCP.

So at the end, the details (as an example) are:

- My public IP: 1.1.1.1
- Open port to my system: 50000
- Assigned IP address from the VPN tunnel: 10.200.100.5
- Remote system reachable from the IPSec tunnel: 10.200.0.1

The <u>**simplest option**</u> is taking advantage of OpenSSH's ability to forward
incoming connections into the SSH tunnel:

```bash
$ ssh user@10.200.0.1 -L 1.1.1.1:50000:localhost:22
```

And let the other person connect to 1.1.1.1:50000.
This works great **as long as we keep our SSH session open**.

An alternative using `iptables` does not have this constrain.

Having a look at iptables flowchart, we may figure out what we need to set it
up by following the upper side of the
[chart](http://www.fclose.com/816/port-forwarding-using-iptables/).

    #!text
    PACKET IN
        |
    PREROUTING--[routing]-->--FORWARD-->--POSTROUTING-->--OUT
     - nat (dst)   |           - filter      - nat (src)
                   |                            |
                   |                            |
                  INPUT                       OUTPUT
                  - filter                    - nat (dst)
                   |                          - filter
                   |                            |
                   `----->-----[app]----->------'


- PREROUTING rule on NAT table to translate incoming connections on port 50000
to the remote system port 22 (SSH).

        :::bash
        $ iptables -t nat -A PREROUTING -p tcp --dport 50000 -j DNAT --to \
        > 10.200.0.1:22 -m comment --comment 'Redirect in 50000 to 10.200.0.1:22'

- FORWARD rule to allow this traffic flow between interfaces (eth0 and tun0).

        :::bash
        $ iptables -I FORWARD -p tcp --dst 10.200.0.1 --dport 22 -j ACCEPT
        $ iptables -I FORWARD -p tcp --src 10.200.0.1 --sport 22 -j ACCEPT

    This also needs the kernel to allow IP forwarding, so we must check:

        :::bash
        $ if [ $(cat /proc/sys/net/ipv4/ip_forward) = 0 ]; then \
        > sudo sysctl -w net.ipv4.ip_forward=1 ;fi

- POSTROUTING rule on NAT table to masquerade the source address of outgoing
traffic.

        :::bash
        $ iptables -t nat -A POSTROUTING -d 10.200.0.1 -p tcp --dport 22 \
        > -j SNAT --to-source 10.200.100.5

With these rules in place the other person can simply access the remote system
with:

```bash
$ ssh username@1.1.1.1 -p 50000
```
The overall process can be automated with a bash script like this:

    #!/bin/bash
    
    GW_PORT=22            # default gateway port
    GW_IP=127.0.0.1       # default gateway ip address
    FWD_PORT=8000         # default forwarding port, must be reachable from remote
    COMMENT="Added by vpn_fwd"   # comment added to iptables rules
    
    disable=false   # unless specified, default action is to enable the forwarding
    
    usage() {
    read -d '' help <<- EOF
      Usage: vpn_fwd  gw-ip   gateway ip (defaults to $GW_IP)
                     [--gw-port]   gateway port (defaults to $GW_PORT)
                     [--fwd-port]   forwarding port (defaults to $FWD_PORT)
                     [--iface]   VPN interface name (default, first PPP interface
                                                     found)
    
             vpn_fwd disable    disable port forwarding to VPN
    
      Example:
             vpn_fwd 10.10.10.1  # redirects port 8000 to 10.10.10.1:22
             vpn_fwd my_gw_host --fwd-port 44000 --iface tun2
    EOF
    echo "$help"
    }
    
    guess_ip(){
    # Look for the VPN assigned IP address (first PPP interface if nothing given)
    if [ -z "$VPN_IF" ]; then
       VPN_IF=$(ifconfig | grep -Pom1 '.*(?=:\sflags=\d+<[\w,]*POINTOPOINT)')
    fi
    if [ "$VPN_IF" ]; then
       ifconfig $VPN_IF | grep -Po \
       '\s*inet\s+\K\b(?:\d{1,3}\.){3}\d{1,3}\b(?=\s+netmask.*)'
    fi
    }
    
    
    
    enable_fwd() {
    # Enable IP forwarding if not already
    if [ $(cat /proc/sys/net/ipv4/ip_forward) = 0 ] ; then
      sudo sysctl -w net.ipv4.ip_forward=1
    fi
    
    if [ "$GW_IP" == "127.0.0.1" ]; then
        VPN_IP=$GW_IP
    else
        VPN_IP=$(guess_ip)
    fi
    
    if [ "$VPN_IP" ]; then
        # Set up iptables rules
        sudo iptables -t nat -A PREROUTING -p tcp --dport $FWD_PORT -j DNAT --to \
        $GW_IP:$GW_PORT -m comment --comment "${COMMENT}"
        sudo iptables -I FORWARD -p tcp --dst $GW_IP --dport $GW_PORT -j ACCEPT \
        -m comment --comment "${COMMENT}"
        sudo iptables -I FORWARD -p tcp --src $GW_IP --sport $GW_PORT -j ACCEPT \
        -m comment --comment "${COMMENT}"
        sudo iptables -t nat -A POSTROUTING -d $GW_IP -p tcp --dport $GW_PORT \
        -j SNAT --to-source $VPN_IP -m comment --comment "${COMMENT}"
    else
        ifconfig -a
        echo 'No POINTOPOINT interface was found up...'
    fi
    }
    
    disable_fwd() {
    # Delete all iptables rules with $COMMENT
    sudo sh -c 'iptables-save | grep -v "${COMMENT}" | iptables-restore'
    echo 'Forwarding disabled'
    sudo iptables-save | grep "${COMMENT}"
    }
    
    main() {
        if [[ ${1} == "disable" ]]; then
           disable=true
           return 1
        else
           GW_IP=$(dig +short ${1})  #mandatory as first argument
           shift
        fi
        while [[ ${1} ]]; do
            case "${1}" in
                --gw-port)
                    GW_PORT=${2}
                    shift
                    ;;
                --fwd-port)
                    FWD_PORT=${2}
                    shift
                    ;;
                --iface)
                    VPN_IF=${2}
                    shift
                    ;;
                *)
                    echo "Unknown parameter: ${1}" >&2
                    usage
                    return 1
            esac
    
            if ! shift; then
                echo 'Missing parameter argument.' >&2
                usage
                return 1
            fi
        done
    }
    
    if [ -z "$1" ]; then
        usage
    else
        main "${@}"
        if $disable; then disable_fwd; else enable_fwd; fi
    fi
