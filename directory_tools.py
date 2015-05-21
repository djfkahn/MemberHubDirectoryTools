#!/usr/bin/env python
"""This module contains the tools to injest a MemberHub directory dump into
a dictionary, and display portions of the dictionary for analysis.
"""

import family

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
    directory  = []   # empty list
    lines_read = lines_processed = families_created = 0

    # initializing a dictionary
    file_name = raw_input('Enter name of directory dump file: ')
    try:
        open_file = open(file_name)
        title_line = open_file.readline()
        fields = title_line.split(',')
        if not len(fields) == 30:
            print "The file %s does not contain 30 fields, and cannot be parsed." % file_name
            print "The following fields were found:"
            print fields
            return []

        for line in open_file:
            lines_read += 1
            fields = line.split(',')
            if not len(fields) == 30:
                print "Incorrect number of fields found on or near line %d.  Line will not be processed." % (count+1)
                print "The following fields were read on this line:"
                print fields

            elif fields[1] == "" or fields[2] == "":
                print "Found a blank name on or near line %d.  Line will not be procssed." % (count+1)
                print "The following fields were read on this line:"
                print fields

            else:
                lines_processed += 1
                # according to MemberHub.com, a new family begins each time the family_relation (field 7)
                # is not numbered (i.e. just "Adult" or just "Child"), so start a new family when that
                # condition is detected
                if fields[7].lower() in ("adult", "child"):
                    # to start processing a new family, append the family previously worked on (if
                    # it exists), then instantiate a new Family class
                    if new_family:
                        directory.append(new_family)
                    new_family = family.Family()
                    families_created += 1
                    
                if fields[7][:5].lower() == "adult":
                    new_family.AddAdultFromDirectory(fields)
                elif fields[7][:5].lower() == "child":
                    new_family.AddChildFromDirectory(fields)
                else:
                    print "Found entry in directory that is neither an adult nor a child."
                    print "The following fields were read on this line:"
                    print fields

        else:
            if new_family:
                directory.append(new_family)

        print "Read %d lines, processed %d lines, and created %d families from directory file" % \
            (lines_read, lines_processed, families_created)

    finally:
        open_file.close()
        
    return directory

def Print(directory):
    while True:
        end_entry = int(raw_input('Enter entry at which to stop printing (enter 0 to stop): '))
        if end_entry == 0:
            break
        elif end_entry > len(directory):
            end_entry = len(directory)

        start_entry = int(raw_input('Enter entry from which to start printing: '))
        if start_entry < 0:
            start_entry += end_entry
            
        for x in directory[start_entry, end_entry]:
            x.Print()

def main():
    directory = ReadDirectory()
    Print(directory)

if __name__ == '__main__':
    main()
