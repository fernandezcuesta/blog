Title: Encrypted filesystem in Dropbox
Date: 27-mar-2015 18:09:11
tags: linux, internet, security
status: published

The idea is to set up a container where we can put private/secret files.
A way to achieve this is setting up **LUKS** on top of a fix-length file,
i.e. `~/Dropbox/private.img`.

##Initialization:

- Initialize a (for example) 100MB file:

        :::bash
        $ dd if=/dev/urandom of=/tmp/private.img bs=1M count=100

- Give format to the container while setting a passphrase:

        :::bash
        $ cryptsetup luksFormat /tmp/private.img
        $ sudo cryptsetup open /tmp/private.img private
        $ sudo mkfs.ext4 -L Private /dev/mapper/private

- Mount and copy files to it

        :::bash
        $ mkdir /tmp/private
        $ sudo mount /dev/mapper/private /tmp/private
        $ sudo chown -R `whoami` /tmp/priv
        $ cp ~/my_private_files/* /tmp/private

- Dismount and move the container to its final location:

        :::bash
        $ sudo umount /tmp/private
        $ sudo cryptsetup luksClose private
        $ mv /tmp/private.img ~/Dropbox/private.img

##Configuration:

For this to be shown as a device, we can do the following:

###Option 1: using `/etc/rc.local`

    #!/bin/bash
    IMG_LOCATION=/home/user/Dropbox/private.img
    case $1 in
     start)
     # start script
     losetup --find --show $IMG_LOCATION
     ;;
     stop)
     # stop script
     losetup -d `losetup | grep -Po ".+(?=(\s+\d){4}.*$IMG_LOCATION)"`
     ;;
    esac
    exit

To start this on every boot do:

    :::bash
    $ sudo chmod +x /etc/rc.local

And ensure the unit file for `rc.local` compatibility
(`/etc/systemd/system/rc-local.service`) is enabled and contains:

    :::bash
    [Unit]
    Description=/etc/rc.local Compatibility
    ConditionPathExists=/etc/rc.local

    [Service]
    Type=forking
    ExecStart=/etc/rc.local start
    ExecStop=/etc/rc.local stop
    TimeoutSec=0
    StandardOutput=tty
    RemainAfterExit=yes
    SysVStartPriority=99

    [Install]
    WantedBy=multi-user.target

###Option 2: systemd unit

Create a systemd user unit file as follows under `/etc/systemd/system`, for
example `/etc/systemd/system/mountloop.service`:

    :::bash
    [Unit]
    Description=Mount loop device
    DefaultDependencies=no
    Conflicts=umount.target
    After=local-fs.target


    [Service]
    Type=forking
    Environment="IMG_LOCATION=/home/user/Dropbox/private.img"
    ExecStart=/usr/sbin/losetup --find --show ${IMG_LOCATION}
    ExecStop=/bin/bash -c "/usr/sbin/losetup -d `losetup | grep -Po \".+(?=(\s+\d){4}.*${IMG_LOCATION})\"`"
    TimeoutSec=0
    RemainAfterExit=yes

    [Install]
    WantedBy=default.target

Then enable this unit file:

    :::bash
    $ sudo systemctl daemon-reload
    $ sudo systemctl enable mountloop
    $ sudo systemctl start mountloop

