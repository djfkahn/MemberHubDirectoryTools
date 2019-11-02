#!/usr/bin/env python
"""Defines the main menu module for a program that inputs a MemberHub directory dump,
a school roster, and a hub map to perform analyses on the MemberHub directory.
"""

import directory_tools
import roster_tools
import hub_map_tools
import import_file_tools
import family
import person

STUDENT_INDICATOR = "+SA"

def FindMissingEmail(arg_list):
    """menu.FindMissingEmail
    INPUTS:
    - directory -- list containing the MemberHub directory families
    - map_d     -- dictionary mapping teacher names to hub IDs
    OUTPUTS:
    Prints to standard output statistics about families with and without
    email addresses, and give the option to display the lists.
    ASSUMPTIONS:
    None.
    """
    directory   = arg_list[0]
    hub_map_d   = arg_list[1]
    map_d       = hub_map_tools.CreateEmptyHubDictionary(hub_map_d)
    adult_count = no_email_adult = 0
    no_email_person = []
    no_email_family = []
    partial_family = []

    for entry_family in directory:
        no_email_count = 0
        for adult in entry_family.adults:
            adult_count += 1
            if adult.DoesNotListEmailAddress():
                no_email_person.append(adult)
                no_email_adult += 1
                no_email_count += 1
                for hub in adult.hubs:
                	if hub in map_d.keys():
	                	map_d[hub].append(adult)

        if no_email_count == len(entry_family.adults):
            no_email_family.append(entry_family)
        elif no_email_count > 0:
            partial_family.append(entry_family)

    print("The directory has %d families and %d adults." % \
          (len(directory), adult_count))
    print("Of the %d adults, %d have no email address." % \
          (adult_count, no_email_adult))
    print("%d out of %d families have no adult with an email address." % \
          (len(no_email_family), len(directory)))
    print("%d out of %d families have some adults without and some with email addresses." % \
          (len(partial_family), len(directory)))
    print("%d out of %d families have all adults with email addresses." % \
          ((len(directory)-len(no_email_family)-len(partial_family)), len(directory)))
    print("%d out of %d families have at least one adult with an email address." % \
          ((len(directory)-len(no_email_family)), len(directory)))

    print("")

    import_file_tools.CreateEmaillessFile(map_d, hub_map_d, "emailless")



def FindOrphans(directory):
    """menu.FindOrphans
    INPUTS:
    - directory -- list containing the MemberHub directory families
    OUTPUTS:
    Prints to standard output the children in the directory who do not have an
    parent associated with their entry.
    ASSUMPTIONS:
    None.
    """
    family_count = orphan_count = 0

    for entry_family in directory:
        family_count += 1
        if entry_family.IsOrphan():
            print("The entry for this family does not identify parents:",)
            entry_family.Print()
            orphan_count += 1

    print("Found %d families without adults out of %d families" % \
          (orphan_count, family_count))

def FindChildless(directory):
    """menu.FindChildless
    INPUTS:
    - directory -- list containing the MemberHub directory families
    OUTPUTS:
    Prints to standard output the adults in the directory who do not have a
    child associated with their entry.
    ASSUMPTIONS:
    None.
    """
    family_count = childless_count = 0

    for entry_family in directory:
        family_count += 1
        if entry_family.IsChildless():
            print("The entry for this family does not identify children:",)
            entry_family.Print()
            childless_count += 1

    print("Found %d families without children out of %d families" % \
          (childless_count, family_count))

def FindHubless(arg_list):
    """menu.FindHubless
    INPUTS:
    - directory -- list containing the MemberHub directory families
    - map_d     -- dictionary mapping teacher names to hub IDs
    OUTPUTS:
    Prints to standard output the names in the directory who are not members of
    at least one classroom hub.
    ASSUMPTIONS:
    None.
    """
    directory        = arg_list[0]
    map_d            = arg_list[1]
    hubless_adults   = []
    hubless_children = []

    for directory_family in directory:
        for adult in directory_family.adults:
            if not hub_map_tools.IsAnyHubClassroomHub(map_d, adult.hubs):
                hubless_adults.append(adult)

        for child in directory_family.children:
            if not hub_map_tools.IsAnyHubClassroomHub(map_d, child.hubs):
                hubless_children.append(child)

    print("Found %d adults who are not in at least one classroom hub." % len(hubless_adults))
    if len(hubless_adults) > 0:
        answer = input("Print list to screen? (<enter> for 'no' and 'y' for yes) ")
        if answer == "y":
            for this_person in hubless_adults:
                print("%s %s <%s>" % (this_person.first_name, this_person.last_name, this_person.hubs))

    print("Found %d children who are not in a classroom hub." % len(hubless_children))
    if len(hubless_children) > 0:
        answer = input("Print list to screen? (<enter> for 'no' and 'y' for yes) ")
        if answer == "y":
            for this_person in hubless_children:
                print("%s %s <%s>" % (this_person.first_name, this_person.last_name, this_person.hubs))



