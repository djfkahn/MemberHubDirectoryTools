#!/usr/bin/env python
"""This module defines the person and family classes.
"""

class Person:
    """Class Person
    TBD - document class
    """
    
    def SetFromDirectory (self, fields):
        self.person_id = fields[0][1:]
        self.last_name = fields[1]
        self.first_name = fields[2]
        self.middle_name = fields[3]
        self.suffix = fields[4]
        self.email = fields[5]
        self.family_id = fields[6]
        self.family_relation = fields[7]
        self.maiden_name = fields[8]
        self.born_on = fields[9]
        self.gender = fields[10]
        self.parents = fields[11]
        self.street = fields[12]
        self.city = fields[13]
        self.state = fields[14]
        self.zip = fields[15]
        self.home_number = fields[16]
        self.work_number = fields[17]
        self.work_number_ext = fields[18]
        self.fax_number = fields[19]
        self.mobile_number = fields[20]
        self.mobile_provider = fields[21]
        self.allow_sms = fields[22]
        self.hubs = fields[23]
        self.hubs_administered = fields[24]
        self.person_created = fields[25]
        self.person_updated = fields[26]
        self.account_created = fields[27]
        self.account_updated = fields[28]
        self.last_login = fields[29][:-3]
    
    def SetFromRoster(self, last_name, first_name, grade, teacher, name_field, family_relation):
        self.last_name = last_name
        self.first_name = first_name
        self.grade = grade
        self.teacher = teacher
        self.name_field = name_field
        self.family_relation = family_relation
        self.person_id = " "

    def IsSame (self, other):
        return self.last_name.lower()  == other.last_name.lower() and \
                self.first_name.lower() == other.first_name.lower() and \
                self.family_relation[:5].lower() == other.family_relation[:5].lower()

