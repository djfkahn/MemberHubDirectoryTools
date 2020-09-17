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
    - file_name -- name of the file containing the MemberHub directory dump
    - hub_map   -- dictionary that maps hub names to hub IDs
    OUTPUTS:
    - directory -- list of families read from the MemberHub directory dump
    ASSUMPTIONS:
    1. The MemberHub directory dump file is a comma-separated text file comprised
       of any number of fields.  However, it is assumed the following fields appear in the file:
        1.  <id> **
        2.  <last_name> **
        3.  <first_name> **
        4.  <middle_name>
        5.  <suffix>
        6.  <email>
        7.  <family_id>
        8.  <family_relation> **
        9.  <hubs>
        10. <account_created>
        11. <account_updated>
        ** - these fields are required
    2. Lines that contain blank required fields (denoted with '**') will be flagged, but
       not added to the output dictionary.
    3. Families appear in the directory in consecutive rows
    """

    directory         = []
    rows_read         = -1
    rows_processed    = 0
    current_family_id = ''
    new_family        = False

    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for fields in csv_reader:
            ##
            ## Use the first row to determine indices of fields used
            if rows_read < 0:
                rows_read = 0
                num_fields          = len(fields)
                person_id_idx       = fields.index('id')
                last_name_idx       = fields.index('last_name')
                first_name_idx      = fields.index('first_name')
                middle_name_idx     = fields.index('middle_name')
                suffix_idx          = fields.index('suffix')
                email_idx           = fields.index('email')
                family_id_idx       = fields.index('family_id')
                family_relation_idx = fields.index('family_relation')
                hub_name_list_idx   = fields.index('hub_membership')
                account_created_idx = fields.index('account_created')
                account_updated_idx = fields.index('account_updated')
                continue

            ##
            ## After the first row...
            ## ...increment the number of rows read, regardless of validity
            rows_read += 1
            ##
            ## ...perform validity checks on the current row
            if not len(fields) == num_fields:
                PrintErrorMessage (fields, "Found row with incorrect number of fields.")
                continue

            if fields[last_name_idx] == "" or fields[first_name_idx] == "" or \
               fields[person_id_idx] == "" or fields[family_relation_idx] == "":
                PrintErrorMessage (fields, "Found a row with missing required fields.")
                continue

            ##
            ## ...by reaching this point, the row is valid.  so increment the number of
            ## rows processed.
            rows_processed += 1
            ##
            ## create a new family every time a new family ID is found
            if fields[family_id_idx] != current_family_id:
                ##
                ## to start processing a new family, append the family previously worked on
                ## (if it exists)
                if new_family:
                    directory.append(new_family)
                ##
                ## instantiate new family object
                new_family = family.Family()
                ##
                ## store the family ID currently working on
                current_family_id = fields[family_id_idx]

            ##
            ## add the person to the new family
            new_family.AddFromDirectory(person_id       = fields[person_id_idx],
                                        last_name       = fields[last_name_idx],
                                        first_name      = fields[first_name_idx],
                                        middle_name     = fields[middle_name_idx],
                                        suffix          = fields[suffix_idx],
                                        email           = fields[email_idx],
                                        family_id       = fields[family_id_idx],
                                        family_relation = fields[family_relation_idx],
                                        hub_name_list   = fields[hub_name_list_idx].split(';'),
                                        account_created = fields[account_created_idx],
                                        account_updated = fields[account_updated_idx],
                                        hub_map         = hub_map)

        else:
            ##
            ## once the last row is read, append the last family processed to the directory list
            if new_family:
                directory.append(new_family)

        ##
        ## show the user the number rows read, processed, and number of families created.
        ## these numbers can be sanity checked manually against the website directory.
        print("Read %d rows, processed %d rows, and created %d families from directory file" % \
            (rows_read, rows_processed, len(directory)))

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
