import unittest
import os
import hub_map_tools
import person

data_file_path = os.path.abspath("./roster_tools_tests/")
hub_file_name  = data_file_path + "/hub_map.csv"
common_hub_map = hub_map_tools.ReadHubMapFromFile(hub_file_name)

class UT_Set(unittest.TestCase):
    def test_01_valid_adult(self):
        result = person.Person()
        self.assertTrue(result.Set(last_name='A', first_name='B', family_relation='Adult', hub_name_list=[], hub_map=common_hub_map))
        self.assertEqual('A'    , result.last_name)
        self.assertEqual('B'    , result.first_name)
        self.assertEqual('Adult', result.family_relation)
        self.assertEqual([]     , result.hubs)
        
    def test_02_valid_child(self):
        result = person.Person()
        self.assertTrue(result.Set(last_name='A', first_name='B', family_relation='Child', hub_name_list=[], hub_map=common_hub_map))
        self.assertEqual('A'    , result.last_name)
        self.assertEqual('B'    , result.first_name)
        self.assertEqual('Child', result.family_relation)
        self.assertEqual([]     , result.hubs)
        
    def test_03_invalid_adult(self):
        result = person.Person()
        self.assertFalse(result.Set(last_name=None, first_name='B', family_relation='Child', hub_name_list=[], hub_map=common_hub_map))
        self.assertEqual(None, result.last_name)
        self.assertEqual(None, result.first_name)
        self.assertEqual(None, result.family_relation)
        self.assertEqual([]     , result.hubs)
        
    def test_04_invalid_child(self):
        result = person.Person()
        self.assertFalse(result.Set(last_name='A', first_name=None, family_relation='Child', hub_name_list=[], hub_map=common_hub_map))
        self.assertEqual(None, result.last_name)
        self.assertEqual(None, result.first_name)
        self.assertEqual(None, result.family_relation)
        self.assertEqual([]     , result.hubs)
        
    def test_05_unknown_relation(self):
        result = person.Person()
        self.assertFalse(result.Set(last_name='A', first_name='B', family_relation=None, hub_name_list=[], hub_map=common_hub_map))
        self.assertEqual(None, result.last_name)
        self.assertEqual(None, result.first_name)
        self.assertEqual(None, result.family_relation)
        self.assertEqual([]     , result.hubs)
        
class UT_IsSame(unittest.TestCase):
    def test_01_same_person(self):
        person_A = person.Person()
        temp     = person_A.Set(last_name='A', first_name='B', family_relation='Adult', hub_name_list=[], hub_map=common_hub_map)
        self.assertTrue(person_A.IsSame(person_A))

    def test_02_different_first_name(self):
        person_A = person.Person()
        temp     = person_A.Set(last_name='Z', first_name='A', family_relation='Adult', hub_name_list=[], hub_map=common_hub_map)
        person_B = person.Person()
        temp     = person_B.Set(last_name='Z', first_name='B', family_relation='Adult', hub_name_list=[], hub_map=common_hub_map)
        self.assertFalse(person_A.IsSame(person_B))

    def test_03_different_last_name(self):
        person_A = person.Person()
        temp     = person_A.Set(last_name='Z', first_name='A', family_relation='Adult', hub_name_list=[], hub_map=common_hub_map)
        person_B = person.Person()
        temp     = person_B.Set(last_name='Y', first_name='A', family_relation='Adult', hub_name_list=[], hub_map=common_hub_map)
        self.assertFalse(person_A.IsSame(person_B))

    def test_04_different_relation(self):
        person_A = person.Person()
        temp     = person_A.Set(last_name='Z', first_name='A', family_relation='Adult', hub_name_list=[], hub_map=common_hub_map)
        person_B = person.Person()
        temp     = person_B.Set(last_name='Z', first_name='A', family_relation='Child', hub_name_list=[], hub_map=common_hub_map)
        self.assertFalse(person_A.IsSame(person_B))

    def test_05_different_hub(self):
        person_A = person.Person()
        temp     = person_A.Set(last_name='Z', first_name='A', family_relation='Adult', hub_name_list=['First, John'], hub_map=common_hub_map)
        person_B = person.Person()
        temp     = person_B.Set(last_name='Z', first_name='A', family_relation='Adult', hub_name_list=['Second, Jane'], hub_map=common_hub_map)
        self.assertFalse(person_A.IsSame(person_B))

    def test_06_same_and_more_hub_adult(self):
        person_A = person.Person()
        temp     = person_A.Set(last_name='Z', first_name='A', family_relation='Adult', hub_name_list=['First, John'], hub_map=common_hub_map)
        person_B = person.Person()
        temp     = person_B.Set(last_name='Z', first_name='A', family_relation='Adult', hub_name_list=['First, John'], hub_map=common_hub_map)
        person_B.hubs.append('2222')
        self.assertFalse(person_A.IsSame(person_B))

    def test_07_same_and_more_hub_child(self):
        person_A = person.Person()
        temp     = person_A.Set(last_name='Z', first_name='A', family_relation='Child', hub_name_list=['First, John'], hub_map=common_hub_map)
        person_B = person.Person()
        temp     = person_B.Set(last_name='Z', first_name='A', family_relation='Child', hub_name_list=['First, John'], hub_map=common_hub_map)
        person_B.hubs.append('2222')
        self.assertFalse(person_A.IsSame(person_B))

