import unittest
from unittest.mock import patch
import os
import hub_map_tools
import roster

import name_parser

data_file_path = os.path.abspath("./name_parser_tests/")
hub_file_name  = data_file_path + "/hub_map.csv"
common_hub_map = hub_map_tools.ReadHubMapFromFile(hub_file_name)
with patch('builtins.input', side_effect=['y']):
    common_RosterC = roster.Roster()


class UT_ParseType1Name(unittest.TestCase):
    def test_01_simple_names(self):
        result = name_parser.ParseType1Name(['John', 'Jane Doe'])
        expect = [{'first' : 'John', 'last' : 'Doe'}, {'first' : 'Jane', 'last' : 'Doe'}]
        self.assertEqual(expect, result)

    def test_02_compound_name(self):
        result = name_parser.ParseType1Name(['John', 'Jane O Doe'])
        expect = [{'first' : 'John', 'last' : 'O Doe'}, {'first' : 'Jane', 'last' : 'O Doe'}]
        self.assertEqual(expect, result)

    def test_03_multi_word_last_name(self):
        result = name_parser.ParseType1Name(['John', 'Jane Smith Doe'])
        expect = [{'first' : 'John', 'last' : 'Doe'}, {'first' : 'Jane Smith', 'last' : 'Doe'}]
        self.assertEqual(expect, result)

    def test_04_hyphenated_last_name(self):
        result = name_parser.ParseType1Name(['John', 'Jane Smith-Doe'])
        expect = [{'first' : 'John', 'last' : 'Smith-Doe'}, {'first' : 'Jane Smith', 'last' : 'Smith-Doe'}]
        self.assertEqual(expect, result)

    def test_05_more_than_2_fields(self):
        result = name_parser.ParseType1Name(['John', 'Susan', 'Jane Doe'])
        expect = [{'first' : 'John', 'last' : 'Doe'}, {'first' : 'Susan', 'last' : 'Doe'}, {'first' : 'Jane Smith', 'last' : 'Doe'}]
        self.assertEqual(expect, result)


class UT_ParseType2Name(unittest.TestCase):
    def test_01_simple_name(self):
        result = name_parser.ParseType2Name(['John Smith', 'Jane Doe'])
        expect = [{'first' : 'John', 'last' : 'Smith'}, {'first' : 'Jane', 'last' : 'Doe'}]
        self.assertEqual(expect, result)

    def test_02_compound_name(self):
        result = name_parser.ParseType2Name(['John Smith', 'Jane Doe'])
        expect = [{'first' : 'John', 'last' : 'Smith'}, {'first' : 'Jane', 'last' : 'Doe'}]
        self.assertEqual(expect, result)

    def test_03_one_name(self):
        result = name_parser.ParseType2Name(['John Smith'])
        expect = [{'first' : 'John', 'last' : 'Smith'}]
        self.assertEqual(expect, result)

    def test_04_three_names(self):
        result = name_parser.ParseType2Name(['John Smith', 'Jane Doe', 'Something Else'])
        expect = [{'first' : 'John', 'last' : 'Smith'}, {'first' : 'Jane', 'last' : 'Doe'}, {'first' : 'Something', 'last' : 'Else'}]
        self.assertEqual(expect, result)


class UT_ParseType3Name(unittest.TestCase):
    def test_01_simple_name(self):
        result = name_parser.ParseType3Name('John Smith')
        expect = [{'first' : 'John', 'last' : 'Smith'}]
        self.assertEqual(expect, result)

    def test_02_compound_last_name(self):
        result = name_parser.ParseType3Name('John de Smith')
        expect = [{'first' : 'John', 'last' : 'De Smith'}]
        self.assertEqual(expect, result)

    def test_03_not_compound_last_name(self):
        result = name_parser.ParseType3Name('John Doe Smith')
        expect = [{'first' : 'John Doe', 'last' : 'Smith'}]
        self.assertEqual(expect, result)

    def test_04_hyphenated_last_name(self):
        result = name_parser.ParseType3Name('John Doe-Smith')
        expect = [{'first' : 'John', 'last' : 'Doe-Smith'}]
        self.assertEqual(expect, result)

    def test_05_extra_spaces(self):
        result = name_parser.ParseType3Name(' John  Smith ')
        expect = [{'first' : 'John', 'last' : 'Smith'}]
        self.assertEqual(expect, result)


