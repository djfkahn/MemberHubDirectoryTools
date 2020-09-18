import unittest
from unittest.mock import patch
import os
import roster_tools
import hub_map_tools

data_file_path = os.path.abspath("./roster_tools_tests/")
hub_file_name  = data_file_path + "/hub_map.csv"
common_hub_map = hub_map_tools.ReadHubMapFromFile(hub_file_name)

class UT_01_ReadRosterFromFile(unittest.TestCase):
    def test_01_simple(self):
        roster_file_name = data_file_path + "/test_1_simple.xlsx"
        with patch('builtins.input', side_effect=[None]):
            result = roster_tools.ReadRosterFromFile(roster_file_name, common_hub_map)
        self.assertEqual(2, len(result))
        self.assertEqual(2, len(result[0].adults))
        self.assertEqual(1, len(result[0].children))
        self.assertEqual(2, len(result[1].adults))
        self.assertEqual(8, len(result[1].children))
        
    def test_02_four_fields(self):
        roster_file_name = data_file_path + "/test_2_four_fields.xlsx"
        with patch('builtins.input', side_effect=[None]):
            result = roster_tools.ReadRosterFromFile(roster_file_name, common_hub_map)
        self.assertEqual(0, len(result))

    def test_03_no_parents(self):
        roster_file_name = data_file_path + "/test_3_no_parents.xlsx"
        with patch('builtins.input', side_effect=[None]):
            result = roster_tools.ReadRosterFromFile(roster_file_name, common_hub_map)
        self.assertEqual(0, len(result))

    def test_04_no_teacher(self):
        roster_file_name = data_file_path + "/test_4_no_teacher.xlsx"
        with patch('builtins.input', side_effect=[None]):
            result = roster_tools.ReadRosterFromFile(roster_file_name, common_hub_map)
        self.assertEqual(0, len(result))

    def test_05_unknown_teacher(self):
        roster_file_name = data_file_path + "/test_5_unknown_teacher.xlsx"
        with patch('builtins.input', side_effect=[None]):
            result = roster_tools.ReadRosterFromFile(roster_file_name, common_hub_map)
        self.assertEqual(1, len(result))
        self.assertEqual(0, len(result[0].adults))
        self.assertEqual(0, len(result[0].children))

    def test_06_one_parent(self):
        roster_file_name = data_file_path + "/test_6_one_parent.xlsx"
        with patch('builtins.input', side_effect=[None]):
            result = roster_tools.ReadRosterFromFile(roster_file_name, common_hub_map)
        self.assertEqual(1, len(result))
        self.assertEqual(1, len(result[0].adults))
        self.assertEqual(1, len(result[0].children))

    def test_07_parent_different_last_names(self):
        roster_file_name = data_file_path + "/test_7_parent_different_last_names.xlsx"
        with patch('builtins.input', side_effect=[None]):
            result = roster_tools.ReadRosterFromFile(roster_file_name, common_hub_map)
        self.assertEqual(1, len(result))
        self.assertEqual(2, len(result[0].adults))
        self.assertEqual(1, len(result[0].children))

    def test_08_parent_multiword_last_name(self):
        roster_file_name = data_file_path + "/test_8_parent_multiword_last_name.xlsx"
        with patch('builtins.input', side_effect=[None]):
            result = roster_tools.ReadRosterFromFile(roster_file_name, common_hub_map)
        self.assertEqual(1, len(result))
        self.assertEqual(2, len(result[0].adults))
        self.assertEqual(2, len(result[0].children))

    def test_09_student_multiword_last_name(self):
        roster_file_name = data_file_path + "/test_9_student_multiword_last_name.xlsx"
        with patch('builtins.input', side_effect=[None]):
            result = roster_tools.ReadRosterFromFile(roster_file_name, common_hub_map)
        self.assertEqual(1, len(result))
        self.assertEqual(2, len(result[0].adults))
        self.assertEqual(2, len(result[0].children))

    def test_10_duplicate_students(self):
        roster_file_name = data_file_path + "/test_10_duplicate_students.xlsx"
        with patch('builtins.input', side_effect=[None]):
            result = roster_tools.ReadRosterFromFile(roster_file_name, common_hub_map)
        self.assertEqual(1, len(result))
        self.assertEqual(2, len(result[0].adults))
        self.assertEqual(1, len(result[0].children))

    def test_11_extra_space_in_parents(self):
        roster_file_name = data_file_path + "/test_11_extra_space_in_parents.xlsx"
        with patch('builtins.input', side_effect=[None]):
            result = roster_tools.ReadRosterFromFile(roster_file_name, common_hub_map)
        self.assertEqual(1, len(result))
        self.assertEqual(2, len(result[0].adults))
        self.assertEqual(3, len(result[0].children))

class UT_02_ReadDirectory(unittest.TestCase):
    @patch('builtins.input', side_effect=[None, None])
    def test_01_use_default(self, mock_input):
        with patch('os.path.abspath', return_value=data_file_path):
            result = roster_tools.ReadRoster(common_hub_map)
        self.assertEqual(1, len(result))

    @patch('builtins.input', side_effect=['0', '1', None])
    def test_02_select_under_range(self, mock_input):
        with patch('os.path.abspath', return_value=data_file_path):
            result = roster_tools.ReadRoster(common_hub_map)
        self.assertEqual(1, len(result))

    @patch('builtins.input', side_effect=['12', None, None])
    def test_03_select_over_range(self, mock_input):
        with patch('os.path.abspath', return_value=data_file_path):
            result = roster_tools.ReadRoster(common_hub_map)
        self.assertEqual(1, len(result))

class UT_03_ReadRosterAdultsFromMostRecent(unittest.TestCase):
    def test_01_use_default(self):
        with patch('os.path.abspath', return_value=data_file_path):
            result = roster_tools.ReadRosterAdultsFromMostRecent()
        self.assertEqual(3, len(result))


if __name__ == '__main__':
    unittest.main()