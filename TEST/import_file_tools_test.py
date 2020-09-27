import unittest
from unittest.mock import patch, mock_open, call
from unittest.mock import Mock
import os
import person
import family
import roster
import time

##
## Unit Under Test:
import import_file_tools


with patch('builtins.input', side_effect=['y']):
    common_RosterC = roster.Roster()

class UT_01_FormTimeTag(unittest.TestCase):

    @patch('import_file_tools.localtime')
    def test_01_simple(self, mock_localtime):
        datetime_str = '2020-01-01-00-00-00'
        mock_localtime.return_value = time.strptime(datetime_str,"%Y-%m-%d-%H-%M-%S")
        self.assertEqual(datetime_str, import_file_tools.FormTimeTag())


    @patch('import_file_tools.localtime')
    def test_02_future_date(self, mock_localtime):
        datetime_str = '2040-01-01-00-00-00'
        mock_localtime.return_value = time.strptime(datetime_str,"%Y-%m-%d-%H-%M-%S")
        self.assertEqual(datetime_str, import_file_tools.FormTimeTag())


    @patch('import_file_tools.localtime')
    def test_03_past_date(self, mock_localtime):
        datetime_str = '1800-01-01-00-00-00'
        mock_localtime.return_value = time.strptime(datetime_str,"%Y-%m-%d-%H-%M-%S")
        self.assertEqual(datetime_str, import_file_tools.FormTimeTag())




class UT_03_WriteNewMemberPerson(unittest.TestCase):
    def test_01_valid_roster_person(self):
        test_person = person.RosterPerson(last_name       ='B',
                                          first_name      ='A',
                                          family_relation ='Adult',
                                          teacher         ='',
                                          hub_map         ={})
        mocker = mock_open()
        with patch('builtins.open', mocker):
            with open('testfile', 'w') as open_file:
                import_file_tools.WriteNewMemberPerson(open_file  = open_file,
                                                       new_person = test_person)
                handle = mocker()
                write_calls = [call('Adult'), call(',A'), call(',B'), call(','), call('\n')]
                handle.write.assert_has_calls(calls=write_calls, any_order=False)


    def test_02_empty_roster_person(self):
        test_person = person.RosterPerson(last_name       ='',
                                          first_name      ='',
                                          family_relation ='',
                                          teacher         ='',
                                          hub_map         ={})
        mocker = mock_open()
        with patch('builtins.open', mocker):
            with open('testfile', 'w') as open_file:
                import_file_tools.WriteNewMemberPerson(open_file  = open_file,
                                                       new_person = test_person)
                handle = mocker()
                write_calls = [call('None'), call(',None'), call(',None'), call(','), call('\n')]
                handle.write.assert_has_calls(calls=write_calls, any_order=False)


    def test_03_null_roster_person(self):
        test_person = person.RosterPerson(last_name       =None,
                                          first_name      =None,
                                          family_relation =None,
                                          teacher         =None,
                                          hub_map         ={})
        mocker = mock_open()
        with patch('builtins.open', mocker):
            with open('testfile', 'w') as open_file:
                import_file_tools.WriteNewMemberPerson(open_file  = open_file,
                                                       new_person = test_person)
                handle = mocker()
                write_calls = [call('None'), call(',None'), call(',None'), call(','), call('\n')]
                handle.write.assert_has_calls(calls=write_calls, any_order=False)


    def test_04_valid_directory_person(self):
        test_person = person.DirectoryPerson(last_name       ='B',
                                             first_name      ='A',
                                             family_relation ='Adult',
                                             hub_name_list   =['Foo'],
                                             hub_map         ={'Foo':'1111'},
                                             person_id       ='1111')
        mocker = mock_open()
        with patch('builtins.open', mocker):
            with open('testfile', 'w') as open_file:
                import_file_tools.WriteNewMemberPerson(open_file  = open_file,
                                                       new_person = test_person)
                handle = mocker()
                write_calls = [call('Adult'), call(',A'), call(',B'), call(',1111'), call('\n')]
                handle.write.assert_has_calls(calls=write_calls, any_order=False)


    def test_05_empty_directory_person(self):
        test_person = person.DirectoryPerson(last_name       ='',
                                             first_name      ='',
                                             family_relation ='',
                                             hub_name_list   =[],
                                             hub_map         ={},
                                             person_id       ='')
        mocker = mock_open()
        with patch('builtins.open', mocker):
            with open('testfile', 'w') as open_file:
                import_file_tools.WriteNewMemberPerson(open_file  = open_file,
                                                       new_person = test_person)
                handle = mocker()
                write_calls = [call('None'), call(',None'), call(',None'), call(','), call('\n')]
                handle.write.assert_has_calls(calls=write_calls, any_order=False)


    def test_06_null_directory_person(self):
        test_person = person.DirectoryPerson(last_name       =None,
                                             first_name      =None,
                                             family_relation =None,
                                             hub_name_list   =[],
                                             hub_map         ={},
                                             person_id       =None)
        mocker = mock_open()
        with patch('builtins.open', mocker):
            with open('testfile', 'w') as open_file:
                import_file_tools.WriteNewMemberPerson(open_file  = open_file,
                                                       new_person = test_person)
                handle = mocker()
                write_calls = [call('None'), call(',None'), call(',None'), call(',None'), call('\n')]
                handle.write.assert_has_calls(calls=write_calls, any_order=False)



