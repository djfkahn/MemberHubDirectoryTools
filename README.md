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
(a) - Find Missing Email
(b) - Find Orphans
(c) - Find Childless
(d) - Find Not In Classroom Hub
(e) - Make Import File for Not In Classroom Hub
(f) - Find Not in Directory
(g) - Make Import File for Not In Directory
(h) - Make Student Hub Population Import File
(i) - Find Adults/Children Hub Mismatches
Or press <enter> to quit:

ASSUMPTIONS
1.  Classroom Hub Definitions Map in file called "hub_map.csv"
Each line in this file maps one teacher name or MemberHub hub name to his/her Hub ID using 
the form:  "<teacher/hub name>|<hub id>".
2.  Known roster errors are stored in file called "roster_errata.csv"
Each line in this file maps one parents name field roster error to its corrected spelling.
3.  All input files are comma-separated text files, with one entry per line
