#!/usr/bin/env python
"""Defines the main menu module for a program that inputs a MemberHub directory dump,
a school roster, and a hub map to perform analyses on the MemberHub directory.
"""

import directory_tools
import roster_tools
import hub_map_tools
import import_file_tools
import roster
import actions

STUDENT_INDICATOR = "+SA"
STDOUT_SEPERATOR  = "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-"

def PrintToScreenFileOrNeither(prompt):
    """menu.PrintToScreenFileOrNeither
    INPUTS:
    - prompt -- string prompting the user to answer
    OUTPUTS:
    - 'y', 'f', or '' -- will ask over and over until one of these inputs is given
    ASSUMPTIONS:
    - None.
    """
    answer = " "
    while answer not in (None, '', 'y', 'Y', 'f', 'F'):
        answer = input(prompt + "? ('y' for 'screen', 'f' for file, <enter> for neither) ")

    return answer.lower()    

def PrintToScreenOrNot():
    """menu.PrintToScreenOrNot
    INPUTS:
    - none
    OUTPUTS:
    - 'y' or '' -- will ask over and over until one of these inputs is given
    ASSUMPTIONS:
    - None.
    """
    answer = " "
    while answer not in (None, '', 'y', 'Y'):
        answer = input("Print list to screen? (<enter> for 'no' and 'y' for 'to screen') ")

    return answer.lower()    

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
    ##
    ## perform the action
    total_adult_count, no_email_person, no_email_family, partial_family, map_d = \
        actions.FindMissingEmail(arg_list)
    ##
    ## extract copies of the arguments so they are not accidentally modified
    directory         = arg_list[0].copy()
    hub_map_d         = arg_list[1].copy()
    ##
    ## print some of the counts to the screen for the user to review
    print(STDOUT_SEPERATOR)
    print("The directory has %d families and %d adults." % \
          (len(directory), total_adult_count))
    print("%d out of the %d adults have no email address." % \
          (len(no_email_person), total_adult_count))
    print("%d out of %d families have no adult with an email address." % \
          (len(no_email_family), len(directory)))
    print("%d out of %d families have some adults without and some with email addresses." % \
          (len(partial_family), len(directory)))
    print("%d out of %d families have all adults with email addresses." % \
          ((len(directory)-len(no_email_family)-len(partial_family)), len(directory)))
    print("%d out of %d families have at least one adult with an email address." % \
          ((len(directory)-len(no_email_family)), len(directory)))
    ##
    ## create a list of people in each hub who do not have an email
    action = PrintToScreenFileOrNeither("Print list of adults without email")
    if action == 'y':
        for this_list in map_d.keys():
            print('Hub ID = ', this_list)
            for this_person in map_d[this_list]:
                this_person.PrintWithHubs()
            print('\n-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-\n')
    elif action == 'f':
        import_file_tools.CreateByHubFile(map_d, hub_map_d, "emailless_by_hub")



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
    ##
    ## perform the action
    orphan_families = actions.FindOrphans(directory)
    ##
    ## show user how many were found
    print("Found %d families without adults out of %d families" % \
          (len(orphan_families), len(directory)))
    ##
    ## if any orphans were found, prompt user whether to show on screen
    if len(orphan_families) > 0:
        if PrintToScreenOrNot() == 'y':
            for entry_family in orphan_families:
                entry_family.Print()
                print(STDOUT_SEPERATOR)
        

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
    ##
    ## perform the action
    childless_families = actions.FindChildless(directory)
    ##
    ## show user how many were found
    print("Found %d families without children out of %d families" % \
          (len(childless_families), len(directory)))
    ##
    ## if any orphans were found, prompt user whether to show on screen
    if len(childless_families) > 0:
        if PrintToScreenOrNot() == 'y':
            for entry_family in childless_families:
                entry_family.Print()
                print(STDOUT_SEPERATOR)


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
    ##
    ## perform the action
    hubless_adults, hubless_children = actions.FindHubless(arg_list)
    ##
    ## show user number of adults not in hubs, and prompt whether to show on screen
    print("Found %d adults who are not in at least one classroom hub." % len(hubless_adults))
    if len(hubless_adults) > 0:
        if PrintToScreenOrNot() == "y":
            for this_person in hubless_adults:
                print("%s %s <%s>" % (this_person.first_name, this_person.last_name, this_person.hubs))
    ##
    ## show user number of children not in hubs, and prompt whether to show on screen
    print("Found %d children who are not in a classroom hub." % len(hubless_children))
    if len(hubless_children) > 0:
        if PrintToScreenOrNot() == "y":
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
    ##
    ## perform the action
    hubful_children = actions.FindChildrenInMultipleClassroom(arg_list)
    ##
    ## show user the number of students who are in multiple classroom hubs,
    ## and prompt whether to show them on the screen.
    print("Found %d students who are not in more than one classroom hub." % len(hubful_children))
    if len(hubful_children) > 0:
        if PrintToScreenOrNot() == "y":
            for this_person in hubful_children:
                print("%s %s <%s>" % (this_person.first_name, this_person.last_name, this_person.hubs))


def ListShowAndAct(this_list, statement, file_name, hide_email=True):
    print(len(this_list), statement)
    if len(this_list) > 0:
        action = PrintToScreenFileOrNeither('Print list to screen or file')
        if action == "y":
            for this_person in this_list:
                if hide_email:
                    this_person.Print()
                else:
                    this_person.PrintWithEmail()
        elif action == "f":
            import_file_tools.CreateFileFromPeople(this_list, file_name)


