#!/usr/bin/env python
"""This module contains the tools to injest a MemberHub directory dump into
a dictionary, and display portions of the dictionary for analysis.
"""

def ReadDirectory():
    """directory_tools.ReadDirectory
    INPUTS:
    Prompts user for name of comma-separated text file containing MemberHub directory dump.
    OUTPUTS:
    Dictionary keyed by file line number with values that are dictionaries with the following keys:
        This function assumes the directory dump fields are in this order:
        1.  "person_id"
        2.  "last_name"
        3.  "first_name"
        4.  "middle_name"
        5.  "suffix"
        6.  "email"
        7.  "family_id"
        8.  "family_relation"
        9.  "maiden_name"
        10. "born_on"
        11. "gender"
        12. "parents"
        13. "street"
        14. "city"
        15. "state"
        16. "zip"
        17. "home_number"
        18. "work_number"
        19. "work_number_ext"
        20. "fax_number"
        21. "mobile_number":
        22. "mobile_provider"
        23. "allow_sms"
        24. "hubs"
        25. "hubs_administered"
        26. "person_created"
        27. "person_updated"
        28. "account_created"
        29. "account_updated"
        30. "last_login"
    ASSUMPTIONS:
    1. Each line should contain exactly 30 fields that are separated by just a comma (','),
    and none of the fields contain commas.
    2. Lines that contain blank first or last names will be flagged, but not added to the 
    output dictionary.
    3. Each line ends in up to 3 new line escape characters, but the last field is last login,
    which should not be used.
"""
    direct_d = {}   # empty dictionary

    count = 0

    # initializing a dictionary
    file_name = raw_input('Enter name of directory dump file: ')
    try:
        open_file = open(file_name)
        title_line = open_file.readline()
        fields = title_line.split(',')
        if not len(fields) == 30:
            print "The file %s does not contain 30 fields, and cannot be parsed." % file_name
            print "Only the following fields were found:"
            print fields
            return {}

        for line in open_file:
            fields = line.split(',')
            if len(fields) < 2:
                fields = line.split(',')

            if fields[1] == "" or fields[2] == "":
                print "Found a blank name on or near line %d.  Line will not be procssed." % (count+1)

            else:
                
                new_entry = {"person_id":fields[0][1:],
                             "last_name":fields[1],
                             "first_name":fields[2],
                             "middle_name":fields[3],
                             "suffix":fields[4],
                             "email":fields[5],
                             "family_id":fields[6],
                             "family_relation":fields[7],
                             "maiden_name":fields[8],
                             "born_on":fields[9],
                             "gender":fields[10],
                             "parents":fields[11],
                             "street":fields[12],
                             "city":fields[13],
                             "state":fields[14],
                             "zip":fields[15],
                             "home_number":fields[16],
                             "work_number":fields[17],
                             "work_number_ext":fields[18],
                             "fax_number":fields[19],
                             "mobile_number":fields[20],
                             "mobile_provider":fields[21],
                             "allow_sms":fields[22],
                             "hubs":fields[23],
                             "hubs_administered":fields[24],
                             "person_created":fields[25],
                             "person_updated":fields[26],
                             "account_created":fields[27],
                             "account_updated":fields[28],
                             "last_login":fields[29][:-3]}
                   
                direct_d.update({count:new_entry})
                
            count += 1

        print "%d lines read and processed from directory file" % count

    finally:
        open_file.close()
        
    return direct_d

def Print(direct_d):
    while True:
        end_entry = int(raw_input('Enter entry at which to stop printing (enter 0 to stop): '))
        if end_entry == 0:
            break
        elif end_entry > len(direct_d):
            end_entry = len(direct_d)

        start_entry = int(raw_input('Enter entry from which to start printing: '))
        if start_entry < 0:
            start_entry += end_entry
            
        for x in range(start_entry, end_entry):
            print direct_d[x]

def main():
    direct_d = ReadDirectory()
    Print(direct_d)

if __name__ == '__main__':
    main()
