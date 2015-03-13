Title: Logical disks in OpenVMS
Published: true
Location: Santander, ES
Tags: OpenVMS

There are situations where an operator wants to run some custom scripts on
their systems. These scripts might not be fully optimized and be the root
cause for bigger problems in the overall system behaviour.
It is also quite common to be asked for a way to *'restrict'* the amount of
log or output files that a script can generate, in a way that the main
services running on the system are not affected by a lack of space.

A way to manage this is by controlling the number of log or output files to
be written to a specific directory.
This can be done with the `SET DIRECTORY /VERSION_LIMIT` or even for
individual files with `SET FILE /VERSION_LIMIT` commands.

Another way to accomplish it is by defining a **Logical Disk (LD)**.


<u>**LDdriver**</u> allows OpenVMS to create a logical volume that physically
resides on a single file. Similar to loop devices on Linux.
The size of the virtual volume can be as big as the real volume where the file
is saved can store.

A couple of use cases:

- Burn a CD with an OpenVMS directory structure. Create a LD, mount it,
copy directories to virtual volume and disconnect.
The container file can now be burnt to a CD.

- Shrink a script not to fill up a disk. Assign the working directory to a LD
with a specific size. Even if the virtual volume is 100% full, the real disk
will not be affected (think about a 8GB virtual disk residing on a 100GB
volume).

        :::text
        > ld help
        
         LD
        
        
         The logical disk utility is a system management tool available to any user for controlling logical disk usage.
         A Logical Disk is a file available on a Physical Disk, which acts as a real Physical Disk (the file may or may not be contiguous).
         The Logical Disks are available in any directory of the Physical Disk.
         A large disk can be divided into smaller sections, each a Logical Disk, supporting the same I/O functions as the Physical Disk.
         By giving the Logical Disk File a good protection level and mounting it private or with device protection, you are able to add a number of protection
         levels to your file system.
         The logical disk is controlled by the LD utility, which can be directly invoked from DCL.
        
        Format:
        
        LD [/qualifiers] [Filespec] [Device]
        
        Additional information available:
        
        Author Command_summary Driver_functions Error_messages
        Features HELP New_features_V5.0 New_features_V5.1
        New_features_V6.0 New_features_V6.2 New_features_V6.3
        New_features_V7.0 New_features_V8.0 New_features_V8.1
        New_features_V8.2 Parameters Privileges_and_Quotas Restrictions
        Setup IO_Trace_example CONNECT CREATE DISCONNECT NOPROTECT
        NOWATCH SHOW TRACE NOTRACE PROTECT WATCH VERSION


##Example

* Add the startup procedures to the `SYS$STARTUP:SYSTARTUP_VMS.COM`

        :::DCL
        $ If f$search("sys$startup:ld$startup.com") .nes. Then @SYS$STARTUP:LD$STARTUP
>Note that this will be executed during system boot. If a reboot is not
possible, invoke it manually from the system prompt with
`@SYS$STARTUP:LD$STARTUP`, then continue with the next steps

* Create a 100MBlock (40MB) logical drive file

        :::DCL
        > ld create $1$dga200:[repository]ldisk1.dsk /size=100000 /nobackup [/contiguous]

* Connect

        :::DCL
        > ld connect $1$dga200:[repository]ldisk1.dsk [lda1:] [/share]
        %LD-I-UNIT, Allocated device is $1$LDA1:

        > ld show lda1:
        %LD-I-CONNECTED, Connected $1$LDA1: to $1$dga200:[repository]ldisk1.dsk;1

* Initialize the logical drive with `/erase` parameter in order to erase any
potentially sensitive data on the underlying disk device.

        :::DCL
        > initialize /erase lda1: ldisk1_label
        > mount /over=id lda1:
        > show dev lda1

        Device Device Error Volume Free Trans Mnt
        Name Status Count Label Blocks Count Cnt
        $1$LDA1: (MIKO) Mounted alloc 0 LDISK1 99900 1 1


        > dismount lda1:
        > ld disconnect lda1: /log

* Set the logical disk to mount automatically during startup

    As previously done for the LD driver startup, we can add the commands for
    connecting and mounting the logical disks, provided that they were
    successfully created.

    This is an example of all the lines added to the end of
    `SYS$STARTUP:SYSTARTUP_VMS.COM`:

        #!DCL
        $!
        $ If f$search("sys$startup:ld$startup.com") .nes. Then @SYS$STARTUP:LD$STARTUP
        $!
        $! Optional: for Logical Magnetic tapes (LM)
        $! If f$search("sys$startup:lm$startup.com") .nes. ""
        $! Then
        $! @SYS$STARTUP:LM$STARTUP
        $! Endif
        $!
        $ If f$search("dsa4:[000000]SCRIPT_LD.DSK") .nes. ""
        $ Then
        $ ld connect dsa4:[000000]SCRIPT_LD.DSK lda1: /share
        $ mount $1$lda1: SCRIPT_LD /system /cluster
        $ Endif
        $!
        $ If f$search("dsa4:[000000]T4$DATA.DSK") .nes. ""
        $ Then
        $ ld connect dsa4:[000000]T4$DATA.DSK lda2: /share
        $ mount $1$lda2: T4$DATA /system /cluster
        $ Endif
        $!
 
