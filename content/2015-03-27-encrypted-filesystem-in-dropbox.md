Title: Encrypted filesystem in Dropbox
Date: 27-mar-2015 18:09:11
tags: linux, internet, security
status: draft

The idea is to set up a container where we can put private/secret files.
A way to achieve this is setting up LUKS on top of a fix-length file,
i.e. `~/Dropbox/private.img`.

Steps:

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

