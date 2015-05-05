# MemberHubDirectoryTools
Tools for checking certain qualities of MemberHub directory dumps, and for creating import files that assign classroom hubs 
and new members.

HOW TO USE
>> python menu.py
Enter name of directory dump file:  <directory dump file name>.csv
#### lines read and processed from directory file
Enter name of roster file: <roster file name>.csv
#### students processed, with #### adults.
#### hub IDs read and processed.
Choose:
(1) - Find Missing Email
(2) - Find Orphans
(3) - Find Childless
(4) - Find Not In Hub
(5) - Make Import File for Not In Hub
(6) - Find Not in Directory
(7) - Make Import File for Not In Directory
Or press <enter> to quit:

ASSUMPTIONS
1.  Classroom Hub Definitions Map in file called "hub_map.csv"
Each line in this file maps one teacher name to his/her Hub ID.

2.  All input files are comma-separated text files, with one entry per line