def FindAdultsWithoutAccounts(arg_list):
    """menu.FindAdultsWithoutAccounts
    INPUTS:
    - directory -- list of families from a MemberHub directory dump.
    OUTPUTS:
    Provides the option to write to standard output or to a file the list of adults who
    do not have accounts, separated by whether their profile has an email address or not.
    """
    ##
    ## perform the action
    teacher_without_email, no_account_without_email, teacher_with_no_account, no_account_with_email, without_email_map, with_email_map = \
        actions.FindAdultsWithoutAccounts(arg_list)
    ##
    ## show the user the number of adults with neither account nor email, and prompt
    ## whether to print to the screen or save to a file.
    ListShowAndAct(this_list = teacher_without_email,
                   statement = "people found who work for the school without accounts or emails.",
                   file_name = "teachers_without_email")

    ListShowAndAct(this_list = no_account_without_email,
                   statement = "adults found without accounts or emails.",
                   file_name = "no_account_without_email")

    ##
    ## show the user the number of adults with no account but with email, and prompt
    ## whether to print to the screen or save to a file.
    ListShowAndAct(this_list = teacher_with_no_account,
                   statement = "people found who work for the school without accounts, but with emails.",
                   file_name = "teachers_without_account",
                   hide_email = False)

    ListShowAndAct(this_list = no_account_with_email,
                   statement = "adults found without accounts, but with emails.",
                   file_name = "no_account_with_email",
                   hide_email = False)



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
    ## perform the action
    entriless = actions.PrintNotInDirectory(arg_list)
    ##
    ## tell the user how many entriless families were found
    print("Found %d people on the roster who were not in the directory" % len(entriless))
    if len(entriless) == 0:
        return
    ##
    ## ask the user how to output the list of entriless families
    action = PrintToScreenFileOrNeither('Print list to screen or file')
    ##
    ## output to the screen
    if action == 'y':
        for entry in entriless:
            print(STDOUT_SEPERATOR)
            print("Did not find this family from the roster in the directory: ")
            entry.Print()
    ##
    ## output to a file
    elif action == 'f':
        import_file_tools.CreateFileFromFamily(entriless)



def FindParentChildrenHubMismatches(directory):
    """menu.FindParentChildrenHubMismatches
    INPUTS:
    - directory -- list containing the MemberHub directory families
    OUTPUTS:
    - at user prompt, prints to standard output the family members and their
      hubs that have adults who are not members of all their children's hubs
    ASSUMPTIONS:
    - None.
    """
    ##
    ## perform the action
    mismatches = actions.FindParentChildrenHubMismatches(directory)
    ##
    ## show user the number of families with adults who are not in all their
    ## children's hubs, and prompt whether to show them on the screen.
    print("Found %d families that have at least one adult who is not in all thier children's classroom hubs." % \
          len(mismatches))
    if len(mismatches) > 0:
        if PrintToScreenOrNot() == "y":
            for this_family in mismatches:
                this_family.PrintWithHubs()
                print(STDOUT_SEPERATOR)


def FindUnsedErrata(arg_list):
    """menu.FindUnsedErrata
    INPUTS:
    - arg_list - menu requires the function to have an input to match template, but this
                 is not used
    OUTPUTS:
    Prints the roster errata entries that are no longer found in the roster, and can be
    removed.
    ASSUMPTIONS:
    - none
    """
    ##
    ## perform the action
    unused_errata, all_errata = actions.FindUnsedErrata()
    ##
    ## show user the number of families with adults who are not in all their
    ## children's hubs, and prompt whether to show them on the screen.
    print("Found %d unused errata." % len(unused_errata))
    if len(unused_errata) > 0:
        if PrintToScreenOrNot() == "y":
            for entry in unused_errata:
                print(entry, '|', all_errata[entry])
                print(STDOUT_SEPERATOR)



def MakePrompt(choices):
    guts = '\n'.join(['(%s) - %s' % (choice, choices[choice]['Description'])
                      for choice in sorted(choices.keys())])
    return '\n' + STDOUT_SEPERATOR + '\nChoose:\n' + guts + '\nOr press <enter> to quit.  Your selection --> '

def RunMenu(master_directory, master_roster, master_map):
    """Runs the user interface for dictionary manipulation."""
    ##
    ## The choices dictionary has function names for values.
    choices = {'a': {'Description':'Find Missing Email',
                     'Function'   :FindMissingEmail,
                     'Arg'        :[master_directory, master_map]},
               'b': {'Description':'Find Orphans',
                     'Function'   :FindOrphans,
                     'Arg'        :master_directory},
               'c': {'Description':'Find Childless',
                     'Function'   :FindChildless,
                     'Arg'        :master_directory},
               'd': {'Description':'Find Not In Classroom Hub',
                     'Function'   :FindHubless,
                     'Arg'        :[master_directory, master_map]},
               'e': {'Description':'Find Adults without Accounts',
                     'Function'   :FindAdultsWithoutAccounts,
                     'Arg'        :[master_directory, master_map]},
               'f': {'Description':'Find Not in Directory',
                     'Function'   :PrintNotInDirectory,
                     'Arg'        :[master_directory, master_roster]},
               'g': {'Description':'Find Adults/Children Hub Mismatches',
                     'Function'   :FindParentChildrenHubMismatches,
                     'Arg'        :master_directory},
               'h': {'Description':'Find Unused Errata',
                     'Function'   :FindUnsedErrata,
                     'Arg'        :'Unused String'},
               'i': {'Description':'Find students who are in multipe classroom hubs',
                     'Function'   :FindChildrenInMultipleClassroom,
                     'Arg'        :[master_directory, master_map]}}

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
    master_map       = hub_map_tools.ReadHubMap()
    print(STDOUT_SEPERATOR)
    master_directory = directory_tools.ReadDirectory(master_map)
    print(STDOUT_SEPERATOR)
    master_roster    = roster_tools.ReadRoster(master_map)
    RunMenu(master_directory, master_roster, master_map)

if __name__ == '__main__':
    main()
