#!/usr/bin/python3

import xml.etree.ElementTree as ET
import sys
from os import path
import subprocess
import re
import argparse

ARCHITECTURES = {
    'arm64':('aarch64-linux',('x0','x1','x2','x3','x4','x5'),('svc #0','x8','x0')),
    'x64':('amd64-linux',('rdi','rsi','rdx','r10','r8','r9'),('syscall','rax','rax')),
    'arm':('arm-linux',('r0','r1','r2','r3','r4','r5'),('swi 0x0','r7','r0')),
    'x86':('i386-linux',('ebx','ecx','edx','esi','edi','ebp'),('int $0x80','eax','eax')),
    'mips32':('mips-n32-linux',('a0','a1','a2','a3','a4','a5'),('syscall','v0','v0')),
    'mips64':('mips-n64-linux',('a0','a1','a2','a3','a4','a5'),('syscall','v0','v0')),
    'ppc64':('ppc-n64-linux',('r3','r4','r5','r6','r7','r8'),('sc','r0','r3')),
    'ppc':('ppc-n-linux',('r3','r4','r5','r6','r7','r8'),('sc','r0','r3')),
    'sparc':('sparc-linux',('o0','o1','o2','o3','o4','o5'),('t','0x10','g1','o0')),
    'sparc64':('sparc64-linux',('o0','o1','o2','o3','o4','o5'),('t','0x6d','g1','o0'))
}

parser = argparse.ArgumentParser(description='Lookup syscall information.')
parser.add_argument('arch', help='The target architecture', choices=ARCHITECTURES.keys())
parser.add_argument('syscall', help='The syscall name/number to look up')
args = parser.parse_args()
arch, syscall = args.arch, args.syscall

filename, order, instruction_sys_ret = ARCHITECTURES[arch]
filepath = path.join(path.dirname(path.realpath(__file__)), 'syscalls', f'{filename}.xml')

try:
    # If the argument is a number, use it to get the name
    syscall_number = int(syscall)
    syscall_name = ET.parse(f'{filepath}').getroot().find(f"./syscall[@number='{syscall_number}']").attrib['name']
except:
    # If the argument is a name, use it to get the number
    syscall_number = int(ET.parse(f'{filepath}').getroot().find(f"./syscall[@name='{syscall}']").attrib['number'])
    syscall_name = syscall

man = subprocess.check_output(f'man {syscall_name}', shell=True).decode()
declaration = re.search(f'{syscall_name}\\(.*\n?.*\\);', man)
if not declaration:
    man = subprocess.check_output(f'man {syscall_name}.2', shell=True).decode()
    declaration = re.search(f'{syscall_name}\\(.*\n?.*\\);', man)

print(f'For {arch}:')
print('The instruction is {}, the syscall register is {}, and the return register is {}'.format(*instruction_sys_ret))
print('The registers for the arguments are: {}'.format(', '.join(order)))
print('The syscall is %#x/%d' % (syscall_number, syscall_number))
print('The syscall function declaration is: \n{}'.format(declaration.group()))
