# Enumerating the Binary:

From the Python tool I've made to enumerate a binary, I get these security insights:

```json
"name": "rev",
    "format": "ELF",
    "bit": 64,
    "linked": "dynamically linked",
    "stripped": "no",
    "relro": "full",
    "canary": "yes",
    "nx": "yes",
    "pie": "yes",
    "rpath": "no",
    "runpath": "no",
    "symbols": "yes",
    "fortify_source": "no",
    "fortified": "0",
    "fortify-able": "0",
    "printed strings": [
        "validate",
        ".note.gnu.build-id"
    ],
    "vulnerable_functions": [
        "scanf"
    ],
    "library": [
        "linux-vdso.so.1",
        "libc.so.6",
        "/lib64/ld-linux-x86-64.so.2"
    ]
```

> So, it's a 64-bit ELF binary.

Then, in the assembler extracted from my script, I see a series of comparisons to a "string":

```asm
0x1205:	mov	dword ptr [rbp - 0x40], 0x66
0x120c:	mov	dword ptr [rbp - 0x3c], 0x6c
0x1213:	mov	dword ptr [rbp - 0x38], 0x61
0x121a:	mov	dword ptr [rbp - 0x34], 0x67
0x1221:	mov	dword ptr [rbp - 0x30], 0x7b
0x1228:	mov	dword ptr [rbp - 0x2c], 0x48
0x122f:	mov	dword ptr [rbp - 0x28], 0x75
0x1236:	mov	dword ptr [rbp - 0x24], 0x43
0x123d:	mov	dword ptr [rbp - 0x20], 0x66
0x1244:	mov	dword ptr [rbp - 0x1c], 0x5f
0x124b:	mov	dword ptr [rbp - 0x18], 0x6c
0x1252:	mov	dword ptr [rbp - 0x14], 0x41
0x1259:	mov	dword ptr [rbp - 0x10], 0x62
0x1260:	mov	dword ptr [rbp - 0xc], 0x7d
```

# Running the Binary:

Upon running the binary and testing, the output is:

```
Welcome to the Salty Spitoon™, How tough are ya?
test
Yeah right. Back to Weenie Hut Jr™ with ya
```

# Finding the Flag

By assembling the char translation of the comparisons made in the assembler code, we have the string "flag{HuCf_lAb}"

```bash
./rev
Welcome to the Salty Spitoon™, How tough are ya?
flag{HuCf_lAb}
Right this way...
```
