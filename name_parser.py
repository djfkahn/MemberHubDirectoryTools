#!/usr/bin/env python

import roster

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
    conjunction = None
    if full_name.find(" and ") > 0:
        conjunction = " and "
    elif full_name.find(" And ") > 0:
        conjunction = " And "
    elif full_name.find(" & ") > 0:
        conjunction = " & "

    if conjunction != None:
        full_name_list = full_name.split(conjunction)

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
    second_name = ParseType3Name(name_list[1])
    first_name  = [{'first': name_list[0].strip(),
                    'last' : second_name[0]['last']}]
    return first_name + second_name

def ParseType2Name(name_list):
    """name_parser.ParseType2Name
    Puprpose:  Parses a name field with the format <first1> <last1> <conjunction> <first2> <last2>
    INPUTS:
    name_list -- A list of names in format ['<first1> <last1>','<first2> <last2>']
    OUTPUTS:
    names     -- A list of name dictionaries.  Each name dictionary contains
                 a single person's first and last names.
    """
    answer  = ParseType3Name(name_list[0])
    answer += ParseType3Name(name_list[1])
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
