#!/usr/bin/env python
"""This module defines the family class.
"""
import person

class Family:
    """Class Person
    TBD - document class
    """
    
    def __init__(self):
        self.adults   = []
        self.children = []
    
    def AddAdultFromDirectory(self, fields):
        new_adult = person.Person()
        self.adults += [new_adult.SetFromDirectory(fields)]
    
    def AddAdultsFromCombinedField(self, fields):
        parent_count = 1
        parent_num = ""
        parents = fields[3].split(" and ")
        # if parents have same last name, then there is only one name
        # before the first "and"
        if len(parents[0].split(" ")) == 1:
            last_name = parents[-1].split(" ")[-1]            
            for name in parents:
                parent = name.split(' ')
                new_adult = person.Person()
                self.adults += [new_adult.SetFromRoster(last_name  = last_name,
                                                        first_name = parent[0],
                                                        grade      = fields[2],
                                                        teacher    = teacher,
                                                        name_field = fields[3],
                                                        family_relation = "Adult"+parent_num)]
                # prepare the parent_tag for the next parent
                parent_count += 1
                parent_num = str(parent_count)

        # each parent as a unique first and last name
        else:
            for name in parents:
                parent = name.split(' ')
                new_adult = person.Person()
                self.adults += [new_adult.SetFromRoster(last_name  = parent[-1],
                                                        first_name = " ".join(parent[0:-1]),
                                                        grade      = fields[2],
                                                        teacher    = teacher,
                                                        name_field = fields[3],
                                                        family_relation = "Adult"+parent_num)]
                # prepare the parent_tag for the next parent
                parent_count += 1
                parent_num = str(parent_count)

     def AddChildFromDirectory(self, fields):
        new_child = person.Person()
        self.children += [new_child.SetFromDirectory(fields)]
    
    def IsSameFamily(self, other):
        if not len(self.adults) == len(other.adults):
            return False
        
        num_found = 0
        for adult in self.adults:
            for other_adult in other.adults:
                if adult.IsSame(other_adult):
                    num_found += 1
                    break
        
        return num_found = len(self.adults)
