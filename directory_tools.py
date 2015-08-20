#!/usr/bin/env python
"""This module contains the tools to injest a MemberHub directory dump into
a dictionary, and display portions of the dictionary for analysis.
"""

import family

def PrintErrorMessage(fields, error_text):
    print error_text, "Line will not be processed."
    print "The following fields were read on this line:",
    print fields
    

def ReadDirectoryFromFile(file_name, hub_map):
    """directory_tools.ReadDirectory
    INPUTS:
    Prompts user for name of comma-separated text file containing MemberHub directory dump.
    INPUTS:
    - file_name -- name of the file containing the MemberHub directory dump
    - hub_map   -- dictionary that maps hub names to hub IDs
    OUTPUTS:
    - directory -- list of families read from the MemberHub directory dump
    ASSUMPTIONS:
    1. The MemberHub directory dump file is a comman separated text file comprised
       of exactly 30 fields in the following order:
        1.  <person_id> **
        2.  <last_name> **
        3.  <first_name> **
        4.  <middle_name>
        5.  <suffix>
        6.  <email>
        7.  <family_id>
        8.  <family_relation> **
        9.  <maiden_name>
        10. <born_on>
        11. <gender>
        12. <parents>
        13. <street>
        14. <city>
        15. <state>
        16. <zip>
        17. <home_number>
        18. <work_number>
        19. <work_number_ext>
        20. <fax_number>
        21. <mobile_number>:
        22. <mobile_provider>
        23. <allow_sms>
        24. <hubs>
        25. <hubs_administered>
        26. <person_created>
        27. <person_updated>
        28. <account_created>
        29. <account_updated>
        30. <last_login>
        ** - indicates required field
    2. None of the fields contain commas.
    3. Lines that contain blank required fields will be flagged, but not added to the 
    output dictionary.
    """

    directory  = []
    lines_read = lines_processed = families_created = 0
    new_family = False

    try:
        open_file = open(file_name)
        title_line = open_file.readline()
        fields = title_line.split(',')
        if not len(fields) == 30:
            PrintErrorMessage \
                (fields, "The file %s does not contain 30 fields, and cannot be parsed." % file_name)
            raise RuntimeError, "This directory file has %d fields, but 30 are expected." % len(fields)

        for line in open_file:
            lines_read += 1
            fields = line.split(',')
            if not len(fields) == 30:
                PrintErrorMessage \
                    (fields, "Found line with incorrect number of fields.")
                continue

            if fields[1] == "" or fields[2] == "" or \
               fields[0] == "" or fields[7] == "":
                PrintErrorMessage \
                    (fields, "Found a line with missing required fields.")
                continue

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
                new_family.AddAdultFromDirectory(fields, hub_map)
            elif fields[7][:5].lower() == "child":
                new_family.AddChildFromDirectory(fields, hub_map)
            else:
                PrintErrorMessage \
                    (fields, "Found entry in directory that is neither an adult nor a child.")

        else:
            # once the last line is read, append the last family processed to the
            # directory list
            if new_family:
                directory.append(new_family)

        print "Read %d lines, processed %d lines, and created %d families from directory file" % \
            (lines_read, lines_processed, families_created)

    finally:
        open_file.close()
        
    return directory


def ReadDirectory(hub_map):
    file_name = raw_input('Enter name of directory dump file (press <enter> to use "dump.csv"): ')
    if not file_name:
        file_name = "dump.csv"

    return ReadDirectoryFromFile(file_name, hub_map)


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
            
        for x in directory[start_entry:end_entry]:
            x.Print()

def main():
    test_directory_files = \
        {"directory_tools_tests/test_directory_general.csv": \
            {"error_expected":False,"number_read":3}, \
         "directory_tools_tests/test_directory_no_first_name.csv": \
            {"error_expected":False,"number_read":1}, \
         "directory_tools_tests/test_directory_no_last_name.csv": \
            {"error_expected":False,"number_read":1},
         "directory_tools_tests/test_directory_no_person_id.csv": \
            {"error_expected":False,"number_read":1},
         "directory_tools_tests/test_directory_no_family_relation.csv": \
            {"error_expected":False,"number_read":1},
         "directory_tools_tests/test_directory_29_fields.csv": \
            {"error_expected":True,"number_read":0}}

    for directory_file in test_directory_files.keys():
        try:
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++"
            print "Testing directory file " + directory_file + "."
            test_directory = ReadDirectoryFromFile(directory_file,{})
            print "Processed directory file successfully",
            if test_directory_files[directory_file]["error_expected"]:
                print "which NOT EXPECTED."
            else:
                print "as expected."
                if len(test_directory) == test_directory_files[directory_file]["number_read"]:
                    print "The expected number of lines were processed."
                else:
                    print "UNEXPECTED number of lines processed."
        except:
            print "Error reading directory file " + directory_file,
            if test_directory_files[directory_file]["error_expected"]:
                print "as expected."
            else:
                print "where error was NOT EXPECTED."

##    directory = ReadDirectory()
##    Print(directory)

if __name__ == '__main__':
    main()
