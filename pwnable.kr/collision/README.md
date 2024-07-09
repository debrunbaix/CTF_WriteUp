# Introduction

When we see the tittle and the description :

> Daddy told me about cool MD5 hash collision today.
> I wanna do something like that too!

This program is may be a md5 replication where we will exploit collision.
# Testing the binary.

```bash
./col                                                                
usage : ./col [passcode]

./col test                                                         
passcode length should be 20 bytes

./col testtesttesttesttest
wrong passcode.

```

We need to pass an argument with length of 20 character to execute this program correctly,  
# C code Analysis

```c
#include <stdio.h>
#include <string.h>

unsigned long hashcode = 0x21DD09EC;

unsigned long check_password(const char* p){

	int* ip = (int*)p;
	int i;
	int res=0;
	
	for(i=0; i<5; i++){
		res += ip[i];
    printf("%d\n", ip[i]);
	}
	
	printf("result is : %d\n", res);
	return res;
}

int main(int argc, char* argv[]){

	if(argc<2){
		printf("usage : %s [passcode]\n", argv[0]);
		return 0;
	}
	
	if(strlen(argv[1]) != 20){
		printf("passcode length should be 20 bytes\n");
		return 0;
	}

	if(hashcode == check_password( argv[1] )){
		system("/bin/cat flag");
		return 0;
	}
	
	else
		printf("wrong passcode.\n");
	return 0;
}
```
## Conditions

At first, we need to provide argument with 20 bytes length.
## Verification

```c
if(hashcode == check_password( argv[1] )){
	system("/bin/cat flag");
	return 0;
}
```

To get the flag we need that the result of check_password match the hashcode

With the code source, I recreate one with verbose. I print every iteration of `ip[i]` in check password to see the result

```bash
./a.out AAAAAAAAAAAAAAAAAAAA                                         
1094795585
1094795585
1094795585
1094795585
1094795585
result is : 1179010629
wrong passcode.
```

```bash
./a.out AAAABBBBCCCCDDDDEEEE
1094795585
1111638594
1128481603
1145324612
1162167621
result is : 1347440719
wrong passcode.
```

lets get the hex value of that:
```bash
>>> hex(1094795585)
'0x41414141' #AAAA
>>> hex(1111638594)
'0x42424242' #BBBB
```

so the program take group of for bytes and add them to return the result.
# Exploiting

To exploit this, we need to do little maths. the result must be `0x21DD09EC` (568134124 in decimal) so lets devide this:

```bash
>>> 568134124 / 5
113626824.8
```

...
we need to do modulation on that

```bash
>>> 568134124 % 5
4
>>> 568134124 - 113626824 * 4
113626828
```

so we need 4 times `113626824`(0x6c5cec8 in hex) and one  time `113626828`(0x6c5cecc in hex)
lets get the flag.

## Getting the flag

```bash
./a.out $(python2 -c "print '\xc8\xce\xc5\x06'*4+'\xcc\xce\xc5\x06'")
113626824
113626824
113626824
113626824
113626828
result is : 568134124
pwned
```

we get the right value !
