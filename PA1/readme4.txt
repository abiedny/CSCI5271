HOW IT WORKS:
-------------
This abuses a difference in when the input file path is checked against the 
block list and when the input file path is opened and written to. First we make 
a fake sudoers file that allows the student user root privledges, and place it 
in /opt/bcvs. Then check it in to BCVS, and then check it out. When BCVS asks
for a log entry when you check it out, wait. Note that the input path has 
already passed the is_blocked() check. In another shell, remove the fake sudoers 
file in /opt/bcvs, and replace it with a symbolic link to /etc/sudoers. Then when 
the checkout is resumed in the first shell, sudoers will be overwritten.

STEP-BY-STEP:
-------------
1. Prepare a fake sudoers file to overwrite /etc/sudoers. My fake sudoers is 
identical to the original sudoers, but with an added line 
"student ALL=(ALL) NOPASSWD: ALL" that allows full privledges to the student user
2. Check in the fake sudoers file using ./bcvs ci fake_sudoers
3. Check out the fake sudoers file using .bcvs co fake_sudoers, but wait when it 
asks to write an explanation to the log.
4. In another shell, delete /opt/bcvs/fake_sudoers, and replace it with a symbolic 
link to /etc/sudoers using ln -s /etc/sudoers sudoers_but_better.
5. Enter anything into the log in the first shell, and then resume the program. 
6. As the is_blocked() check was passed before the file was replaced with a 
symlink, BCVS will overwrite sudoers with your fake sudoers
7. student will now have root! Get a shell with sudo -s or sudo /bin/sh

UNIQUENESS ARG:
---------------
This is the only exploit that abuses a difference in the time input paths are 
checked, and the time they are used.

HOW TO PATCH:
-------------
The is_blocked() check should happen right before the src and dst files are 
opened in copyFile(). It should definitely not be called before the writeLog 
function that will stall the program waiting for user input.