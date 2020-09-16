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
import roster

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
    ## extract copies of the arguments so they are not accidentally modified,
    ## and initialize method variables
    directory         = arg_list[0].copy()
    hub_map_d         = arg_list[1].copy()
    total_adult_count = 0
    no_email_person   = []
    no_email_family   = []
    partial_family    = []

    ##
    ## create a dictionary of classroom hubs that will hold lists of
    ## adults without emails
    map_d = hub_map_tools.CreateEmptyHubDictionary(hub_map_d)

    ##
    ## loop over all the families in the directory
    for entry_family in directory:
        ##
        ## add the number of adults in this family to the count of all the adults
        ## in the directory
        total_adult_count += len(entry_family.adults)

        ##
        ## for each family, count number of adults without emails
        this_family_no_email_count = 0
        
        ##
        ## loop over each adult in the family
        for adult in entry_family.adults:
            ##
            ## check whether this adult DOES NOT an email address
            if adult.DoesNotListEmailAddress():
                ##
                ## found adult without an email, so add to list of persons without email
                no_email_person.append(adult)
                ##
                ## increment the number of adults in this family without email
                this_family_no_email_count += 1
                ##
                ## loop over all the adult's hubs, and add them to the hub
                ## dictionary
                for hub in adult.hubs:
                    if hub in map_d.keys():
                        map_d[hub].append(adult)

        ##
        ## if this family's no email count is the same as number of adults,
        ## then append this family to the no_email_family list
        if this_family_no_email_count == len(entry_family.adults):
            no_email_family.append(entry_family)
        ##
        ## otherwise, if fewer adults do not have email than are in the family
        ## then append this family to the partial_family list
        elif this_family_no_email_count > 0:
            partial_family.append(entry_family)

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
        print(map_d)
    elif action == 'f':
        import_file_tools.CreateEmaillessByHubFile(map_d, hub_map_d, "emailless_by_hub")



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
    ## make copy of the argument so it is not accidentally modified,
    ## and initialize method variables
    local_dir       = directory.copy()
    orphan_families = []

    ##
    ## loop over all families in the directory to find orphan families
    for entry_family in local_dir:
        if entry_family.IsOrphan():
            orphan_families.append(entry_family)

    ##
    ## show user how many were found
    print("Found %d families without adults out of %d families" % \
          (len(orphan_families), len(local_dir)))
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
    ## make copy of the argument so it is not accidentally modified,
    ## and initialize method variables
    local_dir          = directory.copy()
    childless_families = []
    family_count = childless_count = 0

    ##
    ## loop over all families in the directory to find childless families
    for entry_family in local_dir:
        if entry_family.IsChildless():
            childless_families.append(entry_family)

    ##
    ## show user how many were found
    print("Found %d families without children out of %d families" % \
          (len(childless_families), len(local_dir)))

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
    ## extract copies of the arguments so they are not accidentally modified,
    ## and initialize method variables
    directory        = arg_list[0].copy()
    map_d            = arg_list[1].copy()
    hubless_adults   = []
    hubless_children = []

    ##
    ## loop over all the families to find any adults or children who are not
    ## in at least one classroom hub
    for directory_family in directory:
        for adult in directory_family.adults:
            if not hub_map_tools.IsAnyHubClassroomHub(map_d, adult.hubs):
                hubless_adults.append(adult)

        for child in directory_family.children:
            if not hub_map_tools.IsAnyHubClassroomHub(map_d, child.hubs):
                hubless_children.append(child)

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
    ## extract copies of the arguments so they are not accidentally modified,
    ## and initialize method variables
    directory       = arg_list[0].copy()
    map_d           = arg_list[1].copy()
    hubful_children = []

    ##
    ## loop over all the families in the directory to find children who are in
    ## more than one classroom hub
    for directory_family in directory:
        for child in directory_family.children:
            if hub_map_tools.IsInMultipleClassroomHubs(map_d, child.hubs):
                hubful_children.append(child)

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
            import_file_tools.CreateAccountlessFile(this_list, file_name)


def FindAdultsWithoutAccounts(directory):
    """menu.FindAdultsWithoutAccounts
    INPUTS:
    - directory -- list of families from a MemberHub directory dump.
    OUTPUTS:
    Provides the option to write to standard output or to a file the list of adults who
    do not have accounts, separated by whether their profile has an email address or not.
    """
    ##
    ## make copy of the argument so it is not accidentally modified,
    ## and initialize method variables
    local_dir                = directory.copy()
    no_account_with_email    = []
    no_account_without_email = []
    teacher_with_no_account  = []
    teacher_without_email    = []

    ##
    ## loop over all the families in the directory, and find those with
    ## no accounts, and separate those between those with an email and those
    ## without an email.
    for this_family in local_dir:
        for this_adult in this_family.adults:
            if this_adult.account_created == "":
                if this_adult.email == "":
                    if this_adult.IsWithSchool():
                        teacher_without_email.append(this_adult)
                    else:
                        no_account_without_email.append(this_adult)
                elif this_adult.IsWithSchool():
                    teacher_with_no_account.append(this_adult)
                else:
                    no_account_with_email.append(this_adult)

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
    ## extract copies of the arguments so they are not accidentally modified,
    ## and initialize method variables
    local_dir  = arg_list[0].copy()
    local_rost = arg_list[1].copy()
    entriless  = []

    ##
    ## loop over all the families in the roster...
    for r_family in local_rost:

        ##
        ## ...to compare to each family in the directory
        for d_family in local_dir:
            ##
            ## look for matches between roster and directory families
            if d_family.IsSameFamily(r_family):
                ##
                ## once a family match is found, check whether the roster family has
                ## children who are not in the directory
                if d_family.HasNewChildren(r_family):
                    temp_family = family.Family()
                    temp_family.FormFamilyWithNewChildren(d_family,r_family)
                    entriless.append(temp_family)
                break
        ##
        ## if the roster family was not found in the directory, add it to list of
        ## families without directory entry
        else:
            entriless.append(r_family)

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
        import_file_tools.CreateNewMemberImport(entriless)



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
    ## extract copies of the arguments so they are not accidentally modified,
    ## and initialize method variables
    local_dir  = directory.copy()
    mismatches = []

    ##
    ## loop over all the families in the directory
    for this_family in local_dir:
        ##
        ## accumulate all the family's children's hubs into one list
        children_hubs = []
        for this_child in this_family.children:
            children_hubs.extend(this_child.hubs)

        ##
        ## next, accumulate list of adults who are not members of their
        ## children's hubs
        for this_adult in this_family.adults:
            for child_hub in children_hubs:
                if child_hub not in this_adult.hubs:
                    mismatches.append(this_family)
                    break

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
    ## Read the adults from the most recent roster file
    adults_list = roster_tools.ReadRosterAdultsFromMostRecent()

    ##
    ## Next, instantiate a Roster class, which includes the default errata, and retrieve
    ## that dictionary
    temp   = roster.Roster(show_errors='y')
    errata = temp.GetErrata()
    
    ##
    ## for each error listed in the errata, look for it in the adults list
    unused_errata = []
    for entry in errata.keys():
        if entry not in adults_list:
            unused_errata.append(entry)
    
    ##
    ## show user the number of families with adults who are not in all their
    ## children's hubs, and prompt whether to show them on the screen.
    print("Found %d unused errata." % len(unused_errata))
    if len(unused_errata) > 0:
        if PrintToScreenOrNot() == "y":
            for entry in unused_errata:
                print(entry, '|', errata[entry])
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
                     'Arg'        :master_directory},
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
