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
    
    def AddAdultsFromCombinedField(self, teacher, name_field, grade):
        parent_count = 1
        parent_num = ""
        parents = name_field.split(" and ")
        # if parents have same last name, then there is only one name
        # before the first "and"
        if len(parents[0].split(" ")) == 1:
            last_name = parents[-1].split(" ")[-1]            
            for name in parents:
                parent = name.split(' ')
                new_adult = person.Person()
                self.adults += [new_adult.SetFromRoster(last_name  = last_name,
                                                        first_name = parent[0],
                                                        grade      = grade,
                                                        teacher    = teacher,
                                                        name_field = name_field,
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
                                                        grade      = grade,
                                                        teacher    = teacher,
                                                        name_field = name_field,
                                                        family_relation = "Adult"+parent_num)]
                # prepare the parent_tag for the next parent
                parent_count += 1
                parent_num = str(parent_count)

    def AddAdultFromDirectory(self, fields):
        new_adult = person.Person()
        self.adults += [new_adult.SetFromDirectory(fields)]
    
    def AddChildFromDirectory(self, fields):
        new_child = person.Person()
        self.children += [new_child.SetFromDirectory(fields)]
    
    def CreateFromRoster(self, fields):
        # for elementary school (< 6th grade) teacher name is retained
        # for middle school, teacher name is replaced with grade level
        if int(fields[2]) < 6:
            teacher = fields[4]
        else:
            teacher = fields[2]

        # add adults to the family
        self.AddAdultsFromCombinedField(teacher    = teacher,
                                        name_field = fields[3],
                                        grade      = fields[2])

        # add the child to the family
        new_child = person.Person() 
        self.children = [new_adult.SetFromRoster(last_name  = fields[0],
                                                 first_name = fields[1],
                                                 grade      = fields[2],
                                                 teacher    = teacher,
                                                 name_field = name_field,
                                                 family_relation = "Child1")]


    def IsSameFamily(self, other):
        if not len(self.adults) == len(other.adults):
            return False
        
        num_found = 0
        for adult in self.adults:
            for other_adult in other.adults:
                if adult.IsSame(other_adult):
                    num_found += 1
                    break
        
        return num_found == len(self.adults)

    def CombineWith(self, other):
        to_add = []
        for possible_child in other.children:
            for existing_child in self.children:
                if existing_child.IsSame(possible_child):
                    break
            else:
                to_add += [possible_child]
                
        self.children += to_add
        
    def IsChildless(self):
        return len(self.children) == 0
    
    def IsOrphan(self):
        return len(self.adults) == 0
    
    
