Title: Bypassing DNS assigned by VPN
Published: True
Location: Santander, ES
Googlewebfonts: "Bree+Serif"
Tags: iptables, networking, security, linux
Categories: 

With some VPN clients like Cisco Anyconnect, the DNS records can be
automatically assigned by the VPN server during negotiation of the secure
connection.

This shouldn't be a problem if we have access to `/etc/resolv.conf` file. For
example enabling the immutable flag (`chattr +i /etc/resolv.conf`) before
connecting or doing a backup&restore of such file.

However Anyconnect client temporarily modifies this file during initialization
*and* monitors it, so changes are not possible without dropping the connection.

Fast an easy way to do this with iptables: redirect all DNS queries (on port
53) to our preferred or local DNS server.
For example:

```bash
iptables -t nat -A OUTPUT -p udp --dport 53 -j DNAT --to 8.8.8.8:53
iptables -t nat -A OUTPUT -p tcp --dport 53 -j DNAT --to 8.8.8.8:53
```

Now, all DNS queries will be redirected to our preferred DNS, regardless of
what's imposed by Cisco client on our `/etc/resolv.conf` file.
