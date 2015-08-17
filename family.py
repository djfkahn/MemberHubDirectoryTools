#!/usr/bin/env python
"""This module defines the family class.
"""
import person
import name_parser

class Family:
    """Class Family
    This class defines family units that have a combination of Person objects
    ATTRIBUTES
    adults   - A list of Person objects representing the family's adults
    children - A list of Person objects representing the family's children
    """
    
    def __init__(self):
        self.adults   = []
        self.children = []
    
    def AddAdultsFromCombinedField(self, teacher, name_field):
        parent_count = 1
        parent_num = ""

        parent_names = name_parser.ParseFullName(name_field)
        for parent in parent_names:
            new_adult = person.RosterPerson()
            new_adult.SetFromRoster(last_name  = parent['last'],
                                    first_name = parent['first'],
                                    teacher    = teacher,
                                    family_relation = "Adult"+parent_num)
            self.adults.append(new_adult)
            parent_count += 1
            parent_num = str(parent_count)


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
        new_child = person.RosterPerson()
        new_child.SetFromRoster(last_name  = fields[0],
                                first_name = fields[1],
                                teacher    = teacher,
                                family_relation = "Child1")
        self.children.append(new_child)

    def AddAdultFromDirectory(self, fields):
        new_adult = person.DirectoryPerson()
        new_adult.SetFromDirectory(fields)
        self.adults.append(new_adult)
    
    def AddChildFromDirectory(self, fields):
        new_child = person.DirectoryPerson()
        new_child.SetFromDirectory(fields)
        self.children.append(new_child)
    
    def IsSameFamily(self, other):
        """Family.IsSameFamily
        INPUTS:
        - other -- the family object to compare to
        OUTPUTS:
        - returns True when the two objects contain all the same adults
          or when the two objects share at least one adult and one child
        - returns False otherwise
        """
        adults_found = 0
        for other_adult in other.adults:
            if self.FindAdultInFamily(other_adult) != None:
                adults_found += 1

        # if both families contain all the same adults
        if adults_found == len(self.adults):
            return True
        # otherwise if the families share at least one adult and one child
        elif adults_found > 0:
            for other_child in other.children:
                if self.FindChildInFamily(other_child) != None:
                    return True

        return False

    def HasNewChildren(self, other):
        """Family.HasNewChildren
        INPUTS:
        - other -- 
        - other -- the family object to compare to
        OUTPUTS:
        - returns True if any child in the other family is not found in this family
        - returns False otherwise
        """
        for other_child in other.children:
            # if any child in the other family cannot be found in this family...
            if self.FindChildInFamily(other_child) == None:
                #... return True
                return True

        return False

    def FormFamilyWithNewChildren(self, directory_family, roster_family):
        # copy the adults from the directory, because they include the person_ids
        self.adults = directory_family.adults
        
        # copy only the new children
        for roster_child in roster_family.children:
            # if the roster_child cannot be found in this family ...
            if directory_family.FindChildInFamily(roster_child) == None:
                # ...then append the roster_child to this family
                self.children.append(roster_child)

    def CombineWith(self, other):
        for possible_child in other.children:
            # if the possible_child cannot be found in this family...
            if self.FindChildInFamily(possible_child) == None:
                #...then append the possible_child to the family
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

    def FindAdultInFamily(self, to_find):
        for adult in self.adults:
            if to_find.IsSame(adult):
                return adult
        return None

    def FindChildInFamily(self, to_find):
        for child in self.children:
            if to_find.IsSame(child):
                return child
        return None
        
    def FindPersonInFamily(self, to_find):
        try_person = self.FindAdultInFamily(to_find)
        if try_person == None:
            try_person = self.FindChildInFamily(to_find)

        return try_person

    def Print(self):
        print "Adults:"
        for adult in self.adults:
            adult.Print()
        print "Children:"
        for child in self.children:
            child.Print()
