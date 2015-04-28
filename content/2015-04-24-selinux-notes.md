Title: Keep calm and setenforce 1 - SELinux notes
Date: 2015-04-24 11:47:27
status: published
tags: linux, security

##GUI tool for SELinux:  **`system-config-selinux`**


- Files, folders, devices  → SELinux objects
- Processes                → SELinux subjects    →    Both mapped in SELinux contexts

Processes are confined in their contexts.
Contexts define which files a process can access and which other processes can
interact with.


##Configuration file: **`/etc/sysconfig/selinux`**

    :::bash
    # This file controls the state of SELinux on the system.
    # SELINUX= can take one of these three values:
    #   enforcing - SELinux security policy is enforced.
    #   permissive - SELinux prints warnings instead of enforcing.
    #   disabled - SELinux is fully disabled.
    SELINUX=enforcing
    # SELINUXTYPE= type of policy in use. Possible values are:
    #   targeted - Only targeted network daemons are protected.
    #   strict - Full SELinux protection.
    SELINUXTYPE=targeted


* Check current mode:

        :::console
        # sestatus
    
        SELinux status:                 enabled
        SELinuxfs mount:                /selinux
        Current mode:                   permissive
        Mode from config file:          permissive
        Policy version:                 24
        Policy from config file:        targeted
      
        # getenforce
        Enforcing

*  Change the current mode:
 
        :::console
        # setenforce [ Enforcing | Permissive | 1 | 0 ]

                                                                                                                                                                                                                    
##USERS

Linux users are mapped into SELinux users (by default Linux users are
unconfined). To show the mapping, run:

    :::console
    # semanage login -l
    Login Name           SELinux User         MLS/MCS Range        Service
    
    __default__          unconfined_u         s0-s0:c0.c1023       *
    root                 unconfined_u         s0-s0:c0.c1023       *
    system_u             system_u             s0-s0:c0.c1023       *
    

* Show SELinux confined users parameters:

        :::console
        # semanage user -l

* Set SELinux rules for a specific user:

        :::console
        # semanage login -s user_u -a one_user
  
*  Set confined user as default for every new added accounts:

        :::console
        # semanage login -m -S targeted -s "user_u" -r s0 __default__

                                                                                                                                                                                                                    
##BOOLEANS


- Show list of booleans with current and default status and short description:

        :::console
        # semanage boolean -l

        #  # Only list of booleans with current status
        # getsebool -a 

- Modify a SELinux boolean:
For example, in order to enable samba shares (`-P` for permanent):

        :::console
        # setsebool -P allow_smbd_anon_write on
        or
        # semanage boolean -m --on allow_smbd_anon_write
                                                                                                                                                                                                            

##CONTEXTS

- SELinux contexts for processes:

        :::console
        # ps -eZfx

- SELinux contexts for users:

        :::console
        # id -Z

- SELinux contexts for files:

        :::console
        # ls -lZ


###Change SELinux file contexts

- <u>Temporary changes</u>: **`chcon`**

        :::console
        # chcon --reference /var/ftp /ftp
        # chcon -R -u system_u -t public_content_rw_t /ftp      
<u>*Where, as an example:*</u>
`public_content_rw_t` allows uploads to an FTP folder

- <u>Permanent changes</u>: **`semanage fcontext`**

        :::console
        # #Adds a new record to the file contexts, but does not apply changes
        # semanage fcontext -a -t public_content_rw_t "/ftp(/.*)?"
        # #Restore contexts according to records, thus applying changes
        # restorecon -Rv /ftp
        # ls -ldZ /ftp

- Unconfined processes:

        :::console
        # ls -Z /usr/sbin/httpd
        -rwxr-xr-x  root root system_u:object_r:httpd_exec_t:s0 /usr/sbin/httpd
        # chcon -t bin_t /usr/sbin/httpd
        # ls -Z /usr/sbin/httpd
        -rwxr-xr-x. root root system_u:object_r:bin_t:s0       /usr/sbin/httpd

