#!/usr/bin/env python
"""This program inputs a MemberHub directory dump, and analyzes it.
"""
import family
import roster
import os
from openpyxl import load_workbook

NUM_ROSTER_FIELDS = 5

def ReadRosterFromFile(file_name, hub_map):
    """ roster_tools.ReadRosterFromFile
    PURPOSE:
    Reads a roster file with the following fields:
    <**Last Name>,<**First Name>,<**Grade>,<**Parent/Guardian Name(s)>,<***Teacher Name>
    **  - indicates always required field
    *** - indicates field that is required when Grade field is < 6
    INPUT:
    - file_name -- name of the roster file
    - hub_map   -- dictionary that maps hub names to hub IDs
    OUTPUTS:
    - roster    -- list of families extracted from the roster
    ASSUMPTIONS:
    1. First row of the file is the column headers...not a member of the roster.
    """
    wb = load_workbook(file_name)
    ws = wb.active

    rosterC       = roster.Roster()
    student_count = 0

    for fields in ws.values:

        # Skip the first row
        if student_count == 0:
            student_count += 1
            continue

        if fields[0] == "" or fields[1] == "" or fields[2] == "" or \
           fields[3] == "" or (int(fields[2]) < 6 and fields[4] == ""):
            print("Found row with missing required fields:", fields)
            continue

        # each row represents one student
        student_count += 1

        new_family = family.Family()
        new_family.CreateFromRoster(fields  = fields,
                                    hub_map = hub_map,
                                    rosterC = rosterC)

        # if new_family is the same as a family already in the roster, then combine
        # families.  Otherwise, append new_family at the end of the roster.
        for roster_entry in rosterC.GetRoster():
            if roster_entry.IsSameFamily(new_family):
                roster_entry.CombineWith(new_family)
                break
        else:
            rosterC.append(new_family)

    print("%d students processed %d families." % (student_count, len(rosterC)))

    return rosterC.GetRoster()


def ReadRoster(hub_map):
    """ roster_tools.ReadRoster
    PURPOSE:
    Prompts the user for roster file name and proceeds to read the file.
    INPUT:
    - none
    OUTPUTS:
    - roster    -- list of families extracted from the roster
    ASSUMPTIONS:
    none
    """

    print ("These are the potential roster files:")
    files = [file for file in os.listdir(".") if (file.lower().endswith('.xlsx'))]
    files.sort(key=os.path.getmtime)
    files = sorted(files,key=os.path.getmtime, reverse=True)

    index = 1
    for file in sorted(files,key=os.path.getmtime, reverse=True):
        print("%d) %s" % (index, file))
        index += 1

    file_number = input("Enter list number of file or press <enter> to use '" + files[0] + "':")
    if not file_number:
        file_name = files[0]
    else:
        file_name = files[file_number-1]

    return ReadRosterFromFile(file_name, hub_map)


def PrintEntries(testRoster):
    while True:
        end_entry = int(input("Enter entry at which to stop printing (enter 0 to stop): "))
        if end_entry == 0:
            break
        elif end_entry > len(testRoster):
            end_entry = len(testRoster)

        start_entry = int(input("Enter entry from which to start printing: "))
        if start_entry < 0:
            start_entry += end_entry

        for x in testRoster[start_entry:end_entry]:
            x.Print()


def main():

    test_roster_files = \
        {"roster_tools_tests/test_roster_general.csv": \
            {"error_expected":False,"number_read":2}, \
         "roster_tools_tests/test_roster_no_parents.csv": \
            {"error_expected":False,"number_read":0}, \
         "roster_tools_tests/test_roster_no_teacher.csv": \
            {"error_expected":False,"number_read":1},
         "roster_tools_tests/test_roster_four_fields.csv": \
            {"error_expected":True,"number_read":0}}

    for roster_file in test_roster_files.keys():
        try:
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("Testing roster file " + roster_file + ".")
            test_roster = ReadRosterFromFile(roster_file,{})
            print("Processed roster file successfully",)
            if test_roster_files[roster_file]["error_expected"]:
                print("which NOT EXPECTED.")
            else:
                print("as expected.")
                if len(test_roster) == test_roster_files[roster_file]["number_read"]:
                    print("The expected number of lines were processed.")
                else:
                    print("UNEXPECTED number of lines processed.")
        except:
            print("Error reading roster file " + roster_file,)
            if test_roster_files[roster_file]["error_expected"]:
                print("as expected.")
            else:
                print("where error was NOT EXPECTED.")


if __name__ == '__main__':
    main()
