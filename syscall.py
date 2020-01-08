#!/usr/bin/python3

import xml.etree.ElementTree as ET
import sys
from os import path
import subprocess
import re

if len(sys.argv) < 3:
    print('Usage: syscall <arch> <syscall>')
    exit()

infos = {
    'arm64':('aarch64-linux',('x0','x1','x2','x3','x4','x5'),('svc #0','x8','x0')),
    'x64':('amd64-linux',('rdi','rsi','rdx','r10','r8','r9'),('syscall','rax','rax')),
    'arm':('arm-linux',('r0','r1','r2','r3','r4','r5'),('swi 0x0','r7','r0')),
    'x86':('i386-linux',('ebx','ecx','edx','esi','edi','ebp'),('int $0x80','eax','eax')),
    'mips32':('mips-n32-linux',('a0','a1','a2','a3','a4','a5'),('syscall','v0','v0')),
    'mips64':('mips-n64-linux',('a0','a1','a2','a3','a4','a5'),('syscall','v0','v0')),
    'ppc64':('ppc-n64-linux',('r3','r4','r5','r6','r7','r8'),('sc','r0','r3')),
    'ppc':('ppc-n-linux',('r3','r4','r5','r6','r7','r8'),('sc','r0','r3')),
    'sparc64':'sparch-n64-linux',
    'sparc':('sparc-n-linux',('o0','o1','o2','o3','o4','o5'),('t','0x10','g1','o0')),
    'sparc64':('sparc-n-linux',('o0','o1','o2','o3','o4','o5'),('t','0x6d','g1','o0'))
}

arch = sys.argv[1]
name = sys.argv[2]

filename = infos[arch][0]
order = infos[arch][1]
instruction_sys_ret = infos[arch][2]
filepath = path.join(path.dirname(path.realpath(__file__)), 'syscalls', f'{filename}.xml')

syscall = ET.parse(f'{filepath}').getroot().find(f"./syscall[@name='{name}']").attrib['number']
man = subprocess.check_output(f'man {name}', shell=True).decode()
declaration = re.search(f'{name}\\(.*\n?.*\\);', man)
if not declaration:
    man = subprocess.check_output(f'man {name}.2', shell=True).decode()
    declaration = re.search(f'{name}\\(.*\n?.*\\);', man)

print(f'For {arch}:')
print('The instruction is {}, the syscall register is {}, and the return register is {}'.format(*instruction_sys_ret))
print('The registers for the arguments are: {}'.format(', '.join(order)))
print('The syscall is {}/{}'.format(hex(int(syscall)),syscall))
print('The syscall function declaration is: \n{}'.format(declaration.group()))