###Show all available SELinux contexts

    :::console
    # seinfo -t
    # seinfo -t | grep '^\s*ftp'


###Restore SELinux contexts

- Show default file contexts:

        :::console
        # semanage fcontext -l
        # restorecon -v -F -R /home/user/ftp
default file contexts are defined in `/etc/selinux/contexts/files/file_contexts`

- Only show default SELinux context for a specific folder/file

        :::console
        # matchpathcon /var/www/html


##FILES

###Mount filesystem with specific context

    :::console
    # mount -o context="system_u:object_r:httpd_sys_content_t:s0" server:/export /var/www/html/content

<u>*Options:*</u>

- `-o context`:    usually for removable media from non-SELinux systems (i.e. a FAT32 USB drive)
- `-o fscontext`:  set or override the filesystem object instance security context (i.e. set ext3 filesystem security)
- `-o defcontext`: set or override the default file security context (instead of default_t)

If the same directory of an export has to be mounted with diferent contexts,
use `-o nosharecache` option.


###Archiving files with extended attributes

    :::console
    # tar --selinux

If extracting a tar file ***without*** extended attribute information, do:

    :::console
    # tar -zxvf archive.tar.gz | restorecon -f -

##OTHER

###Copy files while preserving the context information
    :::console
    $ cp --preserve=context source_file destination_file

###Add a custom port for a service
    :::console
    # semanage port -a -t http_port_t -p 10443

###Mounting filesystems with specific SELinux contexts
    :::console
    # mount server:/export /local/mount/point -o context="system_u:object_r:httpd_sys_content_t:s0"
    
    or in /etc/fstab
    
    #server:/export /local/mount/ nfs context="system_u:object_r:httpd_sys_content_t:s0" 0 0

##TROUBLESHOOT

    :::console
    #  # Search 'qemu' related SELinux violations
    # ausearch -m avc -c qemu
    #  # Automatically generate a policy
    # ausearch -m avc -c qemu | audit2allow -M mypol
    # sealert  -a /var/log/audit/audit.log  # (TUI)
    # sealert  # (GUI)


###Troubleshoot a specific problem

- Reproduce the problem while watching the logs:

        :::console
        # tail -f /var/log/audit/audit.log | audit2why

        or

        # tail -f /var/log/audit/audit.log | audit2allow -a

    In addition, as explained in
[certdepot](http://www.certdepot.net/selinux-diagnose-policy-violations/),
we can filter on the AVC as follows:

        :::console
        # tailf /var/log/audit/audit.log
        ...
        type=AVC msg=audit(1415714880.156:29): avc:  denied  { name_connect } for  pid=1349 \
          comm="nginx" dest=8080 scontext=unconfined_u:system_r:httpd_t:s0 \
          tcontext=system_u:object_r:http_cache_port_t:s0 tclass=tcp_socket
        
        # grep 1415714880.156:29 /var/log/audit/audit.log | audit2why

- If an output like this one is shown:

        :::text
        #============= httpd_sys_script_t ==============
        allow httpd_sys_script_t self:capability { setuid setgid };
        allow httpd_sys_script_t self:process setrlimit;

    proceed with flag `-M`:
        
        :::console
        # tailf /var/log/audit/audit.log | audit2allow -a -M my_semanage_file

- And fix with:

        :::console
        # semodule -i my_semanage_file.pp

This process may be repeated several times to fully troubleshoot the problem.


If the `setroubleshoot-server` is installed, some errors may appear directly
in the journal or in `/var/log/messages` like:

    SELinux is preventing [...] run sealert -l 21d07129-dd4f-4ac7-9579-fd17e89f53ee



##References

- [RHEL7 SELinux user's and Administrator's Guide](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/SELinux_Users_and_Administrators_Guide/index.html)
- [Certdepot](http://www.certdepot.net/selinux-diagnose-policy-violations/)
