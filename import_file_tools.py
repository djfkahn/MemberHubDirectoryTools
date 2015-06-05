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

def WriteNewMemberLine(open_file, family_relation, first_name, last_name, hubs, person_id):
    line = "%s,%s,%s,%s,%s\n" % (family_relation, first_name, last_name, hubs, person_id)
    open_file.write(line)

def WriteNewMemberPerson(open_file, new_person):
    family_relation = new_person.family_relation
    first_name = new_person.first_name
    last_name  = new_person.last_name
    hubs = ""
    for hub_id in new_person.hubs:
        hubs = str(hub_id) + ";"
    hubs       = hubs[:-1]  # strip off the trailing ';'
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
            for new_adult in new_family.GetAdults():
                WriteNewMemberPerson(open_file, new_adult)
            for new_child in new_family.GetChildren():
                WriteNewMemberPerson(open_file, new_child)

    finally:
        open_file.close()


def CreateHublessImportFile(update_d):
    """CreateHublessImportFile
Inputs : update_d - a dictionary containing the first/last name, hub memberships
                    and person ID to be updated
Outputs: None
Summary: 1. asks user to name file to be written to.  this file will be
            over-written!
         2. opens file for writing, and writes the column titles
         3. iterates over the inputs to write the data to the file
         4. closes the file
"""
 
    file_name = "hubless_import_" + FormTimeTag() + ".csv"
    print "Writing to import file called %s." % file_name
    try:
        open_file = open(file_name,"w")
        open_file.write("first_name,last_name,hubs,person_id\n")

        for entry in update_d.keys():
            line = "%s,%s,%s,%s\n" % \
                       (update_d[entry]["first_name"],
                        update_d[entry]["last_name"],
                        update_d[entry]["hubs"],
                        update_d[entry]["person_id"])
            open_file.write(line)

    finally:
        open_file.close()
