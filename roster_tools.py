#!/usr/bin/env python
"""This program inputs a MemberHub directory dump, and analyzes it.
"""
import family
import roster

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
    try:
        open_file = open(file_name)
        raw_line = open_file.readline()
        if len(raw_line.split(',')) != 5:
            raise RuntimeError, "This roster file has %d fields, but 5 are expected." % len(raw_line.split(','))

        rosterC       = roster.Roster()
        student_count = 0

        for line in open_file:
            # process the line without the trailing '\r\n' that Excel adds
            fields = line.strip('\n\r').strip('"').split(',')

            if len(fields) > NUM_ROSTER_FIELDS:
            	temp_field = fields[4].strip('"')+","+fields[5]
            	if len(fields) > NUM_ROSTER_FIELDS+1:
            		temp_field += ","+fields[6].strip('"')
            	fields[4]=temp_field

            if fields[0] == "" or fields[1] == "" or fields[2] == "" or \
               fields[3] == "" or (int(fields[2]) < 6 and fields[4] == ""):
                print "Found line with missing required fields:",
                print fields
                continue

            # each line read represents one student
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

        print "%d students processed %d families." % (student_count, len(rosterC))

    finally:
        open_file.close()

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
    file_name = raw_input('Enter name of roster comma-separated text file (press <enter> to use "roster.csv"): ')
    if not file_name:
        file_name = "roster.csv"

    return ReadRosterFromFile(file_name, hub_map)


def PrintEntries(testRoster):
    while True:
        end_entry = int(raw_input('Enter entry at which to stop printing (enter 0 to stop): '))
        if end_entry == 0:
            break
        elif end_entry > len(testRoster):
            end_entry = len(testRoster)

        start_entry = int(raw_input('Enter entry from which to start printing: '))
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
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++"
            print "Testing roster file " + roster_file + "."
            test_roster = ReadRosterFromFile(roster_file,{})
            print "Processed roster file successfully",
            if test_roster_files[roster_file]["error_expected"]:
                print "which NOT EXPECTED."
            else:
                print "as expected."
                if len(test_roster) == test_roster_files[roster_file]["number_read"]:
                    print "The expected number of lines were processed."
                else:
                    print "UNEXPECTED number of lines processed."
        except:
            print "Error reading roster file " + roster_file,
            if test_roster_files[roster_file]["error_expected"]:
                print "as expected."
            else:
                print "where error was NOT EXPECTED."


if __name__ == '__main__':
    main()
