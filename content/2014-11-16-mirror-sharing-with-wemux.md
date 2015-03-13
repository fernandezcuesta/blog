Title: Mirror sharing with tmux/wemux
Published: true
Location: Santander, ES
Tags: iptables, linux, networking, agile

Fast and easy way to live sharing the screen, useful during upgrades where the
activities are to be audited real-time.

The following 2 components are in place:

- [**Wemux**](https://github.com/zolrath/wemux) and
[**tmux**](http://tmux.sourceforge.net/), where the former acts as a wrapper
for `tmux`.
- **OpenSSH** configured in such a way that guests are directly attached to an
existing `wemux` session (or disconnected otherwise).

##[**Wemux**](https://github.com/zolrath/wemux)

Assuming `tmux` is already configured and working in the system, we can just
install wemux (`wemux-git` in AUR). For the configuration we can either run
`wemux config` or edit `/etc/wemux/wemux.conf` file.

This is all I needed to change from the defaults:

```bash
host_list=(my_local_username)   # only my own user will be running in host mode
default_client_mode="mirror"    # all clients are attached read-only
```

##OpenSSH

Create a guest user and set OpenSSH up as follows:

    #!/bin/bash
    # Ensure only public key authentication is allowed
    $ sudo sed -E -i.bak 's/^#?(PasswordAuthentication|ChallengeResponseAuthentication).*$/\1 no/' /etc/ssh/sshd_config

    # Create new guest user
    $ sudo useradd -m guest
    $ echo -e 'guestpassword\nguestpassword' | sudo passwd guest

    # Create ssh key for guest
    $ su - guest
    $ mkdir .ssh
    $ ssh-keygen -N MY_PASSPHRASE -f .ssh/guest-ssh-key
    $ echo 'command="wemux",no-port-forwarding,no-x11-forwarding,no-agent-forwarding ' > .ssh/authorized_keys 
    $ cat .ssh/guest-ssh-key.pub >> .ssh/authorized_keys


Now share keys to the other party over a secure channel.

#&lt;tl;dr&gt;

Or **much easier and more secure**, if the other party has a **github** account both
steps above can be shorten by using `github-auth` with a simple command:

```bash
gh-auth add --command="wemux client mirror" --users=GITHUB_USER_ID
```

This will add the user’s keys straight to our `~/.ssh/authorized` keys and force
the connection matching the keys to attach as mirror clients to the existing
`wemux` session.

Removing the keys is even easier with:

```bash
gh-auth remove --users=GITHUB_USER_ID
```
<br/>
##<u>UPDATE:</u> When wemux is not an option

If `wemux` is not an option, we can still reach the same results only by using
`tmux` and OpenSSH.

What we need from the host is to open a tmux session with a specific name,
for example:

```bash
tmux new-session -s shared
```

On **line 13** above, replace `command="wemux"` by
`command="tmux attach-session -t session -r"` and you're done!.