#!/usr/bin/env python
"""This program inputs the map of elementary school teachers to hub names.
It assumes the presence of a file called 'hub_map.csv' in the directory from
which the program is executed.
"""

map_d = {}   # empty dictionary

def ConvertToHubIDList(hub_name_list):
    hub_id_list = []
    for hub_name in hub_name_list:
        hub_id_list.append(map_d[hub_name])
    
    return hub_id_list

def ReadMap():
    """hub_map_tools.ReadMap() 
    INPUTS:  
    Reads the 'hub_map.csv' file in the run directory.
    OUTPUTS:
    A dictionary for which the key is the teacher or grade name, and the
    values are the associated Hub IDs.
    ASSUMPTONS:
    This function assumes the data file has two fields per line, separated by a "|",
    and that the last two characters of each line are carriage returns symbols.
    """
    count = 0

    try:
        open_file = open('hub_map.csv')

        for line in open_file:
            fields = line.split('|')
            ## be sure to strip the '\r\n' that Excel adds at the end of lines
            map_d.update({fields[0]:fields[-1][:-2]})
            count += 1

        print "%d hub IDs read and processed." % count

    finally:
        open_file.close()
        
    return map_d

def IsInClassroomHub(map_d, hub_id):
    """hub_map_tools.IsInClassroomHub(map_d, hub_id)
    INPUTS:
    - map_d    -- dictionary containing the map of teachers to HUB IDs
    - hub_id   -- hub ID to check against classroom hubs
    OUTPUTS:
    - True     -- if the hub_id matches any classroom hub ID in the hub map
    - False    -- otherwise
    ASSUMPTIONS:
    None
    """
    return hub_id in map_d.values()
    
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
    
def PrintMap(map_d):
    print map_d

def main():
    map_d = ReadMap()
    PrintMap(map_d)

if __name__ == '__main__':
    main()
