#!/usr/bin/env python
"""This program inputs a MemberHub directory dump, and analyzes it.
"""
import family

def ReadRoster():
    roster        = []   # empty list
    student_count = 0

    file_name = raw_input('Enter name of roster comma-separated text file: ')
    print file_name
    try:
        open_file = open(file_name)
        raw_line = open_file.readline()

        for line in open_file:
            # each line read represents one student
            student_count += 1

            # process the line without the trailing '\r\n' that Excel adds
            fields = line[:-2].split(',')
            
            new_family = family.Family()
            new_family.CreateFromRoster(fields)

            # if new_family is the same as a family already in the roster, then combine
            # families.  Otherwise, append new_family at the end of the roster.
            for family in roster:
                if family.IsSameFamily(new_family):
                    family.CombineWith(new_family)
                    break
            else:
                roster += [new_family]

        print "%d students processed %d families." % (student_count, len(roster))

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
