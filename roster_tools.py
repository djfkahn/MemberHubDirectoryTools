#!/usr/bin/env python
"""This program inputs a MemberHub directory dump, and analyzes it.
"""

def FindEntry(roster_d, name_field):
    for entry in roster_d.keys():
        if roster_d[entry]["name_field"] == name_field:
            return entry
    else:
        return -1

def AddEntry(roster_d,
             last_name,
             first_name,
             grade,
             teacher,
             name_field,
             family_relation):
    
    new_entry = {"last_name":last_name,
                 "first_name":first_name,
                 "grade":grade,
                 "teacher":teacher,
                 "name_field":name_field,
                 "family_relation":family_relation,
                 "person_id":" "}
    roster_d.update({len(roster_d)+1:new_entry})

    return roster_d

def AddEntryAtCount(roster_d,
                    last_name,
                    first_name,
                    grade,
                    teacher,
                    name_field,
                    family_relation,
                    count):

    # create a roster with the entries up to the insertion point,
    # and add the new entry at the insertion point
    first_roster = {}
    for entry in roster_d.keys()[:count]:
        first_roster.update({entry:roster_d[entry]})
    
    first_roster = AddEntry(first_roster, last_name, first_name, grade,
                            teacher, name_field, family_relation)

    # shift the remaining entries by one
    second_roster = {}
    for entry in roster_d.keys()[count:]:
        second_roster.update({entry+1:roster_d[entry]})

    # add the two parts of the roster together
    first_roster.update(second_roster)

    return first_roster

def ReadRoster():
    roster_d = {}   # empty dictionary
    count = student_count = adult_count = 0

    # 
    file_name = raw_input('Enter name of roster file: ')
    print file_name
    try:
        open_file = open(file_name)
        raw_line = open_file.readline()

        for line in open_file:
            # process the line without the trailing '\r\n' that Excel adds
            fields = line[:-2].split(',')

            # for elementary school (< 6th grade) teacher name is retained
            # for middle school, teacher name is replaced with grade level
            if int(fields[2]) < 6:
                teacher = fields[4]
            else:
                teacher = fields[2]

            # skip the parent name extraction, if they are already in
            # the adult roster, but extract them first to keep the parent-
            # child relationship in a family
            entry_found_at = FindEntry(roster_d, fields[3])
            if entry_found_at >= 0:

                # increment the insertion after point, while the next entry
                # is part of the same parent group, but add the teacher name to
                # the adults
                child_count = 1
                while  roster_d[entry_found_at]["name_field"] == fields[3]:
                    
                    if roster_d[entry_found_at]["family_relation"][:5] == "Adult":
                        
                        roster_d[entry_found_at]["teacher"] += "|" + teacher

                    else: # family_relation is child, so increment child count

                        child_count += 1
                            
                    if entry_found_at < len(roster_d) and \
                       roster_d[entry_found_at+1]["name_field"] == fields[3]:
                        
                        entry_found_at += 1
                        
                    else:
                        break
            
                # found a duplicate parent, so do not enter new parent,
                # but find the right location to insert child
                roster_d = \
                    AddEntryAtCount (roster_d = roster_d,
                                     last_name = fields[0],
                                     first_name = fields[1],
                                     grade = fields[2],
                                     teacher = teacher,
                                     name_field = fields[3],
                                     family_relation = "Child%d" % child_count,
                                     count = entry_found_at) 

            else: # found first child of a parent set

                parent_count = 1
                parent_num = ""
                parents = fields[3].split(" and ")
                # if parents have same last name, then there is only one name
                # before the first "and"
                if len(parents[0].split(" ")) == 1:
                    last_name = parents[-1].split(" ")[-1]            
                    for name in parents:
                        parent = name.split(' ')
                        roster_d = \
                            AddEntry (roster_d = roster_d,
                                      last_name = last_name,
                                      first_name = parent[0],
                                      grade = fields[2],
                                      teacher = teacher,
                                      name_field = fields[3],
                                      family_relation = "Adult"+parent_num)
                        # prepare the parent_tag for the next parent
                        parent_count += 1
                        parent_num = str(parent_count)

                        adult_count += 1
                        count += 1
                # each parent as a unique first and last name
                else:
                    for name in parents:
                        parent = name.split(' ')
                        roster_d = \
                            AddEntry (roster_d = roster_d,
                                      last_name = parent[-1],
                                      first_name = " ".join(parent[0:-1]),
                                      grade = fields[2],
                                      teacher = teacher,
                                      name_field = fields[3],
                                      family_relation = "Adult"+parent_num)
                        # prepare the parent_tag for the next parent
                        parent_count += 1
                        parent_num = str(parent_count)

                        adult_count += 1
                        count += 1

                # store the student information
                roster_d = \
                    AddEntry (roster_d = roster_d,
                              last_name = fields[0],
                              first_name = fields[1],
                              grade = fields[2],
                              teacher = teacher,
                              name_field = fields[3],
                              family_relation = "Child1")
                student_count += 1
                count += 1
                
        print "%d students processed, with %d adutls." % (student_count, adult_count)

    finally:
        open_file.close()
        
    return roster_d

def PrintEntries(roster_d):
    num_to_print = raw_input('Enter number of entries to print: ')
    for x in roster_d.keys()[:int(num_to_print)]:
        print roster_d[x]

        

def main():
    roster_d = ReadRoster()
    PrintEntries(roster_d)

if __name__ == '__main__':
    main()
