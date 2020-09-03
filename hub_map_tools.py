#!/usr/bin/env python
"""This program inputs the map of elementary school teachers to hub names.
It assumes the presence of a file called 'hub_map.csv' in the directory from
which the program is executed.
"""
import csv
import os

def ConvertHubStringListToIDList(hub_name_list, map_d):
    """hub_map_tools.ConvertHubStringListToIDList
    INPUTS:
    - hub_name_list -- list of hub or teacher names
    - map_d         -- dictionary that maps hub/teacher names to hub IDs
    OUTPUTS:
    - hub_id_list   -- list of hub IDs corresponding to the hub_name_list.
                       if a corrsponding ID is not in the map, the original
                       hub name is returned in that position.
    """
    hub_id_list = []

    for hub_name in hub_name_list:
        # strip off quotes
        if isinstance(hub_name, str):
            hub_name = hub_name.strip('"')
            if len(hub_name) == 0:
                continue

        # check if the hub name is among map keys
        if hub_name in map_d.keys():
            hub_id_list.append(map_d[hub_name])
        else:
            hub_id_list.append(hub_name)

    return hub_id_list



def ConvertToHubIDList(hub_name_list):
    return ConvertHubStringListToIDList(hub_name_list, ReadHubMap())



def CreateEmptyHubDictionary(raw_map):
    raw_values = raw_map.values()
    temp = ['0']
    for val in sorted(raw_values):
        if temp[-1] != val:
            temp.append(val)
    reduced_values = temp[1:]
    new_map = {}
    for val in reduced_values:
        new_map[val] = []
    return new_map

def PrintReadErrorMessage(line, message):
    print(message, "Skipping this line.")
    print("Line read:", line)

def ReadHubMapFromFile(file_name):
    """hub_map_tools.ReadHubMapFromFile()
    INPUTS:
    - file_name -- name of the file containing the hub map.
    OUTPUTS:
    - map_d     -- dictionary for which the key is the teacher or grade name,
                   and the values are the associated hub IDs.
    ASSUMPTONS:
    1. The data file has two fields per line, separated by a "|"
    2. Additional fields after the 2nd field are comments
    3. Lines beginning with a hash, "#", are comments
    """
    map_d = {}

    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')

        for fields in csv_reader:
            ## skip line if the first character is a comment
            if fields[0][0] == "#":
                continue
            ## skip lines that do not have the right number of fields
            if len(fields) < 2:
                PrintReadErrorMessage \
                    (line, "Not enough fields found on this line.")
                continue
            ## skip lines for which the teacher name is not unique
            if fields[0] in map_d.keys():
                PrintReadErrorMessage \
                    (line, "Duplicate teacher found on this line.")
                continue

            map_d.update({fields[0]:fields[1]})

    return map_d

def ReadHubMap():
    """hub_map_tools.IsInClassroomHub(map_d, hub_id)
    INPUTS:
    - none
    OUTPUTS:
    - a dictionary that maps the teacher names to their hub numbers
    ASSUMPTIONS:
    - the hub map is documented in a CSV file called 'hub_map.csv'
    """
    return ReadHubMapFromFile('hub_map.csv')


def IsInClassroomHub(map_d, hub_id):
    """hub_map_tools.IsInClassroomHub(map_d, hub_id)
    INPUTS:
    - map_d    -- dictionary containing the map of teachers to hub IDs
    - hub_id   -- hub ID to check against classroom hubs
    OUTPUTS:
    - True     -- if the hub_id matches any classroom hub ID in the hub map,
                  or if the hub_id is either the "Teachers" or "Staff" hub
    - False    -- otherwise
    ASSUMPTIONS:
    None
    """
    return hub_id in map_d.values() or \
           hub_id == "Teachers" or \
           hub_id == "Staff" or \
           hub_id == "Volunteers"


def IsAnyHubClassroomHub(map_d, hubs):
    """hub_map_tools.IsAnyHubClassroomHub(map_d, hub_field)
    INPUTS:
    - map_d     -- dictionary containing the map of teachers to HUB IDs
    - hub       -- list of hubs to check against classroom hubs
    OUTPUTS:
    - True      -- if any of the hubs in hub_field qualify as classroom hubs
    - False     -- otherwise
    ASSUMPTIONS:
    If hub_field is not empty, its hubs are separated by semi-colons (";").
    """
    for hub in hubs:
        if IsInClassroomHub(map_d, hub):
            return True

    return False


def IsInMultipleClassroomHubs(map_d, hubs):
    """hub_map_tools.IsInMultipleClassroomHubs
    INPUTS:
    - map_d     -- dictionary containing the map of teachers to HUB IDs
    - hubs      -- list of hubs to check against classroom hubs
    OUTPUTS:
    - True      -- if more than one hub in the hubs list qualify as classroom hub
    - False     -- otherwise
    ASSUMPTIONS:
    If hub_field is not empty, its hubs are separated by semi-colons (";").
    """
    count = 0
    for hub in hubs:
        if IsInClassroomHub(map_d, hub):
            count += 1

    return count > 1
