import unittest
from unittest.mock import patch
import os
import directory_tools
import hub_map_tools

data_file_path = os.path.abspath("./directory_tools_tests/")
hub_file_name  = data_file_path + "/hub_map.csv"
common_hub_map = hub_map_tools.ReadHubMapFromFile(hub_file_name)

class UT_01_ReadDirectoryFromFile(unittest.TestCase):
    def test_1_general(self):
        file_name = data_file_path + "/test_1_general.csv"
        result = directory_tools.ReadDirectoryFromFile(file_name, common_hub_map)
        self.assertEqual(3, len(result))
        
    def test_2_too_few_fields(self):
        file_name = data_file_path + "/test_2_too_few_fields.csv"
        result = directory_tools.ReadDirectoryFromFile(file_name, common_hub_map)
        self.assertEqual(3, len(result))

    def test_2a_too_many_fields(self):
        file_name = data_file_path + "/test_2a_too_many_fields.csv"
        result = directory_tools.ReadDirectoryFromFile(file_name, common_hub_map)
        self.assertEqual(3, len(result))

    def test_3_no_family_relation(self):
        file_name = data_file_path + "/test_3_no_family_relation.csv"
        result = directory_tools.ReadDirectoryFromFile(file_name, common_hub_map)
        self.assertEqual(3, len(result))

    def test_4_no_first_name(self):
        file_name = data_file_path + "/test_4_no_first_name.csv"
        result = directory_tools.ReadDirectoryFromFile(file_name, common_hub_map)
        self.assertEqual(3, len(result))

    def test_5_no_last_name(self):
        file_name = data_file_path + "/test_5_no_last_name.csv"
        result = directory_tools.ReadDirectoryFromFile(file_name, common_hub_map)
        self.assertEqual(3, len(result))

    def test_6_no_person_id(self):
        file_name = data_file_path + "/test_6_no_person_id.csv"
        result = directory_tools.ReadDirectoryFromFile(file_name, common_hub_map)
        self.assertEqual(3, len(result))

    def test_7_adult_and_child_same_name(self):
        file_name = data_file_path + "/test_7_adult_and_child_same_name.csv"
        result = directory_tools.ReadDirectoryFromFile(file_name, common_hub_map)
        self.assertEqual(1, len(result))


class UT_02_ReadDirectory(unittest.TestCase):
    @patch('builtins.input', side_effect=[None])
    def test_01_use_default(self, mock_input):
        with patch('os.path.abspath', return_value=data_file_path):
            result = directory_tools.ReadDirectory(common_hub_map)
        self.assertEqual(1, len(result))

    @patch('builtins.input', side_effect=['0', '1'])
    def test_02_select_under_range(self, mock_input):
        with patch('os.path.abspath', return_value=data_file_path):
            result = directory_tools.ReadDirectory(common_hub_map)
        self.assertEqual(1, len(result))

    @patch('builtins.input', side_effect=['11', None])
    def test_03_select_over_range(self, mock_input):
        with patch('os.path.abspath', return_value=data_file_path):
            result = directory_tools.ReadDirectory(common_hub_map)
        self.assertEqual(1, len(result))

def Run():
    unittest.main()

if __name__ == '__main__':
    unittest.main()