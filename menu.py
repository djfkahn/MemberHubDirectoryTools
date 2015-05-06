#!/usr/bin/env python
"""This program inputs a MemberHub directory dump, and analyzes it.
"""

import directory_tools
import roster_tools
import hub_map_tools
import import_file_tools

def ContainsName(name_field, first_name, last_name):

    found_name = name_field.find(first_name) >= 0 and \
                 name_field.find(last_name) >= 0

    return found_name       

def IsSameName(from_directory, from_roster):
    is_same = False
    
    if from_roster["family_relation"][:5].lower() == "child":
        
        is_same = from_directory["last_name"]  == from_roster["last_name"] and \
                  from_directory["first_name"] == from_roster["first_name"]

    else:

        is_same = ContainsName(from_roster["name_field"],
                               from_directory["first_name"],
                               from_directory["last_name"])

    return is_same
    
    
def FindMissingEmail(direct_d):
    """FindMissingEmail finds all the adults in the directory that do not have
an email address associated with their entry.
"""
    adult_count = no_email_count = 0
    for entry in direct_d:
        if direct_d[entry]["family_relation"][:5].lower() == "adult":
            adult_count += 1
            if direct_d[entry]["email"] == "":
                no_email_count += 1

    print "Found %d out of %d adults with missing email addresses" % \
          (no_email_count, adult_count)

def FindOrphans(direct_d):
    """FindOrphans finds all the children in the directory that do not have an
adult associated with them.
"""
    child_count = orphan_count = 0

    for entry in direct_d:
        if direct_d[entry]["family_relation"][:5].lower() == "child":
            child_count += 1
            if direct_d[entry]["parents"] == "":
                orphan_count += 1
            
    print "Found %d children without adults in the family out of %d children" % \
          (orphan_count, child_count)

def FindChildless(direct_d):
    print "This functionality has not been added yet"

def FindHubless(arg_list):
    direct_d = arg_list[0]
    map_d    = arg_list[1]

    child_count = adult_count = 0

    for entry in direct_d:
        if not hub_map_tools.IsAnyHubClassroomHub(map_d, direct_d[entry]["hubs"]):
            print "%s %s is not in a classroom hub (%s)" % (direct_d[entry]["first_name"],
                                                            direct_d[entry]["last_name"],
                                                            direct_d[entry]["hubs"])
            if direct_d[entry]["family_relation"][:5].lower() == "child":
                child_count += 1
            else:
                adult_count += 1

    print "Found %d children who are not in at least one hub" % child_count
    print "Found %d adults who are not in at least one hub" % adult_count

def MakeImportForHubless(arg_list):
    direct_d = arg_list[0]
    roster_d = arg_list[1]
    map_d    = arg_list[2]
    update_d = {}

    processed_count = hubed_count = hubless_count = 0

    for entry in direct_d:
        if not hub_map_tools.IsAnyHubClassroomHub(map_d, direct_d[entry]["hubs"]):
            print "%s %s is not in a classroom hub (%s)" % (direct_d[entry]["first_name"],
                                                            direct_d[entry]["last_name"],
                                                            direct_d[entry]["hubs"])
            processed_count += 1
            for person in roster_d:
                if IsSameName(direct_d[entry], roster_d[person]):

                    temp = direct_d[entry]
                    hub_names = temp["hubs"] + "|"
                    for teacher in (roster_d[person]["teacher"].split('|')):
                        hub_names += map_d[teacher] + "|"
                        
                    temp.update({"hubs":hub_names})
                    update_d.update({processed_count:temp})
                    hubed_count += 1
                    break
            else:
                print "Did not find match for %s %s in the roster." % \
                          (direct_d[entry]["first_name"], direct_d[entry]["last_name"])
                hubless_count += 1

    print "Processed %d entries that were not in any classroom hub." % processed_count
    print "Was able to find classroom hubs for %d entries." % hubed_count
    print "Was not able to find classroom hubs for %d entries." % hubless_count

    import_file_tools.CreateHublessImportFile(update_d)
            
def FindEntriless(arg_list):
    direct_d = arg_list[0]
    roster_d = arg_list[1]

    entriless_count = 0

    for person in roster_d:
        
        for entry in direct_d:
            if IsSameName(direct_d[entry], roster_d[person]):
                print "Found %s %s in directory." % \
                      (roster_d[person]["first_name"], roster_d[person]["last_name"])
                break
            
        else:
            print "Did not find match for %s %s." % \
                  (roster_d[person]["first_name"], roster_d[person]["last_name"])
            entriless_count += 1

    print "Found %d people on the roster who were not in the directory" % entriless_count


def MakeImportNotInDirectory(arg_list):
    direct_d = arg_list[0]
    roster_d = arg_list[1]
    map_d    = arg_list[2]
    update_d = {}

    entriless_count = 0

    for person in roster_d:
        for entry in direct_d:
            if IsSameName(direct_d[entry], roster_d[person]):
                break
            
        else:
            hub_names = "|"
            for teacher in (roster_d[person]["teacher"].split('|')):
                hub_names += map_d[teacher] + "|"
            update_d.update({entriless_count:{"last_name":roster_d[person]["last_name"],
                                              "first_name":roster_d[person]["first_name"],
                                              "family_relation":roster_d[person]["family_relation"],
                                              "person_id":" ",
                                              "hubs":hub_names}})
            entriless_count += 1

    print "Found %d people on the roster who were not in the directory" % entriless_count

    import_file_tools.CreateNewMemberImport(update_d)
            
def MakePrompt(choices):
    choice_list = sorted(choices)
    guts = '\n'.join(['(%s)%s' % (choice[0], choice[1:])
                      for choice in choice_list])
    return 'Choose:\n' + guts + '\nOr press <enter> to quit '

def RunMenu(direct_d, roster_d, map_d):
    """Runs the user interface for dictionary manipulation."""
    # The choices dictionary has function names for values.
    choices = {'1 - Find Missing Email':{'Function':FindMissingEmail,'Arg':direct_d},
               '2 - Find Orphans':{'Function':FindOrphans,'Arg':direct_d},
               '3 - Find Childless':{'Function':FindChildless,'Arg':direct_d},
               '4 - Find Not In Hub':{'Function':FindHubless,'Arg':[direct_d,map_d]},
               '5 - Make Import File for Not In Hub':{'Function':MakeImportForHubless,
                                                      'Arg':[direct_d,roster_d,map_d]},
               '6 - Find Not in Directory':{'Function':FindEntriless,
                                            'Arg':[direct_d,roster_d]},
               '7 - Make Import File for Not In Directory':
                                           {'Function':MakeImportNotInDirectory,
                                            'Arg':[direct_d,roster_d,map_d]}}
    
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
    direct_d = directory_tools.ReadDirectory()
    roster_d = roster_tools.ReadRoster()
    map_d    = hub_map_tools.ReadMap()
    RunMenu(direct_d, roster_d, map_d)

if __name__ == '__main__':
    main()
