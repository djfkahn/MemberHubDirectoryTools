#!/usr/bin/env python
"""This program inputs the map of elementary school teachers to hub names.
It assumes the presence of a file called 'hub_map.csv' in the directory from
which the program is executed.
"""

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


def ConvertHubIDListToStringList(hub_id_list, map_d):
    """hub_map_tools.ConvertHubIDListToStringList
    INPUTS:
    - hub_id_list   -- list of hub IDs
    - map_d         -- dictionary that maps hub/teacher names to hub IDs
    OUTPUTS:
    - hub_name_list -- list of hub names corresponding to the hub_name_list.
                       if a corrsponding ID is not in the map, the original
                       hub name is returned in that position.
    """
"""
    hub_name_list = []

    if IsAnyHubClassroomHub(map_d, hub_id_list):
	    for hub_id in hub_id_list:
    	    # check if the hub name is among map keys
        	if IsInClassroomHub(map_d, hub_id):
        		temp_list = map_d.values().find(hub_id)
        		hub_name_list.append(temp_list.min())

    return hub_name_list
"""

"""
def ConvertToHubStringList(hub_name_list):
    return ConvertHubIDListToStringList(hub_name_list, ReadHubMap())
"""

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

    try:
        open_file = open(file_name)

        for line in open_file:
            if line[0] == "#":
                continue
            ## be sure to strip the '\r\n' that Excel adds at the end of lines
            fields = line.strip('\r\n').split('|')
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

    finally:
        open_file.close()

    return map_d

def ReadHubMap():
    file_name = input("Enter name of hub map file (press <enter> to use \"hub_map.csv\"): ")
    if not file_name:
        file_name = "hub_map.csv"

    return ReadHubMapFromFile(file_name)


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
    ## MODIFIED CODE BEGIN - 2017-09-06
    return hub_id in map_d.values() or \
           hub_id == "Teachers" or \
           hub_id == "Staff" or \
           hub_id == "Volunteers"
    ## MODIFIED CODE END

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
    print(map_d)

def main():
    print("====================================")
    print("Unit Under Test:  ReadHubMapFromFile")
    test_files = \
        {"hub_map_tools_tests/test_hub_map_general.csv": \
            {"error_expected":False,"number_read":3}, \
         "hub_map_tools_tests/test_hub_map_duplicate.csv": \
            {"error_expected":False,"number_read":2}, \
         "hub_map_tools_tests/test_hub_map_1_field.csv": \
            {"error_expected":False,"number_read":2}}

    for hub_map_file in test_files.keys():
        try:
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("Testing hub map file " + hub_map_file + ".")
            test_hub_map = ReadHubMapFromFile(hub_map_file)
            print("Processed hub map file successfully",)
            if test_files[hub_map_file]["error_expected"]:
                print("which NOT EXPECTED.")
            else:
                print("as expected.")
                if len(test_hub_map) == test_files[hub_map_file]["number_read"]:
                    print("The expected number of lines were processed.")
                else:
                    print("UNEXPECTED number of lines processed.")
                    print(test_hub_map)
        except:
            print("Error reading hub_map file " + hub_map_file,)
            if test_files[hub_map_file]["error_expected"]:
                print("as expected.")
            else:
                print("where error was NOT EXPECTED.")

    print("==============================================")
    print("Unit Under Test:  ConvertHubStringListToIDList")
    test_list = \
        {1: {"hub_names":['Smith']        ,"hub_ids":['9001']}, \
         2: {"hub_names":['Smits']        ,"hub_ids":['9001']}, \
         3: {"hub_names":['Smyth']        ,"hub_ids":['Smyth']},
         4: {"hub_names":['Smith','8th']  ,"hub_ids":['9001','9002']},
         5: {"hub_names":['Smith','Smyth'],"hub_ids":['9001','Smyth']}}
    test_hub_map = ReadHubMapFromFile ("hub_map_tools_tests/test_hub_map_general.csv")

    for test_case in test_list.keys():
        result = ConvertHubStringListToIDList \
                    (test_list[test_case]["hub_names"], test_hub_map)
        if result == test_list[test_case]["hub_ids"]:
            print("Test case %d successful." % test_case)
        else:
            print("Test case %d FAILED." % test_case)
            print("Actual Results:  ",)
            print(result)
            print("Expected Results:",)
            print(test_list[test_case]["hub_ids"])

if __name__ == '__main__':
    main()
