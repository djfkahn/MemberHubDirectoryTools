#!/usr/bin/env python

import roster

def SplitNameString(full_name):
    possible_conjunctions = [' and ', ' And ', ' & ', ',']
    split_name            = [full_name.strip()]
    num_found             = 0
    for x in range(len(possible_conjunctions)):
        ##
        ## stop processing the possible conjuction if it cannot be found
        if full_name.find(possible_conjunctions[x]) < 1:
            continue

        ##
        ## split the name by the current conjunction
        split_name = full_name.split(possible_conjunctions[x])
        num_found  = len(split_name)
        
        if num_found > 1:
            ##
            ## full_name was split into more thann one entry, but other conjunctions
            ## may be also be used, so try to split each entry in the split_name array
            ## by the other conjunctions, and insert any found
            for y in range(num_found):
                split_name[y] = split_name[y].strip()
                temp = SplitNameString(split_name[y])
                if len(temp) > 1:
                    split_name.pop(y)
                    for z in reversed(temp):
                        if len(z.strip()) > 0:
                            split_name.insert(y, z.strip())
            ##
            ## and exit the loop
            break
    
    return split_name

def ParseFullName(full_name, rosterC):
    """name_parser.ParseFullName
    Purpose:  Advanced name field Parseting that recognizes most multi-word last
              names.
    INPUTS:
    full_name -- A string containing the name field to be parsed
    OUTPUTS:
    names     -- A list of name dictionaries.  Each name dictionary contains
                 a single person's first and last names.
    ASSUMPTIONS:
    - Each person has both a first and last name.
    - full_name contains no salutations (Mr., Mrs., etc.), suffixes (Sr., Jr., etc.),
      words in parentheses (like nicknames), or initials.
    - Middle names are treated as part of a multi-word first name.
    - Only multi-word last names with certain common prefixes (de, von, st., ect.)
      are recognized.
    - full_name contains either two or one name, following one of these formats:
      1. <first1> <conjunction> <first2> <last>
      2. <first1> <last 1> <conjunction> <first 2> <last2>
      3. <first> <last>
      where <first#> and <last#> may be multi-word names
    """

    ## correct for known errors before proceeding
    full_name = rosterC.ApplyErrata(full_name)

    ## separate the name field based on the conjunction
    full_name_list = SplitNameString(full_name)

    if len(full_name_list) > 1:

        ## if parents have same last name, then there is only one name
        ## before the conjuction
        ## TBD - does not handle the multi-word first name case
        if len(full_name_list[0].split(" ")) == 1:
            answer = ParseType1Name(full_name_list)
        else:
            answer = ParseType2Name(full_name_list)
    else:
        answer = ParseType3Name(full_name)

    return answer


def ParseType1Name(name_list):
    """name_parser.ParseType1Name
    Puprpose:  Parses a name field with the format <first1> <conjunction> <first2> <last>
    INPUTS:
    name_list -- A list of names in format ['<first1>','<first2> <last>']
    OUTPUTS:
    names     -- A list of name dictionaries.  Each name dictionary contains
                 a single person's first and last names.
    """
    ## last name for this type of name field resides in the name after the conjuction
    answer    = ParseType3Name(name_list[-1])
    last_name = answer[0]['last']
    for name in reversed(name_list[:-1]):
        answer.insert(0, {'first': name, 'last' : last_name})
    return answer

def ParseType2Name(name_list):
    """name_parser.ParseType2Name
    Puprpose:  Parses a name field with the format <first1> <last1> <conjunction> <first2> <last2>
    INPUTS:
    name_list -- A list of names in format ['<first1> <last1>','<first2> <last2>']
    OUTPUTS:
    names     -- A list of name dictionaries.  Each name dictionary contains
                 a single person's first and last names.
    """
    answer = []
    for name in name_list:
        answer.extend(ParseType3Name(name))
    return answer

def ParseType3Name(full_name):
    """name_parser.ParseType3Name
    Puprpose:  Parses a name field with the format <first> <last>
    INPUTS:
    name_list -- A list of names in format ['<first> <last>']
    OUTPUTS:
    name      -- A list of a name dictionary containing the person's first and last names.
    """

    last_processed = -1
    fname = ""
    lname = ""

    ## split into words
    name_parts = full_name.strip().split(" ")

    ## concat the first name
    for i in range(len(name_parts)-1):
        word = name_parts[i]
        ## move on to parsing the last name if we find an indicator of a compound
        ## last name (Von, Van, etc) we use i > 0 to allow for rare cases where an
        ## indicator is actually the first name (like "Von Fabella")
        if IsCompoundLastName(word) and i > 0:
            break;

        last_processed = i
        fname += " " + word.title()

    ## check that we have more than 1 word in our string
    if len(name_parts) > 1:
        ## concat the last name
        lname = ""
        for i in range(last_processed+1,len(name_parts)):
            lname += " " + name_parts[i].title()
    else:
        ## otherwise, single word strings are assumed to be first names
        fname = name_parts[0].title()

    ## return the various parts in an array
    name = [{'first': fname.strip(),
             'last' : lname.strip()}]
    return name


## detect compound last names like "Von Fange"
def IsCompoundLastName(word):
    ## these are some common prefixes that identify a compound last names
    prefix_words = ('vere','von','van','de','del','della','di','da','d',\
             'pietro','vanden','du','st.','st','la','ter','o')
    return word.lower() in prefix_words
