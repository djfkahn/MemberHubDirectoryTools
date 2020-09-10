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
from openpyxl import load_workbook
import csv

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


def FindChildrenInMultipleClassroom(arg_list):
    """menu.FindChildrenInMultipleClassroom
    INPUTS:
    - directory -- list containing the MemberHub directory families
    - map_d     -- dictionary mapping teacher names to hub IDs
    OUTPUTS:
    Prints to standard output the students in the directory who are members of
    more than one classroom hub.
    ASSUMPTIONS:
    None.
    """
    directory       = arg_list[0]
    map_d           = arg_list[1]
    hubful_children = []

    for directory_family in directory:
        for child in directory_family.children:
            if hub_map_tools.IsInMultipleClassroomHubs(map_d, child.hubs):
                hubful_children.append(child)

    print("Found %d students who are not in more than one classroom hub." % len(hubful_children))
    if len(hubful_children) > 0:
        answer = input("Print list to screen? (<enter> for 'no' and 'y' for yes) ")
        if answer == "y":
            for this_person in hubful_children:
                print("%s %s <%s>" % (this_person.first_name, this_person.last_name, this_person.hubs))


def FindAdultsWithoutAccounts(directory):
    """menu.FindAdultsWithoutAccounts
    INPUTS:
    - directory -- list of families from a MemberHub directory dump.
    OUTPUTS:
    Provides the option to write to standard output or to a file the list of adults who
    do not have accounts, separated by whether their profile has an email address or not.
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
    answer = input("Print list to screen or file? ('y' for 'screen', 'f' for file, <return> for neither) ")
    if answer == "y":
        for this_person in no_account_without_email:
            this_person.Print()
    elif answer == "f":
        import_file_tools.CreateEmaillessFile(no_account_without_email, "no_account_without_email")

    print("Found %d adults without accounts, but with emails." % len(no_account_with_email))
    answer = input("Print list to screen or file? ('y' for 'screen', 'f' for file, <return> for neither) ")
    if answer == "y":
        for this_person in no_account_with_email:
            print("%s %s <%s>" % (this_person.first_name, this_person.last_name, this_person.email))
    elif answer == "f":
        import_file_tools.CreateEmaillessFile(no_account_with_email, "no_account_with_email")



def PrintNotInDirectory(arg_list):
    """menu.PrintNotInDirectory
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
    ##
    ## extract copies of the arguments so they are not accidentally modified,
    ## and initialize method variables
    directory = arg_list[0].copy()
    roster    = arg_list[1].copy()
    entriless = []

    ##
    ## loop over all the families in the roster...
    for roster_family in roster:

        ##
        ## ...to compare to each family in the directory
        for directory_family in directory:
            ##
            ## look for matches between roster and directory families
            if directory_family.IsSameFamily(roster_family):
                ##
                ## once a family match is found, check whether the roster family has
                ## children who are not in the directory
                if directory_family.HasNewChildren(roster_family):
                    temp_family = family.Family()
                    temp_family.FormFamilyWithNewChildren(directory_family,roster_family)
                    entriless.append(temp_family)
                break
        ##
        ## if the roster family was not found in the directory, add it to list of
        ## families without directory entry
        else:
            entriless.append(roster_family)

    ##
    ## tell the user how many entriless families were found
    print("Found %d people on the roster who were not in the directory" % len(entriless))
    if len(entriless) == 0:
        return
    
    ##
    ## ask the user how to output the list of entriless families
    answer = " "
    while answer not in (None, '', 'y', 'Y', 'f', 'F'):
        answer = input("Print list to screen or file? ('y' for 'screen', 'f' for file, <return> for neither) ")

    ##
    ## output to the screen
    if answer in ('y', 'Y'):
        for entry in entriless:
            print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-")
            print("Did not find this family from the roster in the directory: ")
            entry.Print()
    ##
    ## output to a file
    elif answer in ('f', 'F'):
        import_file_tools.CreateNewMemberImport(entriless)



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
    - Assumes the roster errata is stored in a file called 'roster_errata.csv'.
    """
    # First, read the roster file once to generate a list of adult names
    roster_adults = []
    roster_name   = roster_tools.GetRosterFileName()
    wb            = load_workbook(roster_name)
    ws            = wb.active
    for fields in ws.values:
        roster_adults.append([fields[3]])

    # Next, read the roster errata file, and check each line that has not been commented out
    line_number = 0
    num_unused  = 0
    with open('roster_errata.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        for fields in csv_reader:
            line_number += 1
            ## skip line if the first character is a comment
            if fields[0][0] == "#":
                continue
            if not([fields[0]] in roster_adults):
                print("Did not find usage of the entry on line %d" % line_number)
                print(fields)
                print("--------------------------------------")
                num_unused += 1

    if num_unused == 0:
        print("No unused errata found.")



def MakePrompt(choices):
    guts = '\n'.join(['(%s) - %s' % (choice, choices[choice]['Description'])
                      for choice in sorted(choices.keys())])
    return '\n===============\nChoose:\n' + guts + '\nOr press <enter> to quit '

def RunMenu(directory, roster, map_d):
    """Runs the user interface for dictionary manipulation."""
    ##
    ## The choices dictionary has function names for values.
    choices = {'a': {'Description':'Find Missing Email',
                     'Function'   :FindMissingEmail,
                     'Arg'        :[directory,map_d]},
               'b': {'Description':'Find Orphans',
                     'Function'   :FindOrphans,
                     'Arg'        :directory},
               'c': {'Description':'Find Childless',
                     'Function'   :FindChildless,
                     'Arg'        :directory},
               'd': {'Description':'Find Not In Classroom Hub',
                     'Function'   :FindHubless,
                     'Arg'        :[directory,map_d]},
               'e': {'Description':'Find Adults without Accounts',
                     'Function'   :FindAdultsWithoutAccounts,
                     'Arg'        :directory},
               'f': {'Description':'Find Not in Directory',
                     'Function'   :PrintNotInDirectory,
                     'Arg'        :[directory,roster]},
               'g': {'Description':'Find Adults/Children Hub Mismatches',
                     'Function'   :FindParentChildrenHubMismatches,
                     'Arg'        :directory},
               'h': {'Description':'Find Unused Errata',
                     'Function'   :FindUnsedErrata,
                     'Arg'        :roster},
               'i': {'Description':'Find students who are in multipe classroom hubs',
                     'Function'   :FindChildrenInMultipleClassroom,
                     'Arg'        :[directory,map_d]}}

    prompt = MakePrompt(choices)

    ##
    ## repeat until exit condition breaks the loop
    while True:
        ##
        ## get the user's selection
        this_choice = input(prompt).lower()
        ##
        ## if the selection is empty (<enter>), the break out of the loop and
        ## terminate the program
        if not this_choice:
            break
        ##
        ## otherwise, perform the selected action if the selection is recognized
        elif this_choice in choices.keys():
            # The appropriate function is called
            # using the dictionary value for the name
            # of the function.
            choices[this_choice]['Function']( choices[this_choice]['Arg'] )
        ##
        ## the selection was not recognized, so tell the user to retry
        else:
            print("%s is not an acceptible choice.  Try again." % this_choice)


def main():
    map_d     = hub_map_tools.ReadHubMap()
    directory = directory_tools.ReadDirectory(map_d)
    roster    = roster_tools.ReadRoster(map_d)
    RunMenu(directory, roster, map_d)

if __name__ == '__main__':
    main()
