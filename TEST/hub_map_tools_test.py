import unittest
import os
import hub_map_tools

data_file_path = os.path.abspath("./hub_map_tools_tests/")

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


if __name__ == '__main__':
    unittest.main()