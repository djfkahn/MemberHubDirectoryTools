#!/usr/bin/env python
'''The tools held in this file create comma separated data files that can be
imported into MemberHub.
'''

import person
import family
import os

from time import localtime, strftime


def FormTimeTag():
    tag = strftime('%Y-%m-%d-%H-%M-%S', localtime())
    return tag



def FormFullFileName(file_prefix, file_extention):
    ##
    ## by default, place the file in the current directory
    file_path = os.path.abspath('.')
    ##
    ## if the current directory is the root directory or does not exist,
    ## place the file on the current user's Desktop.
    if file_path == '/' or not os.path.exists(file_path):
        file_path = os.path.expanduser('~/Desktop')
    ##
    ## formulate the file name, and print it to the 
    file_name = file_path + '/' + file_prefix + '_' + FormTimeTag() + file_extention
    print('Writing to file:  ' + file_name)
    
    return file_name



def WriteToFile(open_file, fields, separator):
    open_file.write(str(fields[0]))
    for field in fields[1:]:
        line = separator + str(field).replace(',','|')
        open_file.write(line)
    open_file.write('\n')



def WriteNewMemberPerson(open_file, new_person):
    if isinstance(new_person, person.DirectoryPerson):
        person_id   = new_person.person_id
    else:
        person_id   = ''

    WriteToFile(open_file = open_file,
                fields    = [new_person.family_relation, new_person.first_name, new_person.last_name, person_id],
                separator = ',')



def CreateFileFromFamily(entriless):
    '''CreateFileFromFamily
    Inputs : entriless - list of families that need to be added to the directory
    Outputs: Creates a file called 'new_member_import_<date tag>.csv' in the
             run directory
    Summary: 1. asks user to name file to be written to.  this file will be
                over-written!
             2. opens file for writing, and writes the column titles
             3. iterates over the inputs to write the data to the file
             4. closes the file
'''

    file_name = FormFullFileName('new_member_import', '.csv')
    with open(file_name, 'w') as open_file:
        WriteToFile(open_file = open_file,
                    fields    = ['family_relation', 'first_name', 'last_name', 'person_id'],
                    separator = ',')

        for new_family in entriless:
            for new_adult in new_family.adults:
                WriteNewMemberPerson(open_file, new_adult)
            for new_child in new_family.children:
                WriteNewMemberPerson(open_file, new_child)



def CreateFileFromPeople(people, file_prefix):
    '''CreateFileFromPeople
    Inputs : people      - list of people whose need to write in created file
             file_prefix - string that starts the name of the import file
    Outputs: Creates a file called '<file_prefix>_<date tag>.csv' in the
             run directory
    Summary: 1. opens file for writing, and writes the column titles
             2. iterates over the inputs to write the data to the file
             3. closes the file
    '''

    file_name = FormFullFileName(file_prefix, '.csv')
    with open(file_name, 'w') as open_file:
        
        if len(people) < 1:
            open_file.write('All adults in this category have EDS PTO MenberHub accounts.\n')
            
        else:
            
            WriteToFile(open_file = open_file,
                        fields    = ['First Name', 'Last Name', 'Affiliated Hub(s)', 'Email'],
                        separator = ',')

            for this_person in people:
                if this_person.DoesNotListEmailAddress():
                    WriteToFile(open_file = open_file,
                                fields    = [this_person.first_name, this_person.last_name, this_person.hubs, ' '],
                                separator = ',')
                else:
                    WriteToFile(open_file = open_file,
                                fields    = [this_person.first_name, this_person.last_name, this_person.hubs, this_person.email],
                                separator = ',')


def CreateByHubFile(map_d, hub_map, file_prefix):

    file_name = FormFullFileName(file_prefix, '.txt')
    with open(file_name, 'w') as open_file:
        for hub in map_d.keys():
            open_file.write('-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-\n')
            open_file.write('Hub ID: ' + hub + '\n')
            ##
            ## print the hub's potential teacher name(s) by matching hub ID to hub map keys
            for map_key in hub_map.keys():
                if hub_map[map_key] == hub:
                    open_file.write('\t\t--> Possible Hub Name: ' + map_key + '\n')
            ##
            ## print a different message if the hub has no adults without emails
            if len(map_d[hub]) < 1:
                open_file.write('All adults in this hub have email addresses in the directory\n')
            else:
                ##
                ## add each person in the hub's list
                open_file.write(str(len(map_d[hub])) + ' people without emails found in this hub\n\n')
                number = 1
                for this_person in map_d[hub]:
                    WriteToFile(open_file = open_file,
                                fields    = [str(number), this_person.last_name, this_person.first_name],
                                separator = ', ')
                    number += 1

            open_file.write('\n')

