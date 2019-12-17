# syscall\_info

This is a script I created originally while working on shellcode writing to get instant info about syscalls from name and about the target architecture such as registers used and required instruction. The xml files are originally in `/usr/share/gdb/syscalls`, but I've included them in the repo anyway, just in case.

It supports:
+ x86
+ x64
+ arm
+ arm64
+ mips
+ powerpc
+ powerpc64
+ sparc
+ sparc64

# TO DO

+ Add info about syscall function C declaration, arguments and return value
