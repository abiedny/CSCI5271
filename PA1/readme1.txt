HOW IT WORKS:
-------------
This exploit takes advantage of the path checking used by the is_blocked() 
function. The original block.list file contains an entry /opt/bcvs/.bcvs/block.list 
that is meant to prevent the block list from being overwritten. But if a file named
block.list is passed in from the /opt/bcvs directory, the realpath() function will 
resolve it to /opt/bcvs/block.list, which would fail a comparision with the entry in 
the original blocklist. This shows an inconsistency between the designer's expectations 
and the actual program behavior, and can be exploited to overwrite the blocklist, and 
then use the root privledges of the program to overwrite /etc/sudoers to one that allows 
student root access.

STEP-BY-STEP:
-------------
1. Move to the /opt/bcvs directory and create an empty file named block.list
2. Use BCVS to check the file in, overwriting the original block.list by calling 
./bcvs ci block.list
3. Prepare a fake sudoers file to overwrite /etc/sudoers. My fake sudoers is 
identical to the original sudoers, but with an added line 
"student ALL=(ALL) NOPASSWD: ALL" that allows full privledges to the student user
4. Check in the fake sudoers file using ./bcvs ci fake_sudoers
5. Delete the fake sudoers file in /opt/bcvs, and then create a symbolic link to
the real sudoers using ln -s /etc/sudoers fake_sudoers. It should be named the same
as the fake sudoers file.
6. Check the fake sudoers out using ./bcvs co fake_sudoers, and then student will 
have root access! Call sudo -s or sudo /bin/sh or similar to get a root shell

UNIQUENESS ARG:
---------------
While many of my exploits overwrite or modify the sudoers file, this is the only one that 
abuses the path checking bug in is_blocked() to overwrite the blocklist. If this bug was 
patched out so that the blocklist functioned as the designers intended, no other exploits would 
be patched out.

HOW TO PATCH:
-------------
This would be simple to patch out, just strip out everything before the file name of the 
passed in path (probably using something like strtok(path, "/")) and construct the 
destination path ("/opt/bcvs/.bcvs/filename"), and use that to compare to the blocklist entries.