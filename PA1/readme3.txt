HOW IT WORKS:
-------------
This exploit uses a buffer overflow in the realpath() function in is_blocked() to 
overwrite the function return address and hijack control flow to shellcode. The 
realpath() function copies the string in its arg1 to its arg2, which makes it a 
good candidate for an overflowing write. realpath() doesn't just copy strings 
though, it also resolves paths, which has the possiblity to modify the attack 
input. Because of this, I overwrote the return address to point to where argv[2],
the malicious input, is stored in the main() stack frame. This way the shellcode and 
NOP sled were not at risk of being modified.

STEP-BY-STEP:
-------------
1. I first used GDB and objdump to view the disassembly of is_blocked(), and from this I 
figured out the offset from the block pointer (register $rbp) that canonical_pathname 
started at. This told me how many bytes I would need to write to canonical_pathname to 
get to the block pointer. 8 bytes after this would be the start of the saved return address, 
which we want to overwrite. 
2. Using the number of bytes from step one, I used GDB on BCVS, but this time with arguments 
of ./bcvs ci $(python -c 'print("A"*bytes)'). This was so I could calculate addresses 
with an argv the same size as it will be when the exploit is launched. I then found the 
actual address of argv[2] in main().
3. Next I used a C program to generate the attack string. It would have a ~250 byte NOP 
sled first, then 27 bytes of shellcode, then some filler, and finally the address I found in 
step two. I tweaked this address some so that it would be in the middle of the NOP sled. 
This was mostly done experimentally by viewing registers and addresses in GDB.
4. Finally I called BCVS with ./bcvs ci $(./a.out), where a.out is the compiled C program 
that generates the input. 
5. The address is overwritten, is_blocked() returns to my address, the NOP sled is hit, 
and then the shellcode executes and we have a root shell!

UNIQUENESS ARG:
---------------
This is my only exploit that user a buffer overflow to hijack control flow.

HOW TO PATCH:
-------------
THis can be patched by passing NULL as the second argument to realpath rather than 
canonical_pathname. This tells realpath to allocate a buffer of the appropriate size 
to hold the path, so no overflows can happen.