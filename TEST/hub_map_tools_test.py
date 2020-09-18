import unittest
import os
import hub_map_tools

data_file_path = os.path.abspath("./hub_map_tools_tests/")
map_d = hub_map_tools.ReadHubMapFromFile(data_file_path+"/hub_map.csv")

class UT_ConvertHubStringListToIDList(unittest.TestCase):
    def test_1_one_name(self):
        result = hub_map_tools.ConvertHubStringListToIDList(["First, John"], map_d)
        self.assertEqual(["1111"], result)
        
    def test_2_two_names(self):
        result = hub_map_tools.ConvertHubStringListToIDList(["First, John", "First (Room 1)"], map_d)
        self.assertEqual(["1111", "1111"], result)

    def test_3_hub_not_found(self):
        result = hub_map_tools.ConvertHubStringListToIDList(["Bogus Name"], map_d)
        self.assertEqual(["Bogus Name"], result)

    def test_4_1_found_1_not(self):
        result = hub_map_tools.ConvertHubStringListToIDList(["First, John", "Bogus Name"], map_d)
        self.assertEqual(["1111", "Bogus Name"], result)


class UT_ReadRosterFromFile(unittest.TestCase):
    def test_1_simple(self):
        file_name = data_file_path + "/test_1_simple.csv"
        result = hub_map_tools.ReadHubMapFromFile(file_name)
        self.assertEqual(3, len(result))
        
    def test_2_1_field(self):
        file_name = data_file_path + "/test_2_1_field.csv"
        result = hub_map_tools.ReadHubMapFromFile(file_name)
        self.assertEqual(2, len(result))

    def test_3_duplicate(self):
        file_name = data_file_path + "/test_3_duplicate.csv"
        result = hub_map_tools.ReadHubMapFromFile(file_name)
        self.assertEqual(2, len(result))

class UT_IsInClassroomHub(unittest.TestCase):
    def test_1_ID_is_classroom_hub(self):
        for value in map_d.values():
            self.assertTrue(hub_map_tools.IsInClassroomHub(map_d, value))

    def test_2_ID_is_special_case(self):
        self.assertTrue(hub_map_tools.IsInClassroomHub(map_d, "Teachers"))
        self.assertTrue(hub_map_tools.IsInClassroomHub(map_d, "Staff"))
        self.assertTrue(hub_map_tools.IsInClassroomHub(map_d, "Volunteers"))

    def test_3_ID_is_not_classroom_hub(self):
        self.assertFalse(hub_map_tools.IsInClassroomHub(map_d, "Bogus"))

    def test_4_ID_is_empty_string(self):
        self.assertFalse(hub_map_tools.IsInClassroomHub(map_d, ""))

    def test_5_ID_is_None(self):
        self.assertFalse(hub_map_tools.IsInClassroomHub(map_d, None))

class UT_IsAnyHubClassroomHub(unittest.TestCase):
    def test_1_one_hub_is_classroom(self):
        self.assertTrue(hub_map_tools.IsAnyHubClassroomHub(map_d, ['1111']))

    def test_2_one_hub_isnot_classroom(self):
        self.assertFalse(hub_map_tools.IsAnyHubClassroomHub(map_d, ['Bogus']))

    def test_3_three_hubs_all_classroom(self):
        self.assertTrue(hub_map_tools.IsAnyHubClassroomHub(map_d, ['0000', '1111', '2222']))

    def test_4_three_hubs_one_is_classroom(self):
        self.assertTrue(hub_map_tools.IsAnyHubClassroomHub(map_d, ['1111', 'Bogus', 'Really Bogus']))
        self.assertTrue(hub_map_tools.IsAnyHubClassroomHub(map_d, ['Bogus', '1111', 'Really Bogus']))
        self.assertTrue(hub_map_tools.IsAnyHubClassroomHub(map_d, ['Bogus', 'Really Bogus', '1111']))

    def test_5_three_hubs_none_classroom(self):
        self.assertFalse(hub_map_tools.IsAnyHubClassroomHub(map_d, ['Bogus', 'Really Bogus', 'Really Really Bogus']))


class UT_IsInMultipleClassroomHubs(unittest.TestCase):
    def test_1_one_hub_is_classroom(self):
        self.assertFalse(hub_map_tools.IsInMultipleClassroomHubs(map_d, ['1111']))

    def test_2_one_hub_isnot_classroom(self):
        self.assertFalse(hub_map_tools.IsInMultipleClassroomHubs(map_d, ['Bogus']))

    def test_3_two_hubs_all_classroom(self):
        self.assertTrue(hub_map_tools.IsInMultipleClassroomHubs(map_d, ['0000', '1111']))

    def test_4_three_hubs_all_classroom(self):
        self.assertTrue(hub_map_tools.IsInMultipleClassroomHubs(map_d, ['0000', '1111', '2222']))

    def test_5_three_hubs_two_classroom(self):
        self.assertTrue(hub_map_tools.IsInMultipleClassroomHubs(map_d, ['1111', '2222', 'Bogus']))
        self.assertTrue(hub_map_tools.IsInMultipleClassroomHubs(map_d, ['Bogus', '1111', '2222']))
        self.assertTrue(hub_map_tools.IsInMultipleClassroomHubs(map_d, ['2222', 'Bogus', '1111']))

    def test_6_three_hubs_none_classroom(self):
        self.assertFalse(hub_map_tools.IsInMultipleClassroomHubs(map_d, ['Bogus', 'Really Bogus', 'Really Really Bogus']))

class UT_CreateEmptyHubDictionary(unittest.TestCase):
    def test_1_one_hub_in_map(self):
        input_map = {'Name 1': '11'}
        self.assertEqual({'11':[]},
                         hub_map_tools.CreateEmptyHubDictionary(input_map))
        
    def test_2_two_hubs_in_map(self):
        input_map = {'Name 1': '11',
                     'Name 2': '22'}
        self.assertEqual({'11':[], '22':[]},
                         hub_map_tools.CreateEmptyHubDictionary(input_map))
        
    def test_3_three_hubs_in_map(self):
        input_map = {'Name 1': '11',
                     'Name 2': '22',
                     'Name 3': '33'}
        self.assertEqual({'11':[], '22':[], '33':[]},
                         hub_map_tools.CreateEmptyHubDictionary(input_map))
        
    def test_4_three_hubs_with_dups(self):
        input_map = {'Name 1': '11',
                     'Name 2': '22',
                     'Name 3': '11'}
        self.assertEqual({'11':[], '22':[]},
                         hub_map_tools.CreateEmptyHubDictionary(input_map))
        
    def test_5_three_hubs_all_dups(self):
        input_map = {'Name 1': '11',
                     'Name 2': '11',
                     'Name 3': '11'}
        self.assertEqual({'11':[]},
                         hub_map_tools.CreateEmptyHubDictionary(input_map))
        
        

if __name__ == '__main__':
    unittest.main()