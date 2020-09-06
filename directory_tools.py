#!/usr/bin/env python
"""This module contains the tools to injest a MemberHub directory dump into
a dictionary, and display portions of the dictionary for analysis.
"""
import csv
import os
import family

def PrintErrorMessage(fields, error_text):
    print(error_text, "Line will not be processed.")
    print("The following fields were read on this row:", fields)


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
       of exactly 31 fields in the following order:
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
        24. <pta_member>
        25. <hubs>
        26. <hubs_administered>
        27. <person_created>
        28. <person_updated>
        29. <account_created>
        30. <account_updated>
        31. <last_login>
        ** - indicates required field
    2. None of the fields contain commas.
    3. Lines that contain blank required fields will be flagged, but not added to the
    output dictionary.
    """

    directory  = []
    rows_read = rows_processed = families_created = 0
    new_family = False
    family_id  = 0

    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for fields in csv_reader:
            # Skip the first row
            if rows_read == 0:
                rows_read += 1
                continue

            rows_read += 1
            if not len(fields) == 31:
                PrintErrorMessage \
                    (fields, "Found row with incorrect number of fields.")
                continue

            if fields[1] == "" or fields[2] == "" or \
               fields[0] == "" or fields[7] == "":
                PrintErrorMessage \
                    (fields, "Found a row with missing required fields.")
                continue

            rows_processed += 1
            # create a new family every time a new family ID is found
            if fields[6] != family_id:
                # to start processing a new family, append the family previously worked on
                # (if it exists)
                if new_family:
                    directory.append(new_family)
                # instantiate new family object
                new_family = family.Family()
                # increment number of families created
                families_created += 1
                # store the family ID currently working on
                family_id = fields[6]

            # add the person to the new family
            new_family.AddFromDirectory(fields, hup_map)

        else:
            # once the last row is read, append the last family processed to the
            # directory list
            if new_family:
                directory.append(new_family)
            # remove one from the rows read to take away the header row
            rows_read -= 1


        print("Read %d rows, processed %d rows, and created %d families from directory file" % \
            (rows_read, rows_processed, families_created))

    return directory


def ReadDirectory(hub_map):
    """ roster_tools.ReadDirectory
    PURPOSE:
    Prompts the user for directory file name and proceeds to read the file.
    INPUT:
    - hub_map   -- mapping of teacher names to hub numbers
    OUTPUTS:
    - directory -- list of families extracted from the directory file
    ASSUMPTIONS:
    - All the candidate directories reside in a folder called "Directory" under the
      run directory.
    - All candidate directories are text CSV files.
    """
    print ("These are the potential directory files:")
    file_path = os.path.abspath("./Directory/")
    with os.scandir(file_path) as raw_files:
        files = [file for file in raw_files if (file.name.endswith('.csv'))]
        files.sort(key=lambda x: os.stat(x).st_mtime, reverse=True)

        index = 0
        for file in files:
            index += 1
            print("%d) %s" % (index, file.name))

        file_number = input("Enter list number of file or press <enter> to use '" + files[0].name + "':")
        if not file_number:
            return ReadDirectoryFromFile(file_path + "/" +files[0].name, hub_map)
        elif 0 < int(file_number) and int(file_number) <= index:
            return ReadDirectoryFromFile(file_path + "/" + files[int(file_number)-1].name, hub_map)
        else:
            print("The selection made is out of range.  Please try again.")
            ReadDirectory(hub_map)
