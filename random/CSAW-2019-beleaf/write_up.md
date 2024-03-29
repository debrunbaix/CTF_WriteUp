# Binary Enumeration:

Using the [python tool](https://github.com/debrunbaix/Enkidu) I created for enumerating a binary, I obtained these security details:

```json
"name": "beleaf",
    "format": "ELF",
    "bit": 64,
    "linked": "dynamically linked",
    "stripped": "yes",
    "relro": "full",
    "canary": "yes",
    "nx": "yes",
    "pie": "yes",
    "rpath": "no",
    "runpath": "no",
    "symbols": "no",
    "fortify_source": "no",
    "fortified": "0",
    "fortify-able": "1",
    "printed strings": [
        "Enter the flag",
        ".note.gnu.build-id"
    ],
    "vulnerable_functions": [
        "scanf",
        "printf"
    ],
    "library": [
        "linux-vdso.so.1",
        "libc.so.6",
        "/lib64/ld-linux-x86-64.so.2"
    ]
```

# Reverse Engineering:

After renaming variables and function names from the pseudo-code extracted from Ghidra, we obtain these two functions:

## MAIN

```c
undefined8 MAIN(void)

{
  size_t USER_INPUT_LEN;
  long lVar1;
  long in_FS_OFFSET;
  ulong I;
  char USER_INPUT [136];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  printf("Enter the flag\n>>> ");
  scanf(&DAT_00100a78,USER_INPUT);
  USER_INPUT_LEN = strlen(USER_INPUT);
  if (USER_INPUT_LEN < 0x21) {
    puts("Incorrect!");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  for (I = 0; I < USER_INPUT_LEN; I = I + 1) {
    TRANSFORM_CHAR_RET = TRANSFORM_CHAR((int)USER_INPUT[I]);
    if (TRANSFORM_CHAR_RET != *(long *)(&DESIRED_OUTPUT + I * 8)) {
      puts("Incorrect!");
                    /* WARNING: Subroutine does not return */
      exit(1);
    }
  }
  puts("Correct!");
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
```

1. The program asks for user input to enter the flag, stored in `USER_INPUT`.
2. It retrieves the length of `USER_INPUT` and stores it in `USER_INPUT_LEN`.
3. First check:
   1. The program checks if the user input length is less than 33 characters (0x21).
   2. If the length is less than 33, the program stops and states it's incorrect.
   3. If the length is greater than 33, the program continues to the second check.
4. Second check:
   1. In a for loop, the program retrieves the return value in `TRANSFORM_CHAR_RET` from a function `TRANSFORM_CHAR` that takes the character `I` from `USER_INPUT` as an argument.
   2. The value of `TRANSFORM_CHAR_RET` is then compared to `DESIRED_OUTPUT`.
   4. If they differ, the program stops and states it's incorrect.
   5. If the value matches, the program continues.
5. The program outputs 'Correct'.

> `DESIRED_OUTPUT`: the characters are stored with an offset of 8 bytes hence `DESIRED_OUTPUT[I * 8]`.

DESIRED_OUTPUT:
```asm
                             DESIRED_OUTPUT

        003014e0 01              ??         01h
        003014e1 00              ??         00h
        003014e2 00              ??         00h
        003014e3 00              ??         00h
        003014e4 00              ??         00h
        003014e5 00              ??         00h
        003014e6 00              ??         00h
        003014e7 00              ??         00h
        003014e8 09              ??         09h
        003014e9 00              ??         00h
        003014ea 00              ??         00h
        003014eb 00              ??         00h
        003014ec 00              ??         00h
        003014ed 00              ??         00h
        003014ee 00              ??         00h
        003014ef

 00              ??         00h
        ...
        ...
```

We can see that the first two expected return values of the function `TRANSFORM_CHAR` are `0x1` & `0x9`.

## TRANSFORM_CHAR

```c
long TRANSFORM_CHAR(char INPUT_CHAR)

{
  long Y;
  
  Y = 0;
  while ((Y != -1 && ((int)INPUT_CHAR != *(int *)(&INDEX_CHAR + Y * 4)))) {
    if ((int)INPUT_CHAR < *(int *)(&INDEX_CHAR + Y * 4)) {
      Y = Y * 2 + 1;
    }
    else if (*(int *)(&INDEX_CHAR + Y * 4) < (int)INPUT_CHAR) {
      Y = (Y + 1) * 2;
    }
  }
  return Y;
}
```

```asm
                             INDEX_CHAR
                             
        00301020 77              ??         77h    w
        00301021 00              ??         00h
        00301022 00              ??         00h
        00301023 00              ??         00h
        00301024 66              ??         66h    f
        00301025 00              ??         00h
        00301026 00              ??         00h
        00301027 00              ??         00h
        00301028 7b              ??         7Bh    {
        00301029 00              ??         00h
        0030102a 00              ??         00h
        0030102b 00              ??         00h
        0030102c 5f              ??         5Fh    _
        0030102d 00              ??         00h
        0030102e 00              ??         00h
        0030102f 00              ??         00h
        00301030 6e              ??         6Eh    n
```

1. The function takes a character from the user input as an argument (`INPUT_CHAR`).
2. Initializes `Y` to 0.
3. As long as `Y` is different from -1 AND the decimal value of `INPUT_CHAR` is different from the decimal value of entry `Y` in `INDEX_CHAR`:
   1. The function increments `Y`.
4. The function returns the value of `Y` once the input character matches one in `INDEX_CHAR`.

# Example:

I retrieve the desired `Y` index in `DESIRED_OUTPUT` using a small Python script.

```python
FILE = 'desired_output.txt'

result = ""

with open(FILE, 'r') as file:
    addresses = file.readlines()

    for raw in addresses:
        index = raw.split()[1]
        if str(index) != '00':
            result += f" {str(index)},"

print(result)
```

```bash
python get_index.py
 01, 09, 11, 27, 02, 12, 03, 08, 12, 09, 12, 11, 01, 03, 13, 04, 03, 05, 15, 2e, 0a, 03, 0a, 12, 03, 01, 2e, 16, 2e, 0a, 12, 06,
```

We choose to start the user input with `fl`. `Y` must consecutively be equal to 1 & 9.

### F

- On the first loop iteration, `Y` equals 0, the decimal value of F (102) is compared to that of `INDEX_CHAR[0]` which is 77 (119 in decimal). The values do not match, and 102 < 119, so we add 1 to `Y`.
- On the second iteration, 102 is compared to the decimal value of `INDEX_CHAR[1]` which is 66 (102 in decimal), thus the loop is completed and `Y` is returned to `MAIN` with a value of 1.
- 1 is compared to `DESIRED_OUTPUT[0]` which is 01, so the values match and the function continues the loop.

### L

- On the first loop iteration, `Y` equals 0, the decimal value of L (108) is compared to that of `INDEX_CHAR[0]` which is 77 (119 in decimal). The values do not match, and 108 < 119, so we add 1 to `Y`.
- On the second iteration, 108 is compared to the decimal value of `INDEX_CHAR[1]` which is 66 (102 in decimal). The values do not match, and 108 > 102, so `Y` equals 4.
- On the third iteration, 108 is compared to the decimal value of `INDEX_CHAR[4]` which is 6e (110 in decimal). The values do not match, and 108 < 110, so `Y` equals 9.
- On the fourth iteration, 108 is compared to the decimal value of `INDEX_CHAR[9]` which is 6c (108 in decimal), thus the loop is completed and `Y` is returned to `MAIN` with a value of 9.
- 9 is compared to `DESIRED_OUTPUT[1]` which is 09, so the values match and the function continues the loop.

We can conclude that we have found the logic and can now find the flag.

# Obtaining the Flag

After reversing the calculation for each index in `DESIRED_OUTPUT`, we obtain the flag: `flag{we_beleaf_in_your_re_future}`.

```bash
./beleaf
Enter the flag
>>> flag{we_beleaf_in_your_re_future}
Correct!
```
