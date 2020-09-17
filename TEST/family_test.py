import unittest
from unittest.mock import patch
import os
import family
import hub_map_tools
import roster
import person

data_file_path = os.path.abspath("./family_tests/")
hub_file_name  = data_file_path + "/hub_map.csv"
common_hub_map = hub_map_tools.ReadHubMapFromFile(hub_file_name)
with patch('builtins.input', side_effect=['y']):
    common_RosterC = roster.Roster()

class UT_01_AddAdultsFromCombinedField(unittest.TestCase):
    def test_01_two_parents(self):
        result = family.Family()
        result.AddAdultsFromCombinedField('Kinder, Jane', 'A and B C', common_hub_map, common_RosterC)
        self.assertEqual(2, len(result.adults))
        self.assertEqual('A', result.adults[0].first_name)
        self.assertEqual('C', result.adults[0].last_name)
        self.assertEqual(['0000'],result.adults[0].hubs)
        self.assertEqual('Adult',result.adults[0].family_relation)
        self.assertEqual('B', result.adults[1].first_name)
        self.assertEqual('C', result.adults[1].last_name)
        self.assertEqual(['0000'],result.adults[1].hubs)
        self.assertEqual('Adult2',result.adults[1].family_relation)
        self.assertEqual(0, len(result.children))

    def test_02_one_parent(self):
        result = family.Family()
        result.AddAdultsFromCombinedField('First, John', 'A C', common_hub_map, common_RosterC)
        self.assertEqual(1, len(result.adults))
        self.assertEqual('A', result.adults[0].first_name)
        self.assertEqual('C', result.adults[0].last_name)
        self.assertEqual(['1111'],result.adults[0].hubs)
        self.assertEqual('Adult',result.adults[0].family_relation)
        self.assertEqual(0, len(result.children))

class UT_02_CreateFromRoster(unittest.TestCase):
    def test_01_two_parents(self):
        result = family.Family()
        result.CreateFromRoster(child_first  = 'D',
                                child_last   = 'C',
                                grade        = '0',
                                adult_names  = 'A and B C',
                                teacher_name = 'Kinder, Jane',
                                hub_map      = common_hub_map,
                                rosterC      = common_RosterC)
        self.assertEqual(2, len(result.adults))
        self.assertEqual('A', result.adults[0].first_name)
        self.assertEqual('C', result.adults[0].last_name)
        self.assertEqual(['0000'],result.adults[0].hubs)
        self.assertEqual('Adult',result.adults[0].family_relation)
        self.assertEqual('B', result.adults[1].first_name)
        self.assertEqual('C', result.adults[1].last_name)
        self.assertEqual(['0000'],result.adults[1].hubs)
        self.assertEqual('Adult2',result.adults[1].family_relation)
        self.assertEqual(1, len(result.children))
        self.assertEqual('D', result.children[0].first_name)
        self.assertEqual('C', result.children[0].last_name)
        self.assertEqual(['0000'],result.children[0].hubs)
        self.assertEqual('Child1',result.children[0].family_relation)

    def test_02_one_parent(self):
        result = family.Family()
        result.CreateFromRoster(child_first  = 'D',
                                child_last   = 'C',
                                grade        = '0',
                                adult_names  = 'A C',
                                teacher_name = 'First, John',
                                hub_map      = common_hub_map,
                                rosterC      = common_RosterC)
        self.assertEqual(1, len(result.adults))
        self.assertEqual('A', result.adults[0].first_name)
        self.assertEqual('C', result.adults[0].last_name)
        self.assertEqual(['1111'],result.adults[0].hubs)
        self.assertEqual('Adult',result.adults[0].family_relation)
        self.assertEqual(1, len(result.children))
        self.assertEqual('D', result.children[0].first_name)
        self.assertEqual('C', result.children[0].last_name)
        self.assertEqual(['1111'],result.children[0].hubs)
        self.assertEqual('Child1',result.children[0].family_relation)

    def test_03_6th_grader(self):
        result = family.Family()
        result.CreateFromRoster(child_first  = 'D',
                                child_last   = 'C',
                                grade        = '6',
                                adult_names  = 'A C',
                                teacher_name = 'First, John',
                                hub_map      = common_hub_map,
                                rosterC      = common_RosterC)
        self.assertEqual(1, len(result.adults))
        self.assertEqual('A', result.adults[0].first_name)
        self.assertEqual('C', result.adults[0].last_name)
        self.assertEqual(['6666'],result.adults[0].hubs)
        self.assertEqual('Adult',result.adults[0].family_relation)
        self.assertEqual(1, len(result.children))
        self.assertEqual('D', result.children[0].first_name)
        self.assertEqual('C', result.children[0].last_name)
        self.assertEqual(['6666'],result.children[0].hubs)
        self.assertEqual('Child1',result.children[0].family_relation)

    def test_04_8th_grader(self):
        result = family.Family()
        result.CreateFromRoster(child_first  = 'D',
                                child_last   = 'C',
                                grade        = '8',
                                adult_names  = 'A C',
                                teacher_name = 'First, John',
                                hub_map      = common_hub_map,
                                rosterC      = common_RosterC)
        self.assertEqual(1, len(result.adults))
        self.assertEqual('A', result.adults[0].first_name)
        self.assertEqual('C', result.adults[0].last_name)
        self.assertEqual(['8888'],result.adults[0].hubs)
        self.assertEqual('Adult',result.adults[0].family_relation)
        self.assertEqual(1, len(result.children))
        self.assertEqual('D', result.children[0].first_name)
        self.assertEqual('C', result.children[0].last_name)
        self.assertEqual(['8888'],result.children[0].hubs)
        self.assertEqual('Child1',result.children[0].family_relation)

    def test_05_9th_grader(self):
        result = family.Family()
        result.CreateFromRoster(child_first  = 'D',
                                child_last   = 'C',
                                grade        = '9',
                                adult_names  = 'A C',
                                teacher_name = 'First, John',
                                hub_map      = common_hub_map,
                                rosterC      = common_RosterC)
        self.assertEqual(0, len(result.adults))
        self.assertEqual(0, len(result.children))

    def test_06_Unknown_Teacher(self):
        result = family.Family()
        result.CreateFromRoster(child_first  = 'D',
                                child_last   = 'C',
                                grade        = '5',
                                adult_names  = 'A C',
                                teacher_name = 'Unknown Teacher',
                                hub_map      = common_hub_map,
                                rosterC      = common_RosterC)
        self.assertEqual(0, len(result.adults))
        self.assertEqual(0, len(result.children))

