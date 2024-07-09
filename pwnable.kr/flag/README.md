# Introduction

> This is reversing task. all you need is binary

It is just a reverse challenge 
# testing the binary

```bash
./flag     
I will malloc() and strcpy the flag there. take it.
```
# Analyse

## Strings

The output of `strings` command is strange but with this line we understand why :

```bash
strings flag | grep upx
$Info: This file is packed with the UPX executable packer http://upx.sf.net $
```
## Unpack the binary

I had to install UPX and then verify if `flag` was packed with it.

```bash
upx -t flag
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2024
UPX 4.2.2       Markus Oberhumer, Laszlo Molnar & John Reiser    Jan 3rd 2024

testing flag [OK]

Tested 1 file.
```

Know we just have to unpack it with `-d`

```bash
upx -d flag
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2024
UPX 4.2.2       Markus Oberhumer, Laszlo Molnar & John Reiser    Jan 3rd 2024

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
    887219 <-    335288   37.79%   linux/amd64   flag

Unpacked 1 file.
```
## Find flag

after opening Ghidra and analyse ALL function (it was long), i find main function here :

![](Pasted%20image%2020240709195144.png)

```c
undefined8 main(void)

{
  char *__dest;
  
  puts("I will malloc() and strcpy the flag there. take it.");
  __dest = (char *)malloc(100);
  strcpy(__dest,flag);
  return 0;
}
```

I just follow the road where `flag` goas and found the flag !

![](Pasted%20image%2020240709195303.png)
