HOW IT WORKS:
-------------
This exploit targets the lack of directory enforcement on where BCVS is ran. By creating 
a fake directory structure and blocklist, we have full control over the .bcvs directory, 
which is normally protected. This is used to create a symbolic link to /etc/sudoers in 
the .bcvs/ directory which is named with a .comments extension so that the writeLog() 
function will write to it. This is used to append the sudoers file with a line giving 
the student user full access.

STEP-BY-STEP:
-------------
1. Create a directory named .bcvs. Inside that directory, create an empty file named 
block.list, and a symbolic link to /etc/sudoers that ends in .comments, using a command 
like ln -s /etc/sudoers anything.txt.comments
2. Change directories to .bcvs/..
3. Run BCVS using its absolute path /opt/bcvs/bcvs ci anything.txt
4. BCVS will then open the logfile for anything.txt, which we have replaced with a 
symbolic link to /etc/sudoers. It will open sudoers to append to it.
5. When you are prompted to write an explanation, enter "student ALL=(ALL) NOPASSWD: ALL\n"
6. This line is appended to sudoers, and student will have root access! Get a root shell 
with sudo -s or sudo /bin/sh

UNIQUENESS ARG:
---------------
While this exploit is similar to sploit1, they target different vulnerabilities. Sploit1 
uses a bug in is_blocked() to overwrite the blocklist and then replace sudoers, while this
sploit2 uses the lack of directory enforcement to create a fake directory structure and 
blocklist for BCVS, and then append to sudoers with the writeLog() function.

HOW TO PATCH:
-------------
To fix this vulnerability, you could add a line near the begining of main() that makes 
sure BCVS is running from /opt/bcvs, otherwise exit.