class UT_04_CreateHubImportFile(unittest.TestCase):
    @patch('import_file_tools.localtime')
    def test_01_1_valid_people(self, mock_localtime):
        test_people = [person.DirectoryPerson(last_name       ='B',
                                              first_name      ='A',
                                              family_relation ='Adult',
                                              hub_name_list   =['Foo'],
                                              hub_map         ={'Foo':'1111'},
                                              person_id       ='1234')]
        mock_localtime.return_value = time.strptime('2020-01-01-00-00-00',"%Y-%m-%d-%H-%M-%S")
        mocker = mock_open()
        with patch('builtins.open', mocker):
            import_file_tools.CreateFileFromPeople(people      = test_people,
                                                   file_prefix = 'test')
            mocker.assert_called_with(os.path.abspath('.')+'/test_2020-01-01-00-00-00.csv','w')
            handle = mocker()
            write_calls = [call('First Name'), call(',Last Name'), call(',Affiliated Hub(s)'), call(',Email'), call('\n'),
                           call('A'), call(',B'), call(',[\'1111\']'), call(',None'), call('\n')]
            handle.write.assert_has_calls(calls=write_calls, any_order=False)


    @patch('import_file_tools.localtime')
    def test_02_2_valid_people(self, mock_localtime):
        test_people = [person.DirectoryPerson(last_name       ='B',
                                              first_name      ='A',
                                              family_relation ='Adult',
                                              hub_name_list   =['Foo'],
                                              hub_map         ={'Foo':'1111'},
                                              email           ='a@b.c',
                                              person_id       ='1234'),
                       person.DirectoryPerson(last_name       ='D',
                                              first_name      ='C',
                                              family_relation ='Child',
                                              hub_name_list   =['Foo'],
                                              hub_map         ={'Foo':'1111'},
                                              person_id       ='2345')]
        mock_localtime.return_value = time.strptime('2020-01-01-00-00-00',"%Y-%m-%d-%H-%M-%S")
        mocker = mock_open()
        with patch('builtins.open', mocker):
            import_file_tools.CreateFileFromPeople(people      = test_people,
                                                   file_prefix = 'test')
            mocker.assert_called_with(os.path.abspath('.')+'/test_2020-01-01-00-00-00.csv','w')
            handle = mocker()
            write_calls = [call('First Name'), call(',Last Name'), call(',Affiliated Hub(s)'), call(',Email'), call('\n'),
                           call('A'), call(',B'), call(',[\'1111\']'), call(',a@b.c'), call('\n'),
                           call('C'), call(',D'), call(',[\'1111\']'), call(',None'), call('\n')]
            handle.write.assert_has_calls(calls=write_calls, any_order=False)