class UT_03_AddFromDirectory(unittest.TestCase):
    def test_01_adult_input(self):
        result = family.Family()
        result.AddFromDirectory(person_id       = '1234',
                                last_name       = 'C',
                                first_name      = 'A',
                                middle_name     = '',
                                suffix          = '',
                                email           = 'email',
                                family_id       = '5678',
                                family_relation = 'Adult',
                                hub_name_list   = 'Kinder (Room 0)'.split(';'),
                                account_created = '',
                                account_updated = '',
                                hub_map         = common_hub_map)
        self.assertEqual(1, len(result.adults))
        self.assertEqual('A', result.adults[0].first_name)
        self.assertEqual('C', result.adults[0].last_name)
        self.assertEqual('1234', result.adults[0].person_id)
        self.assertEqual('5678', result.adults[0].family_id)
        self.assertEqual('Adult',result.adults[0].family_relation)
        self.assertEqual('email',result.adults[0].email)
        self.assertEqual(['0000'],result.adults[0].hubs)
        self.assertEqual(0, len(result.children))

    def test_02_child_input(self):
        result = family.Family()
        result.AddFromDirectory(person_id       = '1234',
                                last_name       = 'C',
                                first_name      = 'A',
                                middle_name     = '',
                                suffix          = '',
                                email           = 'email',
                                family_id       = '5678',
                                family_relation = 'Child',
                                hub_name_list   = 'Kinder (Room 0)'.split(';'),
                                account_created = '',
                                account_updated = '',
                                hub_map         = common_hub_map)
        self.assertEqual(0, len(result.adults))
        self.assertEqual(1, len(result.children))

    def test_03_adult_lower_input(self):
        result = family.Family()
        result.AddFromDirectory(person_id       = '1234',
                                last_name       = 'C',
                                first_name      = 'A',
                                middle_name     = '',
                                suffix          = '',
                                email           = 'email',
                                family_id       = '5678',
                                family_relation = 'adult',
                                hub_name_list   = 'Kinder (Room 0)'.split(';'),
                                account_created = '',
                                account_updated = '',
                                hub_map         = common_hub_map)
        self.assertEqual(1, len(result.adults))
        self.assertEqual(0, len(result.children))

    def test_04_child_lower_input(self):
        result = family.Family()
        result.AddFromDirectory(person_id       = '1234',
                                last_name       = 'C',
                                first_name      = 'A',
                                middle_name     = '',
                                suffix          = '',
                                email           = 'email',
                                family_id       = '5678',
                                family_relation = 'child',
                                hub_name_list   = 'Kinder (Room 0)'.split(';'),
                                account_created = '',
                                account_updated = '',
                                hub_map         = common_hub_map)
        self.assertEqual(0, len(result.adults))
        self.assertEqual(1, len(result.children))

    def test_05_other_input(self):
        result = family.Family()
        result.AddFromDirectory(person_id       = '1234',
                                last_name       = 'C',
                                first_name      = 'A',
                                middle_name     = '',
                                suffix          = '',
                                email           = 'email',
                                family_id       = '5678',
                                family_relation = 'Other',
                                hub_name_list   = 'Kinder (Room 0)'.split(';'),
                                account_created = '',
                                account_updated = '',
                                hub_map         = common_hub_map)
        self.assertEqual(0, len(result.adults))
        self.assertEqual(0, len(result.children))

