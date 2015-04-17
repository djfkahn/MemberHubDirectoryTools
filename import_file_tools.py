#!/usr/bin/env python
"""The tools held in this file create comma separated data files that can be
imported into MemberHub.
"""

from time import localtime, strftime

def FormTimeTag():
    tag = strftime("%Y-%m-%d-%H-%M-%S", localtime())
    return tag

def CreateNewMemberImport(update_d):
    """CreateHubUpdateCSV
Inputs : update_d - a dictionary containing the first/last name, hub memberships
                    and person ID to be updated
Outputs: None
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
        open_file.write("family_relation,first_name,last_name,hubs,person_id\n")

        for entry in update_d.keys():
            line = "%s,%s,%s,%s,%s\n" % \
                       (update_d[entry]["family_relation"],
                        update_d[entry]["first_name"],
                        update_d[entry]["last_name"],
                        update_d[entry]["hubs"],
                        update_d[entry]["person_id"])
            open_file.write(line)

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
