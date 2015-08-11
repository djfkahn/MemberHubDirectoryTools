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

    def Set(self, last_name, first_name, family_relation):
        self.last_name       = last_name
        self.first_name      = first_name
        self.family_relation = family_relation

    def IsSame (self, other):
        return self.last_name.lower()  == other.last_name.lower() and \
                self.first_name.lower() == other.first_name.lower() and \
                self.family_relation[:5].lower() == other.family_relation[:5].lower()

    def SetHubs (self, hub_list):
        for hub_id in hub_list:
            self.AddHubID(hub_id)

    def AddHubID(self, hub_id):
        self.hubs.append(hub_id)

    def DoesNotListEmailAddress(self):
        return self.email == ""

    def Print(self):
        print "%s %s" % (self.first_name, self.last_name)

class DirectoryPerson (Person):
    """This class extends the Person class with Directory-only fields."""

    def SetFromDirectory (self, fields):
        self.Set(last_name = fields[1], first_name = fields[2], family_relation = fields[7])

        self.person_id = fields[0][1:]
        self.middle_name = fields[3]
        self.suffix = fields[4]
        self.email = fields[5]
        self.family_id = fields[6]
        self.parents = fields[11]
        hub_name_list = fields[23].split(';')
        self.hubs = hub_map_tools.ConvertToHubIDList(hub_name_list)
        self.account_created = fields[27]
        self.account_updated = fields[28]

class RosterPerson (Person):
    """This class extends the Person class with Roster-only fields."""

    def SetFromRoster(self, last_name, first_name, teacher, family_relation):
        self.Set(last_name = last_name, first_name = first_name, family_relation = family_relation)
        self.hubs = hub_map_tools.ConvertToHubIDList([teacher])

