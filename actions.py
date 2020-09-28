"""Defines the main menu module for a program that inputs a MemberHub directory dump,
a school roster, and a hub map to perform analyses on the MemberHub directory.
"""

import roster_tools
import hub_map_tools
import family
# import person
import roster



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

    return total_adult_count, no_email_person, no_email_family, partial_family, map_d




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

    return orphan_families



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

    ##
    ## loop over all families in the directory to find childless families
    for entry_family in local_dir:
        if entry_family.IsChildless():
            childless_families.append(entry_family)

    return childless_families



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

    return hubless_adults, hubless_children




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

    return hubful_children



def FindAdultsWithoutAccounts(arg_list):
    """menu.FindAdultsWithoutAccounts
    INPUTS:
    - directory -- list of families from a MemberHub directory dump.
    - hub_map   -- the school's hub map
    OUTPUTS:
    Provides the option to write to standard output or to a file the list of adults who
    do not have accounts, separated by whether their profile has an email address or not.
    """
    ##
    ## make copy of the argument so it is not accidentally modified,
    ## and initialize method variables
    local_dir                = arg_list[0].copy()
    local_hub_map            = arg_list[1].copy()
    no_account_with_email    = []
    no_account_without_email = []
    teacher_with_no_account  = []
    teacher_without_email    = []

    ##
    ## create a dictionary of classroom hubs that will hold lists of
    ## adults without accounts
    with_email_map    = hub_map_tools.CreateEmptyHubDictionary(local_hub_map)
    without_email_map = hub_map_tools.CreateEmptyHubDictionary(local_hub_map)

    ##
    ## loop over all the families in the directory, and find those with
    ## no accounts, and separate those between those with an email and those
    ## without an email.
    for this_family in local_dir:
        for this_adult in this_family.adults:
            if this_adult.account_created == "":
                if this_adult.DoesNotListEmailAddress():
                    if this_adult.IsWithSchool():
                        teacher_without_email.append(this_adult)
                    else:
                        no_account_without_email.append(this_adult)
                        for hub in this_adult.hubs:
                            if hub in without_email_map.keys():
                                without_email_map[hub].append(this_adult)
                ##
                ## this adult does have an email, so check if they are with the school
                elif this_adult.IsWithSchool():
                    teacher_with_no_account.append(this_adult)
                ##
                ## this adult does have an email and is not with the school, so add to parents
                ## without accounts but with emails
                else:
                    no_account_with_email.append(this_adult)
                    for hub in this_adult.hubs:
                        if hub in with_email_map.keys():
                            with_email_map[hub].append(this_adult)

    return teacher_without_email, no_account_without_email, teacher_with_no_account, no_account_with_email, without_email_map, with_email_map



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

    return entriless



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

    return mismatches


def FindUnsedErrata(errata_file='roster_errata.csv', roster_file=None):
    """menu.FindUnsedErrata
    INPUTS:
    - none
    OUTPUTS:
    Prints the roster errata entries that are no longer found in the roster, and can be
    removed.
    ASSUMPTIONS:
    - none
    """
    ##
    ## Read the adults from the most recent roster file
    adults_list = roster_tools.ReadRosterAdultsFromMostRecent(file_name=roster_file)

    ##
    ## Next, instantiate a Roster class, which includes the default errata, and retrieve
    ## that dictionary
    temp   = roster.Roster(show_errors='y', file_name=errata_file)
    all_errata = temp.GetErrata()
    
    ##
    ## for each error listed in the errata, look for it in the adults list
    unused_errata = []
    for entry in all_errata.keys():
        if entry not in adults_list:
            unused_errata.append(entry)
    
    return unused_errata, all_errata