class UT_SetFromDirectory(unittest.TestCase):
    def test_01_set_adult(self):
        result = person.DirectoryPerson()
        self.assertIsNone(result.last_name)
        self.assertIsNone(result.first_name)
        self.assertIsNone(result.family_relation)
        self.assertEqual([], result.hubs)
        
        fields = ['1234','C','A','','','email','5678','Adult','','','','','','','','','','','','','','','0','','Kinder (Room 0)','all','','','','','']
        result.SetFromDirectory(fields, common_hub_map)
        self.assertEqual('A', result.first_name)
        self.assertEqual('C', result.last_name)
        self.assertEqual('1234', result.person_id)
        self.assertEqual('5678', result.family_id)
        self.assertEqual('Adult',result.family_relation)
        self.assertEqual('email',result.email)
        self.assertEqual(['0000'],result.hubs)

    def test_02_set_child(self):
        result = person.DirectoryPerson()
        fields = ['1234','C','A','','','email','5678','Child','','','','','','','','','','','','','','','0','','Kinder (Room 0)','all','','','','','']
        result.SetFromDirectory(fields, common_hub_map)
        self.assertEqual('A', result.first_name)
        self.assertEqual('C', result.last_name)
        self.assertEqual('1234', result.person_id)
        self.assertEqual('5678', result.family_id)
        self.assertEqual('Child',result.family_relation)
        self.assertEqual('email',result.email)
        self.assertEqual(['0000'],result.hubs)

    def test_03_set_no_first_name(self):
        result = person.DirectoryPerson()
        fields = ['1234','C','','','','email','5678','Child','','','','','','','','','','','','','','','0','','Kinder (Room 0)','all','','','','','']
        result.SetFromDirectory(fields, common_hub_map)
        self.assertIsNone(result.last_name)
        self.assertIsNone(result.first_name)
        self.assertIsNone(result.family_relation)
        self.assertEqual([], result.hubs)

    def test_04_set_no_last_name(self):
        result = person.DirectoryPerson()
        fields = ['1234','','A','','','email','5678','Child','','','','','','','','','','','','','','','0','','Kinder (Room 0)','all','','','','','']
        result.SetFromDirectory(fields, common_hub_map)
        self.assertIsNone(result.last_name)
        self.assertIsNone(result.first_name)
        self.assertIsNone(result.family_relation)
        self.assertEqual([], result.hubs)

    def test_05_set_no_relation(self):
        result = person.DirectoryPerson()
        fields = ['1234','C','A','','','email','5678','','','','','','','','','','','','','','','','0','','Kinder (Room 0)','all','','','','','']
        result.SetFromDirectory(fields, common_hub_map)
        self.assertIsNone(result.last_name)
        self.assertIsNone(result.first_name)
        self.assertIsNone(result.family_relation)
        self.assertEqual([], result.hubs)

    def test_06_set_other_relation(self):
        result = person.DirectoryPerson()
        fields = ['1234','C','','','','email','5678','Other','','','','','','','','','','','','','','','0','','Kinder (Room 0)','all','','','','','']
        result.SetFromDirectory(fields, common_hub_map)
        self.assertIsNone(result.last_name)
        self.assertIsNone(result.first_name)
        self.assertIsNone(result.family_relation)
        self.assertEqual([], result.hubs)

    def test_07_set_no_hubs(self):
        result = person.DirectoryPerson()
        fields = ['1234','C','A','','','email','5678','Child','','','','','','','','','','','','','','','0','','','all','','','','','']
        result.SetFromDirectory(fields, common_hub_map)
        self.assertEqual('A', result.first_name)
        self.assertEqual('C', result.last_name)
        self.assertEqual('1234', result.person_id)
        self.assertEqual('5678', result.family_id)
        self.assertEqual('Child',result.family_relation)
        self.assertEqual('email',result.email)
        self.assertEqual([],result.hubs)

    def test_02_set_multiple_hubs(self):
        result = person.DirectoryPerson()
        fields = ['1234','C','A','','','email','5678','Child','','','','','','','','','','','','','','','0','','Kinder (Room 0);First (Room 1)','all','','','','','']
        result.SetFromDirectory(fields, common_hub_map)
        self.assertEqual('A', result.first_name)
        self.assertEqual('C', result.last_name)
        self.assertEqual('1234', result.person_id)
        self.assertEqual('5678', result.family_id)
        self.assertEqual('Child',result.family_relation)
        self.assertEqual('email',result.email)
        self.assertEqual(['0000','1111'],result.hubs)


if __name__ == '__main__':
    unittest.main()