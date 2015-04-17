#!/usr/bin/env python
"""This program inputs the map of elementary school teachers to hub names.
It assumes the presence of a file called 'hub_map.csv' in the directory from
which the program is executed.
It also assumes 'hub_map.csv' was created by saving an Excel spreadsheet as
a "Windows Comma Separated (.csv)" file (Excel offers other CSV options that
do not work with this program).
"""

def ReadMap():
    map_d = {}   # empty dictionary
    count = 0

    try:
        open_file = open('hub_map.csv')

        for line in open_file:
            fields = line.split(',')
            ## be sure to strip the '\r\n' that Excel adds at the end of lines
            map_d.update({fields[0]:fields[-1][:-2]})
            count += 1

        print "%d hub IDs read and processed." % count

    finally:
        open_file.close()
        
    return map_d

def PrintMap(map_d):
    print map_d

        

def main():
    map_d = ReadMap()
    PrintMap(map_d)

if __name__ == '__main__':
    main()
