# Introduction

When we see the tittle and the description :

> FD
> Mommy! what is a file descriptor in Linux?

We know that we have to google what is a file descriptor. After searching it, a file descriptor is an integer that links to an opened file
# Testing the binary.

```bash
./fd     
pass argv[1] a number

./fd test
learn about Linux file IO
```

We need to pass an argument to execute this program correctly,  the phrase "learn about linux file IO" links to the file descriptor learning.
# C code Analysis

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char buf[32];

int main(int argc, char* argv[], char* envp[]){

	if(argc<2){
		printf("pass argv[1] a number\n");
		return 0;
	}
	
	int fd = atoi( argv[1] ) - 0x1234;
	int len = 0;
	len = read(fd, buf, 32);
	
	if(!strcmp("LETMEWIN\n", buf)){
		printf("good job :)\n");
		system("/bin/cat flag");
		exit(0);
	}
	
	printf("learn about Linux file IO\n");
	return 0;

}

```
## First condition

```c
if(argc<2){
	printf("pass argv[1] a number\n");
	return 0;
}
```

The first condition verify if we passed an argument or not, we must pass one.
## Getting file descriptor 

```c
int fd = atoi( argv[1] ) - 0x1234;
```

The function `atoi()` (ascii to integer) convert the number on a string argument to integer, if there is no number, the result will be 0

fd is equal to the result of this function minus `0x1234`.
## Put value in buf

```c
len = read(fd, buf, 32);
```

`read()` will put the content of the file target of the fd in the buf char
## The win instruction

```c
if(!strcmp("LETMEWIN\n", buf)){
	printf("good job :)\n");
	system("/bin/cat flag");
	exit(0);
}
```

To win, buf need to have the value "LETMEWIN\n"
# Exploiting

To win, we need to pass the string "LETMEWIN\n" in buf so we need an input, to do that we can invoke the stdin with the file descriptor 0 !
To get fd = 0 we simply need to put an argument that is equal to 0x1234.

```bash
./fd 0x1234
learn about Linux file IO
```

the problem is that the argument dont interprete hex value so we need to [convert](https://www.rapidtables.com/convert/number/hex-to-decimal.html?x=1234) in decimal :

![](Pasted%20image%2020240707192303.png)
## Getting the flag

```bash
./fd 4660             
LETMEWIN
good job :)
```