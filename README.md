# MemberHubDirectoryTools
Tools for checking certain qualities of MemberHub directory dumps, and for creating import files that assign classroom hubs and new members.

(_note:  This tool has been upgraded to Python 3.8.0 compatibility, and is no longer compatible with Python 2.x.  Since Python 2.x will deprecate on 1/1/2020, there are no plans to make it backward compatible._)

---
## HOW TO USE
`% python3 menu.py` <br>
`Enter name of hub map file (press <enter> to use "hub_map.csv"): ` <br>
`Enter name of directory dump file (press <enter> to use "dump.csv"): ` <br>
`Read #### lines, processed #### lines, and created ### families from directory file` <br>
`Enter name of roster comma-separated text file (press <enter> to use "roster.csv"): ` <br>
`Print corrected roster errors to the screen? (press <enter> for "no", press "y" for "yes"): ` <br>
`### students processed ### families.` <br>
`Choose:` <br>
`(a) - Find Missing Email` <br>
`(b) - Find Orphans` <br>
`(c) - Find Childless` <br>
`(d) - Find Not In Classroom Hub` <br>
`(e) - Find Adults without Accounts` <br>
`(f) - Find Not in Directory` <br>
`(g) - Make Import File for Not In Directory` <br>
`(h) - Make Student Hub Population Import File` <br>
`(i) - Find Adults/Children Hub Mismatches` <br>
`(j) - Find Unused Errata` <br>
`Or press <enter> to quit:` <br>

---
## ASSUMPTIONS
1.  Classroom Hub Definitions Map in file called "hub_map.csv"
Each line in this file maps one teacher name or MemberHub hub name to his/her Hub ID using 
the form:  "<teacher/hub name>|<hub id>".
2.  Known roster errors are stored in file called "roster_errata.csv"
Each line in this file maps one parents name field roster error to its corrected spelling.
3.  All input files are comma-separated text files, with one entry per line
