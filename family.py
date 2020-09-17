#!/usr/bin/env python
"""This module defines the family class.
"""
import person
import name_parser
import hub_map_tools

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

    def AddAdultsFromCombinedField(self, teacher, name_field, hub_map, rosterC):
        parent_count = 1
        parent_num = ""

        parent_names = name_parser.ParseFullName(name_field, rosterC)
        for parent in parent_names:
            new_adult = person.RosterPerson()
            new_adult.SetFromRoster(last_name       = parent['last'],
                                    first_name      = parent['first'],
                                    teacher         = teacher,
                                    family_relation = "Adult"+parent_num,
                                    hub_map         = hub_map)
            self.adults.append(new_adult)
            parent_count += 1
            parent_num = str(parent_count)


    def CreateFromRoster(self, fields, hub_map, rosterC):
        # for elementary school (< 6th grade) teacher name is retained
        # for middle school, teacher name is replaced with grade level
        if 0 <= int(fields[2]) <= 5:
            if hub_map_tools.IsInClassroomHub(hub_map, fields[4]):
                teacher = fields[4]
            else:
                print("Elementry school student from Roster found with unknown teacher.")
                print(fields)
                return
        elif 6 <= int(fields[2]) <= 8:
            teacher = fields[2]
        else:
            print("Student from Roster found with unknown teacher and unknown grade level.")
            print(fields)
            return
           

        # add adults to the family
        self.AddAdultsFromCombinedField(teacher    = teacher,
                                        name_field = fields[3],
                                        hub_map    = hub_map,
                                        rosterC    = rosterC)

        # add the child to the family
        new_child = person.RosterPerson()
        new_child.SetFromRoster(last_name       = fields[0],
                                first_name      = fields[1],
                                teacher         = teacher,
                                family_relation = "Child1",
                                hub_map         = hub_map)
        self.children.append(new_child)

    def AddFromDirectory(self, fields, hub_map):
        if fields[7][:5].lower() == 'adult':
            new_adult = person.DirectoryPerson()
            new_adult.SetFromDirectory(fields, hub_map)
            self.adults.append(new_adult)
        elif fields[7][:5].lower() == 'child':
            new_child = person.DirectoryPerson()
            new_child.SetFromDirectory(fields, hub_map)
            self.children.append(new_child)
        else:
            print("Attempting to add person from Directory to family with unrecognized family relation.")
            print(fields)


    def IsSameFamily(self, other):
        """Family.IsSameFamily
        INPUTS:
        - other -- the family object to compare to
        OUTPUTS:
        - returns True when the two objects contain all the same adults
          or when the two objects share at least one adult and one child
        - returns False otherwise
        """
        # Families cannot be the same, if either one of them contain orphans
        if self.IsOrphan() or other.IsOrphan():
            return False

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
        if not self.IsSameFamily(other):
            return
        
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
        ## not childless if more than zero persons in children attribute
        if len(self.children) > 0:
            return False

        ## not considered childless if the first adult is a teacher or staff,
        ## as indicated by membership in either the "Teachers" or "Staff" hubs
        if "Teachers" in self.adults[0].hubs or \
           "Staff" in self.adults[0].hubs or \
           "Volunteers" in self.adults[0].hubs:
            return False

        ## considered childless if none of the above conditions hold
        return True


    def IsOrphan(self):
        ##
        ## Consider the family an "orphan" if there are no adults, or
        ## if all the adults have no first or last name
        none_cnt = 0
        for this_adult in self.adults:
            if not this_adult.first_name or not this_adult.last_name:
                none_cnt += 1
        return len(self.adults) == 0 or len(self.adults) == none_cnt

    def FindAdultInFamily(self, to_find):
        # Cannot find adult in a family if family is orphan
        if self.IsOrphan():
            return None

        for adult in self.adults:
            if to_find.IsSame(adult):
                return adult
        return None

    def FindChildInFamily(self, to_find):
        for child in self.children:
            if to_find.IsSame(child):
                return child
        return None

    def Print(self):
        print("Adults:")
        for adult in self.adults:
            adult.Print()
        print("Children:")
        for child in self.children:
            child.Print()

    def PrintWithHubs(self):
        print("Adults:")
        for adult in self.adults:
            adult.PrintWithHubs()
        print("Children:")
        for child in self.children:
            child.PrintWithHubs()