class UT_IsCompoundLastName(unittest.TestCase):
    def test_01_is_compound_indicator(self):
        prefix_words = ('vere','von','van','de','del','della','di','da','d',\
                        'pietro','vanden','du','st.','st','la','ter','o')
        for this in prefix_words:
            self.assertTrue(name_parser.IsCompoundLastName(this))

    def test_02_not_compound_indicator(self):
        self.assertFalse(name_parser.IsCompoundLastName('smith'))


class UT_ParseFullName(unittest.TestCase):
    def test_01_same_last_name(self):
        result = name_parser.ParseFullName('John and Jane Doe', common_RosterC)
        expect = [{'first' : 'John', 'last' : 'Doe'}, {'first' : 'Jane', 'last' : 'Doe'}]
        self.assertEqual(expect, result)

    def test_02_different_last_name(self):
        result = name_parser.ParseFullName('John Smith and Jane Doe', common_RosterC)
        expect = [{'first' : 'John', 'last' : 'Smith'}, {'first' : 'Jane', 'last' : 'Doe'}]
        self.assertEqual(expect, result)

    def test_03_one_name(self):
        result = name_parser.ParseFullName('Jane Doe', common_RosterC)
        expect = [{'first' : 'Jane', 'last' : 'Doe'}]
        self.assertEqual(expect, result)

    def test_04_three_names(self):
        result = name_parser.ParseFullName('John Smith and Jane Doe and Someone Else', common_RosterC)
        expect = [{'first' : 'John', 'last' : 'Smith'}, {'first' : 'Jane', 'last' : 'Doe'}, {'first' : 'Someone', 'last' : 'Else'}]
        self.assertEqual(expect, result)

    def test_05_name_with_error(self):
        result = name_parser.ParseFullName('Name With Error', common_RosterC)
        expect = [{'first' : 'Name Without', 'last' : 'Error'}]
        self.assertEqual(expect, result)

    def test_06_multi_word_last_name(self):
        result = name_parser.ParseFullName('John and Jane Doe Smith', common_RosterC)
        expect = [{'first' : 'John', 'last' : 'Smith'}, {'first' : 'Jane Doe', 'last' : 'Smith'}]
        self.assertEqual(expect, result)

    def test_06_hyphenated_last_name(self):
        result = name_parser.ParseFullName('John and Jane Doe-Smith', common_RosterC)
        expect = [{'first' : 'John', 'last' : 'Doe-Smith'}, {'first' : 'Jane', 'last' : 'Doe-Smith'}]
        self.assertEqual(expect, result)

    def test_07_multi_word_first_name(self):
        result = name_parser.ParseFullName('Jon Claude and Jane van Damme', common_RosterC)
        expect = [{'first' : 'Jon Claude', 'last' : 'Van Damme'}, {'first' : 'Jane', 'last' : 'Van Damme'}]
        self.assertEqual(expect, result)

    def test_08_hyphenated_first_name(self):
        result = name_parser.ParseFullName('Jon-Claude and Jane van Damme', common_RosterC)
        expect = [{'first' : 'Jon-Claude', 'last' : 'Van Damme'}, {'first' : 'Jane', 'last' : 'Van Damme'}]
        self.assertEqual(expect, result)

    def test_09_extra_spaces(self):
        result = name_parser.ParseFullName(' John  and  Jane  Doe ', common_RosterC)
        expect = [{'first' : 'John', 'last' : 'Doe'}, {'first' : 'Jane', 'last' : 'Doe'}]
        self.assertEqual(expect, result)


if __name__ == '__main__':
    unittest.main()