def FindAdultsWithoutAccounts(directory):
    """menu.FindAdultsWithoutAccounts
    INPUTS:
    - directory -- list of families from a MemberHub directory dump.
    OUTPUTS:
    Provides the option to write to standard output the list of adults who
    do not have accounts, separated by whether their profile has an email
    address or not.
    """
    no_account_with_email    = []
    no_account_without_email = []

    for this_family in directory:
        for this_adult in this_family.adults:
            if this_adult.account_created == "":
                if this_adult.email == "":
                    no_account_without_email.append(this_adult)
                else:
                    no_account_with_email.append(this_adult)

    print("Found %d adults without accounts or emails." % len(no_account_without_email))
    answer = input("Print list to screen? ('y' for yes) ")
    if answer == "y":
        for this_person in no_account_without_email:
            this_person.Print()

    print("Found %d adults without accounts, but with emails." % len(no_account_with_email))
    answer = input("Print list to screen? ('y' for yes) ")
    if answer == "y":
        for this_person in no_account_with_email:
            print("%s %s <%s>" % (this_person.first_name, this_person.last_name, this_person.email))



def FindEntriless(arg_list):
    """menu.FindEntriless
    INPUTS:
    - directory -- list containing the MemberHub directory families
    - roster    -- list containing the school roster families
    OUTPUTS:
    - entriless -- returns list of families in the school roster that could not
                   be found in the directory
    Also prints to standard output the names in the school roster who are not in the
    MemberHub directory.
    ASSUMPTIONS:
    None.
    """
    directory = arg_list[0]
    roster    = arg_list[1]
    entriless = []

    for roster_family in roster:

        for directory_family in directory:
            if directory_family.IsSameFamily(roster_family):
                if directory_family.HasNewChildren(roster_family):
                    temp_family = family.Family()
                    temp_family.FormFamilyWithNewChildren(directory_family,roster_family)
                    print("Found family in directory with new child in roster:",)
                    temp_family.Print()
                    entriless.append(temp_family)
                break

        else:
            print("Did not find this family from the roster in the directory:",)
            roster_family.Print()
            entriless.append(roster_family)

    print("Found %d people on the roster who were not in the directory" % len(entriless))
    return entriless

def PrintNotInDirectory(arg_list):
    discard = FindEntriless(arg_list)

def MakeImportNotInDirectory(arg_list):
    """menu.MakeImportNotInDirectory
    INPUTS:
    - directory -- dictionary containing the MemberHub directory
    - roster    -- dictionary containing the school roster
    - map_d     -- dictionary mapping teacher names to hub IDs
    OUTPUTS:
    Creates a comma-separated text file that can be imported into MemberHub to create
    directory entries for people who are in the roster, but not already in the directory.
    Includes hub ID assignments for these people.
    ASSUMPTIONS:
    None.
    """
    entriless = FindEntriless(arg_list)

    import_file_tools.CreateNewMemberImport(entriless)

def MakeStudentImportFile(arg_list):
    """menu.MakeStudentImportFile
    INPUTS:
    - directory -- dictionary containing the MemberHub directory
    - roster    -- dictionary containing the school roster
    OUTPUTS:
    Creates a comma-separated text file that can be imported into MemberHub to create
    directory entries for people who are in the roster, but not already in the directory.
    Includes hub ID assignments for these people.
    ASSUMPTIONS:
    Each person in the roster belongs to only one hub, and it is the classroom hub.
    """
    directory = arg_list[0]
    roster    = arg_list[1]
    students  = []
    not_found = []

    ## For each family in the roster ...
    for roster_family in roster:
        ## ...find the corresponding family in the directory
        for directory_family in directory:
            if directory_family.IsSameFamily(roster_family):
                ## For each child in the roster family...
                for roster_child in roster_family.children:
                    ## ...find the corresponding child in the directory family
                    directory_child = directory_family.FindChildInFamily(roster_child)
                    if directory_child != None:
                        ## instantiate a new Directory Person object, and copy the directory child into it
                        temp_child = person.DirectoryPerson()
                        temp_child = directory_child
                        ## populate the temporary object's hub with the roster child's hub
                        ## modified with the student indicator appended
                        ## MODIFIED CODE START - 2017-09-02
                        ##temp_child.hubs = [roster_child.hubs[0] + STUDENT_INDICATOR]
                        temp_child.hubs = "/"+roster_child.hubs[0] + STUDENT_INDICATOR+"/"
                        ## MODIFIED CODE END

                        ## add the temporary child object to the list of students
                        students.append(temp_child)
                    else:
                        print("##################")
                        print("Did not find this child",)
                        roster_child.Print()
                        print(" in the family: ")
                        directory_family.Print()
                        not_found.append(roster_child)
                ## Found the roster family in the directory, so break out of the directory_family loop
                break
        else:
            print("Did not find this family from the roster in the directory:",)
            roster_family.Print()
            not_found.append(roster_family.children)

    print("Found %d students on the roster who were in the directory" % len(students))
    print("%d students on the roster could not be matched with the directory" % len(not_found))

    ## Create an import file with all the students
    import_file_tools.CreateHubImportFile(students, "students2hubs")