class UT_04_IsSameFamily(unittest.TestCase):
    def test_01_same_family(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        that = family.Family()
        that.CreateFromRoster(child_first  = 'D',
                              child_last   = 'C',
                              grade        = '0',
                              adult_names  = 'A C',
                              teacher_name = 'Kinder, Jane',
                              hub_map      = common_hub_map,
                              rosterC      = common_RosterC)
        self.assertTrue(this.IsSameFamily(that))

    def test_02_same_adult_different_child(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        that = family.Family()
        that.CreateFromRoster(child_first  = 'E',
                              child_last   = 'C',
                              grade        = '0',
                              adult_names  = 'A C',
                              teacher_name = 'Kinder, Jane',
                              hub_map      = common_hub_map,
                              rosterC      = common_RosterC)
        self.assertTrue(this.IsSameFamily(that))

    def test_03_directory_orphan(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        that = family.Family()
        that.CreateFromRoster(child_first  = 'E',
                              child_last   = 'C',
                              grade        = '0',
                              adult_names  = 'A C',
                              teacher_name = 'Kinder, Jane',
                              hub_map      = common_hub_map,
                              rosterC      = common_RosterC)
        self.assertFalse(this.IsSameFamily(that))

    def test_04_roster_orphan(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        that = family.Family()
        that.CreateFromRoster(child_first  = 'E',
                              child_last   = 'C',
                              grade        = '0',
                              adult_names  = ' ',
                              teacher_name = 'Kinder, Jane',
                              hub_map      = common_hub_map,
                              rosterC      = common_RosterC)
        self.assertFalse(this.IsSameFamily(that))

    def test_05_different_adult_same_child(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        that = family.Family()
        that.CreateFromRoster(child_first  = 'D',
                              child_last   = 'C',
                              grade        = '0',
                              adult_names  = 'E C',
                              teacher_name = 'Kinder, Jane',
                              hub_map      = common_hub_map,
                              rosterC      = common_RosterC)
        self.assertFalse(this.IsSameFamily(that))

    def test_06_more_adults_in_directory(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1236',
                              last_name       = 'C',
                              first_name      = 'B',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        that = family.Family()
        that.CreateFromRoster(child_first  = 'D',
                              child_last   = 'C',
                              grade        = '0',
                              adult_names  = 'A C',
                              teacher_name = 'Kinder, Jane',
                              hub_map      = common_hub_map,
                              rosterC      = common_RosterC)
        self.assertTrue(this.IsSameFamily(that))

    def test_07_more_adults_in_roster(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        that = family.Family()
        that.CreateFromRoster(child_first  = 'D',
                              child_last   = 'C',
                              grade        = '0',
                              adult_names  = 'A C',
                              teacher_name = 'Kinder, Jane',
                              hub_map      = common_hub_map,
                              rosterC      = common_RosterC)
        self.assertTrue(this.IsSameFamily(that))

class UT_05_HasNewChildren(unittest.TestCase):
    def test_01_same_family(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        that = family.Family()
        that.CreateFromRoster(child_first  = 'D',
                              child_last   = 'C',
                              grade        = '0',
                              adult_names  = 'A C',
                              teacher_name = 'Kinder, Jane',
                              hub_map      = common_hub_map,
                              rosterC      = common_RosterC)
        self.assertFalse(this.HasNewChildren(that))

    def test_02_same_adult_different_child(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        that = family.Family()
        that.CreateFromRoster(child_first  = 'E',
                              child_last   = 'C',
                              grade        = '0',
                              adult_names  = 'A C',
                              teacher_name = 'Kinder, Jane',
                              hub_map      = common_hub_map,
                              rosterC      = common_RosterC)
        self.assertTrue(this.HasNewChildren(that))

    def test_03_directory_orphan(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        that = family.Family()
        that.CreateFromRoster(child_first  = 'E',
                              child_last   = 'C',
                              grade        = '0',
                              adult_names  = 'A C',
                              teacher_name = 'Kinder, Jane',
                              hub_map      = common_hub_map,
                              rosterC      = common_RosterC)
        self.assertTrue(this.HasNewChildren(that))

    def test_04_roster_orphan(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        that = family.Family()
        that.CreateFromRoster(child_first  = 'E',
                              child_last   = 'C',
                              grade        = '0',
                              adult_names  = 'A C',
                              teacher_name = 'Kinder, Jane',
                              hub_map      = common_hub_map,
                              rosterC      = common_RosterC)
        self.assertTrue(this.HasNewChildren(that))

    def test_05_different_adult_same_child(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        that = family.Family()
        that.CreateFromRoster(child_first  = 'D',
                              child_last   = 'C',
                              grade        = '0',
                              adult_names  = 'A C',
                              teacher_name = 'Kinder, Jane',
                              hub_map      = common_hub_map,
                              rosterC      = common_RosterC)
        self.assertFalse(this.HasNewChildren(that))

    def test_06_more_adults_in_directory(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1236',
                              last_name       = 'C',
                              first_name      = 'B',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        that = family.Family()
        that.CreateFromRoster(child_first  = 'D',
                              child_last   = 'C',
                              grade        = '0',
                              adult_names  = 'A C',
                              teacher_name = 'Kinder, Jane',
                              hub_map      = common_hub_map,
                              rosterC      = common_RosterC)
        self.assertFalse(this.HasNewChildren(that))

    def test_07_more_adults_in_roster(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        that = family.Family()
        that.CreateFromRoster(child_first  = 'D',
                              child_last   = 'C',
                              grade        = '0',
                              adult_names  = 'A C',
                              teacher_name = 'Kinder, Jane',
                              hub_map      = common_hub_map,
                              rosterC      = common_RosterC)
        self.assertFalse(this.HasNewChildren(that))

class UT_06_FormFamilyWithNewChildren(unittest.TestCase):
    def test_01_family_with_new_child(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        that = family.Family()
        that.CreateFromRoster(child_first  = 'E',
                              child_last   = 'C',
                              grade        = '0',
                              adult_names  = 'A C',
                              teacher_name = 'Kinder, Jane',
                              hub_map      = common_hub_map,
                              rosterC      = common_RosterC)
        result = family.Family()
        result.FormFamilyWithNewChildren(this, that)
        self.assertEqual(result.adults, this.adults)
        self.assertEqual(1,len(result.children))
        self.assertEqual('E',result.children[0].first_name)
        self.assertEqual('C',result.children[0].last_name)

    def test_02_family_without_new_child(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        that = family.Family()
        that.CreateFromRoster(child_first  = 'D',
                              child_last   = 'C',
                              grade        = '0',
                              adult_names  = 'A C',
                              teacher_name = 'Kinder, Jane',
                              hub_map      = common_hub_map,
                              rosterC      = common_RosterC)
        result = family.Family()
        result.FormFamilyWithNewChildren(this, that)
        self.assertEqual(result.adults, this.adults)
        self.assertEqual(0,len(result.children))

class UT_07_CombineWith(unittest.TestCase):
    def test_01_add_new_child(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        that = family.Family()
        that.CreateFromRoster(child_first  = 'E',
                              child_last   = 'C',
                              grade        = '0',
                              adult_names  = 'A C',
                              teacher_name = 'Kinder, Jane',
                              hub_map      = common_hub_map,
                              rosterC      = common_RosterC)
        this.CombineWith(that)
        self.assertEqual(2,len(this.children))
        self.assertEqual('D',this.children[0].first_name)
        self.assertEqual('C',this.children[0].last_name)
        self.assertEqual('E',this.children[1].first_name)
        self.assertEqual('C',this.children[1].last_name)

    def test_02_existing_child(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        that = family.Family()
        that.CreateFromRoster(child_first  = 'D',
                              child_last   = 'C',
                              grade        = '0',
                              adult_names  = 'A C',
                              teacher_name = 'Kinder, Jane',
                              hub_map      = common_hub_map,
                              rosterC      = common_RosterC)
        this.CombineWith(that)
        self.assertEqual(1,len(this.children))
        self.assertEqual('D',this.children[0].first_name)
        self.assertEqual('C',this.children[0].last_name)

    def test_03_different_family(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'B',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        that = family.Family()
        that.CreateFromRoster(child_first  = 'E',
                              child_last   = 'C',
                              grade        = '0',
                              adult_names  = 'A D',
                              teacher_name = 'Kinder, Jane',
                              hub_map      = common_hub_map,
                              rosterC      = common_RosterC)
        this.CombineWith(that)
        self.assertEqual(1,len(this.children))
        self.assertEqual('B',this.children[0].first_name)
        self.assertEqual('C',this.children[0].last_name)

class UT_08_IsChildless(unittest.TestCase):
    def test_01_parent_and_chlid(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        self.assertFalse(this.IsChildless())

    def test_02_parent_no_chlid(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        self.assertTrue(this.IsChildless())

    def test_03_teacher(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Teachers'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        self.assertFalse(this.IsChildless())

    def test_04_Staff(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Staff'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        self.assertFalse(this.IsChildless())

    def test_05_volunteer(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Volunteers'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        self.assertFalse(this.IsChildless())

class UT_09_IsOrphan(unittest.TestCase):
    def test_01_child_and_parent(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        self.assertFalse(this.IsOrphan())

    def test_02_child_no_parent(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        self.assertTrue(this.IsOrphan())

class UT_10_FindAdultInFamily(unittest.TestCase):
    def test_01_one_adult_one_match(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        to_find = person.RosterPerson()
        to_find.SetFromRoster('C', 'A', 'Kinder, Jane', 'Adult', common_hub_map)
        self.assertIsNotNone(this.FindAdultInFamily(to_find))

    def test_02_two_adult_one_match(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        to_find = person.RosterPerson()
        to_find.SetFromRoster('C', 'A', 'Kinder, Jane', 'Adult', common_hub_map)
        self.assertIsNotNone(this.FindAdultInFamily(to_find))

    def test_03_three_adult_one_match(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1236',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        to_find = person.RosterPerson()
        to_find.SetFromRoster('C', 'A', 'Kinder, Jane', 'Adult', common_hub_map)
        self.assertIsNotNone(this.FindAdultInFamily(to_find))

    def test_04_two_adult_no_match(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        to_find = person.RosterPerson()
        to_find.SetFromRoster('C', 'E', 'Kinder, Jane', 'Adult', common_hub_map)
        self.assertIsNone(this.FindAdultInFamily(to_find))

    def test_05_no_adult(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        to_find = person.RosterPerson()
        to_find.SetFromRoster('C', 'A', 'Kinder, Jane', 'Adult', common_hub_map)
        self.assertIsNone(this.FindAdultInFamily(to_find))

class UT_11_FindChildInFamily(unittest.TestCase):
    def test_01_one_child_one_match(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        to_find = person.RosterPerson()
        to_find.SetFromRoster('C', 'A', 'Kinder, Jane', 'Child', common_hub_map)
        self.assertIsNotNone(this.FindChildInFamily(to_find))

    def test_02_two_child_one_match(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'B',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        to_find = person.RosterPerson()
        to_find.SetFromRoster('C', 'A', 'Kinder, Jane', 'Child', common_hub_map)
        self.assertIsNotNone(this.FindChildInFamily(to_find))

    def test_03_three_child_one_match(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'B',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1236',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        to_find = person.RosterPerson()
        to_find.SetFromRoster('C', 'A', 'Kinder, Jane', 'Child', common_hub_map)
        self.assertIsNotNone(this.FindChildInFamily(to_find))

    def test_04_three_child_no_match(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'B',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1236',
                              last_name       = 'C',
                              first_name      = 'D',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Child',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        to_find = person.RosterPerson()
        to_find.SetFromRoster('C', 'E', 'Kinder, Jane', 'Child', common_hub_map)
        self.assertIsNone(this.FindChildInFamily(to_find))

    def test_05_no_child(self):
        this = family.Family()
        this.AddFromDirectory(person_id       = '1234',
                              last_name       = 'C',
                              first_name      = 'A',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        this.AddFromDirectory(person_id       = '1235',
                              last_name       = 'C',
                              first_name      = 'B',
                              middle_name     = '',
                              suffix          = '',
                              email           = 'email',
                              family_id       = '5678',
                              family_relation = 'Adult',
                              hub_name_list   = 'Kinder (Room 0)'.split(';'),
                              account_created = '',
                              account_updated = '',
                              hub_map         = common_hub_map)
        to_find = person.RosterPerson()
        to_find.SetFromRoster('C', 'A', 'Kinder, Jane', 'Child', common_hub_map)
        self.assertIsNone(this.FindChildInFamily(to_find))

if __name__ == '__main__':
    unittest.main()