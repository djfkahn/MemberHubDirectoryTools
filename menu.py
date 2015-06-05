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

def FindMissingEmail(directory):
    """menu.FindMissingEmail
    INPUTS:
    - directory -- list containing the MemberHub directory families
    OUTPUTS:
    Prints to standard output the adults in the directory who do not have an
    email address associated with their entry.
    ASSUMPTIONS:
    None.
    """
    adult_count = no_email_count = 0
    for entry_family in directory:
        for adult in entry_family.adults:
            adult_count += 1
            if adult.DoesNotListEmailAddress():
                print "The entry for this person does not have an email address:",
                adult.Print()
                no_email_count += 1

    print "Found %d out of %d adults with missing email addresses" % \
          (no_email_count, adult_count)

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
            print "The entry for this family does not identify parents:",
            entry_family.Print()
            orphan_count += 1
            
    print "Found %d families without adults out of %d families" % \
          (orphan_count, family_count)

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
            print "The entry for this family does not identify children:",
            entry_family.Print()
            childless_count += 1
            
    print "Found %d families without children out of %d families" % \
          (childless_count, family_count)

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
    directory = arg_list[0]
    map_d     = arg_list[1]
    hubless   = []

    child_count = adult_count = 0

    for directory_family in directory:
        for adult in directory_family.adults:
            if not hub_map_tools.IsAnyHubClassroomHub(map_d, adult.hubs):
                print "Found adult not in a classroom hub.  Current hubs = (%s).  Name = " % adult.hubs,
                adult.Print()
                adult_count += 1
                hubless.append(adult)
        
        for child in directory_family.children:
            if not hub_map_tools.IsAnyHubClassroomHub(map_d, child.hubs):
                print "Found child not in a classroom hub.  Current hubs =  (%s).  Name = " % child.hubs,
                child.Print()
                child_count += 1
                hubless.append(child)

    print "Found %d children who are not in a classroom hub." % child_count
    print "Found %d adults who are not in at least one classroom hub." % adult_count
    
    return hubless

def PrintHubless(arg_list):
    discard = FindHubless(arg_list)

def MakeImportForHubless(arg_list):
    """menu.MakeImportForHubless
    INPUTS:
    - directory -- dictionary containing the MemberHub directory
    - roster    -- dictionary containing the school roster
    - map_d     -- dictionary mapping teacher names to hub IDs
    OUTPUTS:
    Prints to standard output the names in the directory who are not members of
    at least one classroom hub.
    Creates a comma-separated text file that can be imported into MemberHub to assign
    hub IDs to existing directory entries.
    ASSUMPTIONS:
    None.
    """
    directory   = arg_list[0]
    map_d       = arg_list[1]
    roster      = arg_list[2]
    hubless     = FindHubless(arg_list)
    update_hubs = []

    hubed_count = hubless_count = 0

    for hubless_person in hubless:
        for roster_family in roster:
            found_person = roster_family.FindPersonInFamily(hubless_person)
            if not found_person == None:
                hubless_person.hubs = found_person.hubs
                update_hubs.append(hubless_person)
                hubed_count += 1
                break
        else:
            print "Did not find match for this person in the roster:",
            hubless_person.Print()
            hubless_count += 1

    print "Processed %d entries that were not in any classroom hub." % len(hubless)
    print "Was able to find classroom hubs for %d entries." % hubed_count
    print "Was not able to find classroom hubs for %d entries." % hubless_count

    import_file_tools.CreateHublessImportFile(update_hubs)

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
                break

        else:
            print "Did not find this family from the roster in the directory:",
            roster_family.Print()
            entriless.append(roster_family)

    print "Found %d people on the roster who were not in the directory" % len(entriless)
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
    directory = arg_list[0]
    roster    = arg_list[1]
    map_d     = arg_list[2]
    entriless = FindEntriless(arg_list)

    import_file_tools.CreateNewMemberImport(entriless)

def MakePrompt(choices):
    choice_list = sorted(choices)
    guts = '\n'.join(['(%s)%s' % (choice[0], choice[1:])
                      for choice in choice_list])
    return 'Choose:\n' + guts + '\nOr press <enter> to quit '

def RunMenu(directory, roster, map_d):
    """Runs the user interface for dictionary manipulation."""
    # The choices dictionary has function names for values.
    choices = {'1 - Find Missing Email':
                    {'Function':FindMissingEmail,'Arg':directory},
               '2 - Find Orphans':
                    {'Function':FindOrphans,'Arg':directory},
               '3 - Find Childless':
                    {'Function':FindChildless,'Arg':directory},
               '4 - Find Not In Classroom Hub':
                    {'Function':PrintHubless,'Arg':[directory,map_d]},
               '5 - Make Import File for Not In Classroom Hub':
                    {'Function':MakeImportForHubless,'Arg':[directory,map_d,roster]},
               '6 - Find Not in Directory':
                    {'Function':PrintNotInDirectory,'Arg':[directory,roster]},
               '7 - Make Import File for Not In Directory':
                    {'Function':MakeImportNotInDirectory,'Arg':[directory,roster,map_d]}}
    
    prompt = MakePrompt(choices)

    while True:
        raw_choice = raw_input(prompt)
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
            print '%s is not an acceptible choice.' % raw_choice

        
def main():
    directory = directory_tools.ReadDirectory()
    roster    = roster_tools.ReadRoster()
    map_d     = hub_map_tools.ReadMap()
    RunMenu(directory, roster, map_d)

if __name__ == '__main__':
    main()