def FindParentChildrenHubMismatches(directory):

    for this_family in directory:
        children_hubs = []
        for this_child in this_family.children:
            for this_hub in this_child.hubs:
                children_hubs.append(this_hub)

        for this_adult in this_family.adults:
            for child_hub in children_hubs:
                if child_hub not in this_adult.hubs:
                    print("Found adult who is not a member of all family children's hubs:")
                    print("Adult Name:    ",)
                    this_adult.Print()
                    print("Adult Hubs:    ",)
                    print(this_adult.hubs)
                    for this_child in this_family.children:
                    	print("Child Name -- ",)
                    	this_child.Print()
                    	print(" -- ")
                    	print(this_child.hubs)
                    break
    else:
        print("All adults are members of hubs to which all family children belong.")


def FindUnsedErrata(roster):
    """menu.FindUnsedErrata
    INPUTS:
    - roster    -- passing roster, because something needs to be passed (not actually used)
    OUTPUTS:
    Prints the roster errata entries that are no longer found in the roster, and can be
    removed.
    ASSUMPTIONS:
    None.
    """
    roster_name = input("Enter name of roster comma-separated text file (press <enter> to use \"roster.csv\"): ")
    if not roster_name:
        roster_name = "roster.csv"

    # First, read the roster file once to generate a list of adult names
    try:
        roster_file = open(roster_name)
        raw_line = roster_file.readline()
        if len(raw_line.split(',')) != 5:
            raise RuntimeError("This roster file has %d fields, but 5 are expected." % len(raw_line.split(',')))

        roster_names = []
        for line in roster_file:
            # process the line without the trailing '\r\n' that Excel adds
            fields = line.strip('\n\r').strip('"').split(',')
            roster_names.append([fields[3]])
    finally:
        roster_file.close()

    # Next, read the roster errata file, and check each line that has not been commented out
    try:
        errata_file = open('roster_errata.csv')
        line_number = 0
        for line in errata_file:
            line_number += 1
            if line[0] != "#":
                fields = line.split('|')
                found  = False
                for entry in roster_names:
                    if fields[0] == entry[0]:
                        found = True
                        break

                if not found:
                    print("Did not find usage of the entry on line %d" % line_number)
                    print(line)
                    print("--------------------------------------")
    finally:
        errata_file.close()



def MakePrompt(choices):
    choice_list = sorted(choices)
    guts = '\n'.join(['(%s)%s' % (choice[0], choice[1:])
                      for choice in choice_list])
    return '\n===============\nChoose:\n' + guts + '\nOr press <enter> to quit '

def RunMenu(directory, roster, map_d):
    """Runs the user interface for dictionary manipulation."""
    # The choices dictionary has function names for values.
    choices = {'a - Find Missing Email':
                    {'Function':FindMissingEmail,'Arg':[directory,map_d]},
               'b - Find Orphans':
                    {'Function':FindOrphans,'Arg':directory},
               'c - Find Childless':
                    {'Function':FindChildless,'Arg':directory},
               'd - Find Not In Classroom Hub':
                    {'Function':FindHubless,'Arg':[directory,map_d]},
               'e - Find Adults without Accounts':
                    {'Function':FindAdultsWithoutAccounts,'Arg':directory},
               'f - Find Not in Directory':
                    {'Function':PrintNotInDirectory,'Arg':[directory,roster]},
               'g - Make Import File for Not In Directory':
                    {'Function':MakeImportNotInDirectory,'Arg':[directory,roster,map_d]},
               'h - Make Student Hub Population Import File':
                    {'Function':MakeStudentImportFile,'Arg':[directory,roster]},
               'i - Find Adults/Children Hub Mismatches':
                    {'Function':FindParentChildrenHubMismatches,'Arg':directory},
               'j - Find Unused Errata':
                    {'Function':FindUnsedErrata,'Arg':roster}}

    prompt = MakePrompt(choices)

    while True:
        raw_choice = input(prompt)
        if not raw_choice:
            break
        given_choice = raw_choice[0].lower()
        for maybe_choice in choices:
            if maybe_choice[0] == given_choice:
                # The appropriate function is called
                # using the dictionary value for the name
                # of the function.
                choices[maybe_choice]['Function'](choices[maybe_choice]['Arg'])
                break
        else:
            print("%s is not an acceptible choice." % raw_choice)


def main():
    map_d     = hub_map_tools.ReadHubMap()
    directory = directory_tools.ReadDirectory(map_d)
    roster    = roster_tools.ReadRoster(map_d)
    RunMenu(directory, roster, map_d)

if __name__ == '__main__':
    main()
