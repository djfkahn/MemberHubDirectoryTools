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
    
    def AddAdultsFromCombinedField(self, teacher, name_field):
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
                new_adult.SetFromRoster(last_name  = last_name,
                                        first_name = parent[0],
                                        teacher    = teacher,
                                        family_relation = "Adult"+parent_num)
                self.adults.append(new_adult)
                # prepare the parent_tag for the next parent
                parent_count += 1
                parent_num = str(parent_count)

        # each parent as a unique first and last name
        else:
            for name in parents:
                parent = name.split(' ')
                new_adult = person.Person()
                new_adult.SetFromRoster(last_name  = parent[-1],
                                        first_name = " ".join(parent[0:-1]),
                                        teacher    = teacher,
                                        family_relation = "Adult"+parent_num)
                self.adults.append(new_adult)
                # prepare the parent_tag for the next parent
                parent_count += 1
                parent_num = str(parent_count)

    def AddAdultFromDirectory(self, fields):
        new_adult = person.Person()
        new_adult.SetFromDirectory(fields)
        self.adults.append(new_adult)
    
    def AddChildFromDirectory(self, fields):
        new_child = person.Person()
        new_child.SetFromDirectory(fields)
        self.children.append(new_child)
    
    def CreateFromRoster(self, fields):
        # for elementary school (< 6th grade) teacher name is retained
        # for middle school, teacher name is replaced with grade level
        if int(fields[2]) < 6:
            teacher = fields[4]
        else:
            teacher = fields[2]

        # add adults to the family
        self.AddAdultsFromCombinedField(teacher    = teacher,
                                        name_field = fields[3])

        # add the child to the family
        new_child = person.Person()
        new_child.SetFromRoster(last_name  = fields[0],
                                first_name = fields[1],
                                teacher    = teacher,
                                family_relation = "Child1")
        self.children.append(new_child)


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
        for possible_child in other.children:
            for existing_child in self.children:
                if existing_child.IsSame(possible_child):
                    break
            else:
                self.children.append(possible_child)
                # change the family relation for the new child
                self.children[-1].family_relation = "Child%d" % (len(self.children))
                # add hubs of the new child to the existing adult hubs.
                for index in range(len(self.adults)):
                    self.adults[index].hubs += possible_child.hubs

    def IsChildless(self):
        return len(self.children) == 0
    
    def IsOrphan(self):
        return len(self.adults) == 0

    def FindPersonInFamily(self, to_find):
        for adult in self.adults:
            if to_find.IsSame(adult):
                return adult
        for child in self.children:
            if to_find.IsSame(child):
                return child
        return None
    
    def Print(self):
        print "Adults:"
        for adult in self.adults:
            adult.Print()
        print "Children:"
        for child in self.children:
            child.Print()