class UT_05_CreateNewMemberImport(unittest.TestCase):
    @patch('import_file_tools.localtime')
    def test_01_1_valid_family(self, mock_localtime):
        test_family = family.RosterFamily('A B')
        test_family.AddToFamily(child_first  = 'C',
                                child_last   = 'B',
                                grade        = '1',
                                adult_names  = 'A B',
                                teacher_name = 'Foo',
                                hub_map      = {'Foo':'1111'},
                                rosterC      = common_RosterC)
        mock_localtime.return_value = time.strptime('2020-01-01-00-00-00',"%Y-%m-%d-%H-%M-%S")
        mocker = mock_open()
        with patch('builtins.open', mocker):
            import_file_tools.CreateFileFromFamily(entriless = [test_family])
            mocker.assert_called_with(os.path.abspath('.')+'/new_member_import_2020-01-01-00-00-00.csv','w')
            handle = mocker()
            write_calls = [call('family_relation'), call(',first_name'), call(',last_name'), call(',person_id'), call('\n'),
                           call('Adult'), call(',A'), call(',B'), call(','), call('\n'),
                           call('Child1'), call(',C'), call(',B'), call(','), call('\n')]
            handle.write.assert_has_calls(calls=write_calls, any_order=False)


    @patch('import_file_tools.localtime')
    def test_01_2_valid_families(self, mock_localtime):
        entriless = [family.RosterFamily('A B'),
                     family.RosterFamily('Y Z')]
        entriless[0].AddToFamily(child_first  = 'C',
                                 child_last   = 'B',
                                 grade        = '1',
                                 adult_names  = 'A B',
                                 teacher_name = 'Foo',
                                 hub_map      = {'Foo':'1111'},
                                 rosterC      = common_RosterC)
        entriless[1].AddToFamily(child_first  = 'X',
                                 child_last   = 'Z',
                                 grade        = '4',
                                 adult_names  = 'Y Z',
                                 teacher_name = 'Foo',
                                 hub_map      = {'Foo':'1111'},
                                 rosterC      = common_RosterC)
        
        mock_localtime.return_value = time.strptime('2020-01-01-00-00-00',"%Y-%m-%d-%H-%M-%S")
        mocker = mock_open()
        with patch('builtins.open', mocker):
            import_file_tools.CreateFileFromFamily(entriless = entriless)
            mocker.assert_called_with(os.path.abspath('.')+'/new_member_import_2020-01-01-00-00-00.csv','w')
            handle = mocker()
            write_calls = [call('family_relation'), call(',first_name'), call(',last_name'), call(',person_id'), call('\n'),
                           call('Adult'), call(',A'), call(',B'), call(','), call('\n'),
                           call('Child1'), call(',C'), call(',B'), call(','), call('\n'),
                           call('Adult'), call(',Y'), call(',Z'), call(','), call('\n'),
                           call('Child1'), call(',X'), call(',Z'), call(','), call('\n')]
            handle.write.assert_has_calls(calls=write_calls, any_order=False)



