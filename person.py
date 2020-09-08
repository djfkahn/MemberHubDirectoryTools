#!/usr/bin/env python
"""This module defines the person and family classes.
"""

import hub_map_tools

class Person:
    """Class Person
    This class defines the characteristics that every Person in this project must possess.
    Several methods are defined for the parent class.
    ATTRIBUTES:
    last_name       - A string
    first_name      - A string
    family_relation - A string of the form "Adult#" or "Child#", where "#" is either blank or a number.
    """
    def __init__(self):
        self.last_name       = None
        self.first_name      = None
        self.family_relation = None
        self.hubs            = []

    def Set(self, last_name, first_name, family_relation, hub_name_list, hub_map):
        if last_name and first_name and family_relation and family_relation[:5].lower() in ('adult', 'child'):
            self.last_name       = last_name
            self.first_name      = first_name
            self.family_relation = family_relation
            self.hubs            = hub_map_tools.ConvertHubStringListToIDList \
                                       (hub_name_list, hub_map)
            return True
        
        return False

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
                

    def SetHubs (self, hub_list):
        for hub_id in hub_list:
            self.AddHubID(hub_id)

    def AddHubID(self, hub_id):
        self.hubs.append(hub_id)

    def DoesNotListEmailAddress(self):
        return self.email == ""

    def Print(self):
        print("%s %s" % (self.first_name, self.last_name))

class DirectoryPerson (Person):
    """This class extends the Person class with Directory-only fields."""
    def __init__(self):
        super(DirectoryPerson, self).__init__()
        self.person_id       = None
        self.middle_name     = None
        self.suffix          = None
        self.email           = None
        self.family_id       = None
        self.parents         = None
        self.account_created = None
        self.account_updated = None

    def SetFromDirectory (self, fields, hub_map):
        if self.Set(last_name       = fields[1].strip('"'),
                    first_name      = fields[2].strip('"'),
                    family_relation = fields[7].strip('"'),
                    hub_name_list   = fields[24].split(';'),
                    hub_map         = hub_map):

            ##
            ## Store attributes that are only given by the Directory
            self.person_id       = fields[0].strip('"')
            self.middle_name     = fields[3].strip('"')
            self.suffix          = fields[4].strip('"')
            self.email           = fields[5].strip('"')
            self.family_id       = fields[6].strip('"')
            self.account_created = fields[28].strip('"')
            self.account_updated = fields[29].strip('"')

class RosterPerson (Person):
    """This class extends the Person class with Roster-only fields."""

    def SetFromRoster(self, last_name, first_name, teacher, family_relation, hub_map):
        temp = self.Set(last_name       = last_name,
                        first_name      = first_name,
                        family_relation = family_relation,
                        hub_name_list   = [teacher],
                        hub_map         = hub_map)
