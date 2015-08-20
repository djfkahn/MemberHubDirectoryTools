#!/usr/bin/env python
"""The tools held in this file create comma separated data files that can be
imported into MemberHub.
"""

import person
import family

from time import localtime, strftime

def FormTimeTag():
    tag = strftime("%Y-%m-%d-%H-%M-%S", localtime())
    return tag

def ConvertHubListToImportString(hub_list):
    hub_str = "/"
    for hub in hub_list:
        hub_str += str(hub) + "/"
        
    return hub_str  # strip off the trailing ';'
    
def WriteNewMemberLine(open_file, family_relation, first_name, last_name, hubs, person_id):
    line = "%s,%s,%s,%s,%s\n" % (family_relation, first_name, last_name, hubs, person_id)
    open_file.write(line)

def WriteNewMemberPerson(open_file, new_person):
    family_relation = new_person.family_relation
    first_name = new_person.first_name
    last_name  = new_person.last_name
    hubs = ConvertHubListToImportString(new_person.hubs)
    person_id  = ''
    WriteNewMemberLine(open_file, family_relation, first_name, last_name, hubs, person_id)
    
def CreateNewMemberImport(entriless):
    """CreateHubUpdateCSV
Inputs : entriless - list of families that need to be added to the directory
Outputs: Creates a file called 'new_member_import_<date tag>.csv' in the
         run directory
Summary: 1. asks user to name file to be written to.  this file will be
            over-written!
         2. opens file for writing, and writes the column titles
         3. iterates over the inputs to write the data to the file
         4. closes the file
"""
 
    file_name = "new_member_import_" + FormTimeTag() + ".csv"
    print "Writing to import file called %s." % file_name
    try:
        open_file = open(file_name,"w")
        WriteNewMemberLine(open_file,'family_relation', 'first_name', 'last_name', 'hubs','person_id')

        for new_family in entriless:
            for new_adult in new_family.adults:
                WriteNewMemberPerson(open_file, new_adult)
            for new_child in new_family.children:
                WriteNewMemberPerson(open_file, new_child)

    finally:
        open_file.close()


def WriteHublessLine(open_file, first_name, last_name, hubs, person_id):
    line = "%s,%s,%s,%s\n" % (first_name, last_name, hubs, person_id)
    open_file.write(line)

def WriteHublessPerson(open_file, new_person):
    first_name = new_person.first_name
    last_name  = new_person.last_name
    hubs = ConvertHubListToImportString(new_person.hubs)
    person_id  = new_person.person_id
    WriteHublessLine(open_file, first_name, last_name, hubs, person_id)
    
def CreateHublessImportFile(hubless):
    """CreateHublessImportFile
Inputs : hubless - list of persons that need their hubs updated
Outputs: Creates a file called 'hubless_import_<date tag>.csv' in the
         run directory
Summary: 1. opens file for writing, and writes the column titles
         2. iterates over the inputs to write the data to the file
         3. closes the file
"""
 
    file_name = "hubless_import_" + FormTimeTag() + ".csv"
    print "Writing to import file called %s." % file_name
    try:
        open_file = open(file_name,"w")
        WriteHublessLine (open_file, "first_name", "last_name", "hubs", "person_id")

        for update_person in hubless:
            WriteHublessPerson(open_file, update_person)

    finally:
        open_file.close()


def CreateHubImportFile(people,file_prefix):
    """CreateStudentHubFile
Inputs : people      - list of people whose need to be populated in hubs
         file_prefix - string that starts the name of the import file
Outputs: Creates a file called '<file_prefix>_<date tag>.csv' in the
         run directory
Summary: 1. opens file for writing, and writes the column titles
         2. iterates over the inputs to write the data to the file
         3. closes the file
"""
 
    file_name = file_prefix + "_" + FormTimeTag() + ".csv"
    print "Writing to import file called %s." % file_name
    try:
        open_file = open(file_name,"w")
        WriteHublessLine (open_file, "first_name", "last_name", "hubs", "person_id")

        for this_person in people:
            WriteHublessPerson(open_file, this_person)

    finally:
        open_file.close()
