import unittest
from unittest.mock import patch
import os
import roster

data_file_path = os.path.abspath("./roster_tests/")

class UT_Init(unittest.TestCase):
    def test_01_do_not_show_errors(self):
        with patch('builtins.input', side_effect=[None]):
            result = roster.Roster()
        self.assertEqual(0, len(result.table))
        self.assertTrue(result.hideErrataOutput)
        self.assertEqual(1, len(result.errata))
        
    def test_02_show_errors_lower(self):
        with patch('builtins.input', side_effect=['y']):
            result = roster.Roster()
        self.assertEqual(0, len(result.table))
        self.assertFalse(result.hideErrataOutput)
        self.assertEqual(1, len(result.errata))
        
    def test_03_show_errors_upper(self):
        with patch('builtins.input', side_effect=['Y']):
            result = roster.Roster()
        self.assertEqual(0, len(result.table))
        self.assertFalse(result.hideErrataOutput)
        self.assertEqual(1, len(result.errata))
        
    def test_04_unknown_show_errors(self):
        with patch('builtins.input', side_effect=['x']):
            result = roster.Roster()
        self.assertEqual(0, len(result.table))
        self.assertTrue(result.hideErrataOutput)
        self.assertEqual(1, len(result.errata))

class UT_ApplyErrata(unittest.TestCase):
    def test_01_with_errata(self):
        with patch('builtins.input', side_effect=[None]):
            rosterC = roster.Roster()
        result = rosterC.ApplyErrata('Name With Error')
        self.assertEqual('Name Without Error', result)
        
    def test_02_no_errata(self):
        with patch('builtins.input', side_effect=[None]):
            rosterC = roster.Roster()
        result = rosterC.ApplyErrata('Just Fine Name')
        self.assertEqual('Just Fine Name', result)
        


if __name__ == '__main__':
    unittest.main()