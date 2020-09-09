#!/usr/bin/env python
"""This module defines the Roster class.
"""

class Roster:
    """Class Roster
    This class defines a roster storage class
    ATTRIBUTES
    table            - A list of roster Families
    errata           - A dictionary of known roster errors and their corrected values
    hideErrataOutput - A flag indicating whether messages should be printed when roster errors are identified
    """

    def __init__(self):
        # Initialize the roster table to an empty set
        self.table            = []
        # Ask whether to show errors, and then hide the errata output as the opposite of that answer
        show_errors = " "
        while show_errors not in (None, '', 'y', 'Y'):
            show_errors       = input("Print corrected roster errors to the screen? (press <enter> for \"no\", press \"y\" for \"yes\"): ")
    
        self.hideErrataOutput = not show_errors
        # Initialize the errata dictionary to the contents of 'roster_errata.csv'
        self.errata           = {}
        try:
            open_file = open('roster_errata.csv')
            for line in open_file:
                if line[0] != "#":
                    fields = line.split('|')
                    self.errata.update({fields[0]:fields[-1].strip("\r\n")})
        finally:
            open_file.close()


    def __len__(self):
        return len(self.table)

    def GetRoster(self):
        return self.table

    def GetErrata(self):
        return self.errata

    def Hide (self):
        return self.hideErrataOutput

    def append(self, new_family):
        self.table.append(new_family)

    def ApplyErrata(self, full_name):
        """Roster.ApplyErrata
        Purpose:  Replaces roster name fields with known errors with the correct name fields.
        INPUTS:
        - full_name -- The raw parent name field from the roster.
        OUTPUTS:
        - corrected full_name if this fields is known to be in error
        - otherwise, the unmodified input full_name
        ASSUMPTIONS:
        - none.
        """
        if full_name in self.errata.keys():
            if not self.hideErrataOutput:
                print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-")
                print("Found Errata for: " + full_name)
                print("Will use " + self.errata[full_name] + " instead.")
            return self.errata[full_name]

        return full_name
