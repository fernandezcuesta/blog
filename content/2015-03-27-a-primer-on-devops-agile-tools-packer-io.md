Title: A primer on DevOps agile tools - packer.io
Date: 2015-03-27 14:06:10
tags: linux, intenet, security
status: draft

###Pros:
- Almost everything: automatization, high paralelysm, lot of customizable
elements, ...
- Debug capabilities: defining an environmental variable `PACKER_LOG`
with any value will redirect detailed log information to stderr.

###Cons (if any):
- Some elements are't too flexible. For example, with file provisioners we
cannot use wildcards, only individual files/directories can be copied to
the VMs. Not a big issue that can be circumvented in many ways.
- If a postprocess error occurs the VM is deleted and the whole process must
be repeated from scratch. A nice to have feature could be to allow a resume
operation (i.e. OS is installed, some packages were successfully installed
but scripts are missing; resuming would retry from the last stage).
- Vagrant postprocessor works copies the artifact to `/tmp` before building
the box. While in most cases this is not a problem, I got several *no space
left* errors when working on a system where `/tmp` is a ramdisk and overall
memory usage is high.
