#!/usr/bin/env python
"""This module defines the person and family classes.
"""

from hub_map_tools import ConvertHubStringListToIDList

class Person:
    """Class Person
    This class defines the characteristics that every Person in this project must possess.
    Several methods are defined for the parent class.
    ATTRIBUTES:
    last_name       - A string
    first_name      - A string
    family_relation - A string of the form "Adult#" or "Child#", where "#" is either blank or a number.
    """

    def __init__(self, last_name, first_name, family_relation, hub_name_list, hub_map):

        if last_name and first_name and family_relation and family_relation[:5].lower() in ('adult', 'child'):
            self.last_name       = last_name
            self.first_name      = first_name
            self.family_relation = family_relation
            if hub_name_list and hub_map:
                self.hubs        = ConvertHubStringListToIDList (hub_name_list, hub_map)
            else:
                self.hubs        = []
        else:
            self.last_name       = None
            self.first_name      = None
            self.family_relation = None
            self.hubs            = []


    def IsSame (self, other):
        ##
        ## Persons are not the same if they do not have the same family relation
        if self.family_relation[:5].lower() != other.family_relation[:5].lower():
            return False
        
        ##
        ## Treat both names in total, to avoid situations in which multi-word names
        ## are split in unexpected ways.  Also, convert all hyphens ("-") to spaces.
        this_full_name = self.first_name.lower()  + " " + self.last_name.lower()
        that_full_name = other.first_name.lower() + " " + other.last_name.lower()
        return this_full_name.replace("-", " ")  == that_full_name.replace("-", " ")
                
    def IsWithSchool(self):
        return 'Staff'   in self.hubs or \
               'Teacher' in self.hubs

    def SetHubs (self, hub_list):
        for hub_id in hub_list:
            self.AddHubID(hub_id)

    def AddHubID(self, hub_id):
        self.hubs.append(hub_id)

    def DoesNotListEmailAddress(self):
        return self.email == ""

    def Print(self):
        print("%s %s" % (self.first_name, self.last_name))

    def PrintWithHubs(self):
        print("%s %s - <%s>" % (self.first_name, self.last_name, self.hubs))

    def PrintWithEmail(self):
        print("%s %s - <%s>" % (self.first_name, self.last_name, self.email))

class DirectoryPerson (Person):
    """This class extends the Person class with Directory-only fields."""
    def __init__(self, last_name, first_name, family_relation, hub_name_list, hub_map,
                 person_id=None, middle_name=None,suffix=None, email=None, family_id=None,
                 account_created=None, account_updated=None):

        super(DirectoryPerson, self).__init__(last_name       = last_name,
                                              first_name      = first_name,
                                              family_relation = family_relation,
                                              hub_name_list   = hub_name_list,
                                              hub_map         = hub_map)
        self.person_id       = person_id
        self.middle_name     = middle_name
        self.suffix          = suffix
        self.email           = email
        self.family_id       = family_id
        self.account_created = account_created
        self.account_updated = account_updated



class RosterPerson (Person):
    """This class extends the Person class with Roster-only fields."""
    def __init__(self, last_name, first_name, family_relation, teacher, hub_map):

        super(RosterPerson, self).__init__(last_name       = last_name,
                                           first_name      = first_name,
                                           family_relation = family_relation,
                                           hub_name_list   = [teacher],
                                           hub_map         = hub_map)

