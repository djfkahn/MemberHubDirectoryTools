import unittest
import os
import roster_tools
import hub_map_tools

data_file_path = os.path.abspath("./roster_tools_tests/")
hub_file_name  = data_file_path + "/hub_map.csv"
common_hub_map = hub_map_tools.ReadHubMapFromFile(hub_file_name)

class UT_ReadRosterFromFile(unittest.TestCase):
    def test_1_simple(self):
        roster_file_name = data_file_path + "/test_1_simple.xlsx"
        result = roster_tools.ReadRosterFromFile(roster_file_name, common_hub_map)
        self.assertEqual(2, len(result))
        
    def test_2_four_fields(self):
        roster_file_name = data_file_path + "/test_2_four_fields.xlsx"
        result = roster_tools.ReadRosterFromFile(roster_file_name, common_hub_map)
        self.assertEqual(0, len(result))

    def test_3_no_parents(self):
        roster_file_name = data_file_path + "/test_3_no_parents.xlsx"
        result = roster_tools.ReadRosterFromFile(roster_file_name, common_hub_map)
        self.assertEqual(0, len(result))

    def test_4_no_teacher(self):
        roster_file_name = data_file_path + "/test_4_no_teacher.xlsx"
        result = roster_tools.ReadRosterFromFile(roster_file_name, common_hub_map)
        self.assertEqual(0, len(result))



if __name__ == '__main__':
    unittest.main()