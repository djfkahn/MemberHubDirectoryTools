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

def WriteNewMemberLine(open_file, family_relation, first_name, last_name, person_id):
    line = "%s,%s,%s,%s\n" % (family_relation, first_name, last_name, person_id)
    open_file.write(line)

def WriteNewMemberPerson(open_file, new_person):
    if isinstance(new_person, person.RosterPerson):
        person_id   = ''
    else:
        person_id   = new_person.person_id
    WriteNewMemberLine(open_file       = open_file,
                       family_relation = new_person.family_relation,
                       first_name      = new_person.first_name,
                       last_name       = new_person.last_name,
                       person_id       = person_id)

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
    print("Writing to import file called %s." % file_name)
    try:
        open_file = open(file_name,"w")
        WriteNewMemberLine(open_file,'family_relation', 'first_name', 'last_name', 'person_id')

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
    print("Writing to import file called %s." % file_name)
    try:
        open_file = open(file_name,"w")
        WriteHublessLine (open_file, "first_name", "last_name", "hubs", "person_id")

        for this_person in people:
            WriteHublessLine(open_file  = open_file,
                             first_name = this_person.first_name,
                             last_name  = this_person.last_name,
                             hubs       = this_person.hubs,
                             person_id  = this_person.person_id)

    finally:
        open_file.close()



def CreateEmaillessFile(people, file_prefix):

    file_name = file_prefix + "_" + FormTimeTag() + ".txt"
    print("Writing to file called %s." % file_name)
    try:
        open_file = open(file_name,"w")
        for person in people:
            line = "%s|%s|%s|%s\n" % (person.first_name, person.last_name, person.family_relation, person.hubs)
            open_file.write(line)


    finally:
        open_file.close()