class UT_06_CreateAccountlessFile(unittest.TestCase):
    @patch('import_file_tools.localtime')
    def test_01_1_valid_people(self, mock_localtime):
        test_people = [person.DirectoryPerson(last_name       ='B',
                                              first_name      ='A',
                                              family_relation ='Adult',
                                              hub_name_list   =['Foo'],
                                              hub_map         ={'Foo':'1111'},
                                              person_id       ='1234')]
        mock_localtime.return_value = time.strptime('2020-01-01-00-00-00',"%Y-%m-%d-%H-%M-%S")
        mocker = mock_open()
        with patch('builtins.open', mocker):
            import_file_tools.CreateFileFromPeople(people      = test_people,
                                                   file_prefix = 'test')
            mocker.assert_called_with(os.path.abspath('.')+'/test_2020-01-01-00-00-00.csv','w')
            handle = mocker()
            write_calls = [call('First Name'), call(',Last Name'), call(',Affiliated Hub(s)'), call(',Email'), call('\n'),
                           call('A'), call(',B'), call(',[\'1111\']'), call(',None'), call('\n')]
            handle.write.assert_has_calls(calls=write_calls, any_order=False)


    @patch('import_file_tools.localtime')
    def test_02_2_valid_people(self, mock_localtime):
        test_people = [person.DirectoryPerson(last_name       ='B',
                                              first_name      ='A',
                                              family_relation ='Adult',
                                              hub_name_list   =['Foo'],
                                              hub_map         ={'Foo':'1111'},
                                              person_id       ='1234'),
                       person.DirectoryPerson(last_name       ='D',
                                              first_name      ='C',
                                              family_relation ='Child',
                                              hub_name_list   =['Foo'],
                                              hub_map         ={'Foo':'1111'},
                                              person_id       ='2345')]
        mock_localtime.return_value = time.strptime('2020-01-01-00-00-00',"%Y-%m-%d-%H-%M-%S")
        mocker = mock_open()
        with patch('builtins.open', mocker):
            import_file_tools.CreateFileFromPeople(people      = test_people,
                                                   file_prefix = 'test')
            mocker.assert_called_with(os.path.abspath('.')+'/test_2020-01-01-00-00-00.csv','w')
            handle = mocker()
            write_calls = [call('First Name'), call(',Last Name'), call(',Affiliated Hub(s)'), call(',Email'), call('\n'),
                           call('A'), call(',B'), call(',[\'1111\']'), call(',None'), call('\n'),
                           call('C'), call(',D'), call(',[\'1111\']'), call(',None'), call('\n')]
            handle.write.assert_has_calls(calls=write_calls, any_order=False)



class UT_07_CreateEmaillessByHubFile(unittest.TestCase):
    @patch('import_file_tools.localtime')
    def test_01_1_valid_people(self, mock_localtime):
        test_people = [person.DirectoryPerson(last_name       ='B',
                                              first_name      ='A',
                                              family_relation ='Adult',
                                              hub_name_list   =['Foo'],
                                              hub_map         ={'Foo':'1111'},
                                              person_id       ='1234')]
        mock_localtime.return_value = time.strptime('2020-01-01-00-00-00',"%Y-%m-%d-%H-%M-%S")
        mocker = mock_open()
        with patch('builtins.open', mocker):
            import_file_tools.CreateByHubFile(map_d       = {'1111':test_people},
                                              hub_map     = {'Foo':'1111'},
                                              file_prefix = 'test')
            mocker.assert_called_with(os.path.abspath('.')+'/test_2020-01-01-00-00-00.txt','w')
            handle = mocker()
            write_calls = [call('-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-\n'),
                           call('Hub ID: 1111\n'),
                           call('\t\t--> Possible Hub Name: Foo\n'),
                           call('1 people without emails found in this hub\n\n'),
                           call('1'), call(', B'), call(', A'), call('\n'), call('\n')]
            handle.write.assert_has_calls(calls=write_calls, any_order=False)


    @patch('import_file_tools.localtime')
    def test_02_empty_list(self, mock_localtime):
        mock_localtime.return_value = time.strptime('2020-01-01-00-00-00',"%Y-%m-%d-%H-%M-%S")
        mocker = mock_open()
        with patch('builtins.open', mocker):
            import_file_tools.CreateByHubFile(map_d       = {'1111':[]},
                                              hub_map     = {'Foo':'1111'},
                                              file_prefix = 'test')
            mocker.assert_called_with(os.path.abspath('.')+'/test_2020-01-01-00-00-00.txt','w')
            handle = mocker()
            write_calls = [call('-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-\n'),
                           call('Hub ID: 1111\n'),
                           call('\t\t--> Possible Hub Name: Foo\n'),
                           call('All adults in this hub have email addresses in the directory\n'),
                           call('\n')]
            handle.write.assert_has_calls(calls=write_calls, any_order=False)




if __name__ == '__main__':
    unittest.main()