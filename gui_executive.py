import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os
import sys
import actions
import directory_tools
import roster_tools
import roster
import hub_map_tools
import import_file_tools



class IORedirector(object):
    '''A general class for redirecting I/O to this Text widget.'''
    def __init__(self,text_area):
        self.text_area = text_area

class StdoutRedirector(IORedirector):
    '''A class for redirecting stdout to this Text widget.'''
    def write(self,str):
        self.text_area.insert("end", str)



class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master["bg"] = "light grey"
        self.pack()
        self.frame_width = 800
        self.input_files_frame    = tk.Frame(master=master,
                                             width=self.frame_width, height= 100, bg="light gray")
        self.input_files_frame.pack(padx=1,pady=5)

        self.input_buttons_frame  = tk.Frame(master=master,
                                             width=self.frame_width, height= 100, bg="light gray")
        self.input_buttons_frame.pack(pady=5)
        self.create_input_file_widgets()

        self.user_selection_frame = tk.Frame(master=master,
                                             width=self.frame_width, height= 90, 
                                             relief=tk.RAISED, borderwidth=1, bg="light gray")
        self.user_selection_frame.pack(pady=5)
        
        self.output_display_frame = tk.Frame(master=master, width=self.frame_width, height= 500,
                                             relief=tk.RAISED, borderwidth=1, bg="light gray")
        self.output_display_frame.pack()
        self.create_text_output_widgets()
        

    def create_input_file_widgets(self):
        
        frame = tk.Frame(master=self.input_files_frame, bg="light gray")
        frame.grid(row=1, column=1)
        label = tk.Label(master=frame, text="Directory File:", bg='light grey')
        label.pack(padx=5, pady=5)

        frame = tk.Frame(master=self.input_files_frame, bg="light gray")
        frame.grid(row=1, column=2)
        label = tk.Button(master = frame, text = "Select Folder", command = self.get_directory_path)
        label.pack(padx=5, pady=5)

        frame = tk.Frame(master=self.input_files_frame, bg="light gray")
        frame.grid(row=1, column=3)
        self.directory_file = ttk.Combobox(master=frame, width=50, values=[])
        self.directory_file.pack(padx=5, pady=5)
        
        frame = tk.Frame(master=self.input_files_frame, bg="light gray")
        frame.grid(row=2, column=1)
        label = tk.Label(master=frame, text="Roster File:", bg='light grey')
        label.pack(padx=5, pady=5)

        frame = tk.Frame(master=self.input_files_frame, bg="light gray")
        frame.grid(row=2, column=2)
        label = tk.Button(master = frame, text = "Select Folder", command = self.get_roster_path)
        label.pack(padx=5, pady=5)

        frame = tk.Frame(master=self.input_files_frame, bg="light gray")
        frame.grid(row=2, column=3)
        self.roster_file = ttk.Combobox(master=frame, width=50, values=[])
        self.roster_file.pack(padx=5, pady=5)
        
        frame = tk.Frame(master=self.input_files_frame, bg="light gray")
        frame.grid(row=3, column=1)
        label = tk.Label(master=frame, text="Hub Map and \nRoster Errata Files:", bg='light grey')
        label.pack(padx=5, pady=5)

        frame = tk.Frame(master=self.input_files_frame, bg="light gray")
        frame.grid(row=3, column=2)
        label = tk.Button(master = frame, text = "Select Folder", command = self.get_hub_map_path)
        label.pack(padx=5, pady=5)

        frame = tk.Frame(master=self.input_files_frame, bg="light gray")
        frame.grid(row=3, column=3)
        self.hub_map_file = ttk.Combobox(master=frame, width=50, values=[])
        self.hub_map_file.pack(padx=5, pady=5)

        frame = tk.Frame(master=self.input_files_frame, bg="light gray")
        frame.grid(row=4, column=3)
        self.errata_file = ttk.Combobox(master=frame, width=50, values=[])
        self.errata_file.pack(padx=5, pady=5)



        frame  = tk.Frame(master=self.input_buttons_frame, bg="light gray")
        frame.grid(row=1, column=1)
        button = tk.Button(master = frame, text = "Read Files", command = self.process_files)
        button.pack(padx=20, pady=5)

        frame  = tk.Frame(master=self.input_buttons_frame, bg="light gray")
        frame.grid(row=1, column=2)
        button = tk.Button(master = frame, text = "QUIT", command = self.master.destroy)
        button.pack(padx=20, pady=5)


    def get_hub_map_path(self):
        initialdir = os.path.abspath('~/Desktop')
        self.hub_map_path = filedialog.askdirectory(initialdir=initialdir)
        print('Will look for directory files in', self.hub_map_path)
        with os.scandir(self.hub_map_path) as raw_files:
            files = [file for file in raw_files \
                        if file.name.startswith('hub') and (file.name.endswith('.csv'))]
            files.sort(key=lambda x: os.stat(x).st_mtime, reverse=True)
            file_names = []
            for f in files:
                file_names.append(f.name)
        self.hub_map_file["values"] = file_names
        self.hub_map_file.set(file_names[0])

        with os.scandir(self.hub_map_path) as raw_files:
            files = [file for file in raw_files \
                        if file.name.startswith('roster') and (file.name.endswith('.csv'))]
            files.sort(key=lambda x: os.stat(x).st_mtime, reverse=True)
            file_names = []
            for f in files:
                file_names.append(f.name)
        self.errata_file["values"] = file_names
        self.errata_file.set(file_names[0])



    def get_directory_path(self):
        initialdir = os.path.abspath('~/Desktop')
        self.directory_path = filedialog.askdirectory(initialdir=initialdir)
        print('Will look for directory files in', self.directory_path)
        with os.scandir(self.directory_path) as raw_files:
            files = [file for file in raw_files \
                        if not(file.name.startswith('~')) and (file.name.endswith('.csv'))]
            files.sort(key=lambda x: os.stat(x).st_mtime, reverse=True)
            file_names = []
            for f in files:
                file_names.append(f.name)
        self.directory_file["values"] = file_names
        self.directory_file.set(file_names[0])



    def get_roster_path(self):
        initialdir = os.path.abspath('~/Desktop')
        self.roster_path = filedialog.askdirectory(initialdir=initialdir)
        print('Will look for roster files in', self.roster_path)
        with os.scandir(self.roster_path) as raw_files:
            files = [file for file in raw_files \
                        if not(file.name.startswith('~')) and (file.name.endswith('.xlsx'))]
            files.sort(key=lambda x: os.stat(x).st_mtime, reverse=True)
            file_names = []
            for f in files:
                file_names.append(f.name)
        self.roster_file["values"] = file_names
        self.roster_file.set(file_names[0])



    def create_text_output_widgets(self, inputStr=""):
        ##
        ## create Text widget to hold the output
        Toutput = tk.Text(master=self.output_display_frame,
                          width=100, #self.frame_width,
                          relief=tk.RAISED)
        ##
        ## redirect STDOUT to this Text widget
        sys.stdout = StdoutRedirector(text_area=Toutput)
        Toutput.pack()
        ##
        ## insert new next into the Text widget
        Toutput.insert(tk.END, inputStr)
        
    
    def create_user_selection_widgets(self):
        choices = [['Find Missing Email', 'Find Not in Directory'       , 'Find Adults/Children Hub Mismatches' ],
                   ['Find Orphans'      , 'Find Not In Classroom Hub'   , 'Find students in multiple classrooms'],
                   ['Find Childless'    , 'Find Adults without Accounts', 'Find Unused Errata'                  ]]
        
        commands = [[self.action_0_0    , self.action_0_1               , self.action_0_2                       ],
                    [self.action_1_0    , self.action_1_1               , self.action_1_2                       ],
                    [self.action_2_0    , self.action_2_1               , self.action_2_2                       ]]

        for i in range(3):
            for j in range(3):
                frame = tk.Frame(master=self.user_selection_frame,
                                 relief=tk.RAISED, bg='light grey',
                                 borderwidth=1)
                frame.grid(row=i, column=j)
                label = tk.Button(master=frame, text=choices[i][j], command=commands[i][j])
                label.pack(padx=10, pady=5)

    def action_0_0(self):
        ##
        ## run the action
        total_adult_count, no_email_person, no_email_family, partial_family, emailless_map = \
            actions.FindMissingEmail([self.directory, self.hub_map])
        ##
        ## print some of the counts to the screen for the user to review
        message  = 'Directory contains: \n'
        message += '- ' +str(total_adult_count)+' adults, of which\n'
        message += '   '+str(len(no_email_person))+' have no email address\n\n'
        message += '- ' +str(len(self.directory)) +' families, of which\n'
        message += '   '+str(len(no_email_family))+' have no email address\n'
        message += '   '+str(len(partial_family)) +' have at least one email address.\n'
        message += '\nThe results will be shown on the screen.  Would you like to save them in a file as well?'
        message += '\n\n(Click "Cancel" to do neither)'
        ##
        ## prompt user whether to show on screen
        action = messagebox.askyesnocancel(title='Next Steps', message=message)
        if action is None:
            print('Not showing or storing results')
        else:
            for this_list in emailless_map.keys():
                print('Hub ID = ', this_list)
                for this_person in emailless_map[this_list]:
                    this_person.PrintWithHubs()
                print('\n-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-\n')
            if action == True:
                import_file_tools.CreateEmaillessByHubFile(emailless_map, self.hub_map, "emailless_by_hub")


    def action_1_0(self):
        ##
        ## run the action
        orphan_families = actions.FindOrphans(self.directory)
        ##
        ## show user how many were found
        message  = 'Found '+str(len(orphan_families))+' families without adults.\n'
        message += '\nThe results will be shown on the screen.  (Click "Cancel" to skip)'
        ##
        ## prompt user whether to show on screen
        action = messagebox.askokcancel(title  ='Next Steps', message=message)
        if not action:
            print('Not showing results')
        else:
            for entry_family in orphan_families:
                entry_family.Print()
        
    
    def action_2_0(self):
        ##
        ## run the action
        childless_families = actions.FindChildless(self.directory)
        ##
        ## show user how many were found
        message  = 'Found '+str(len(childless_families))+' families without children.\n'
        message += '\nThe results will be shown on the screen.  (Click "Cancel" to skip)'
        ##
        ## prompt user whether to show on screen
        action = messagebox.askokcancel(title  ='Summary', message=message)
        if not action:
            print('Not showing results')
        else:
            for entry_family in childless_families:
                entry_family.Print()


    def action_0_1(self):
        ##
        ## run the action
        entriless = actions.PrintNotInDirectory([self.directory, self.roster])
        ##
        ## print some of the counts to the screen for the user to review
        message  = 'Found '+str(len(entriless))+' people on the roster who were not in the directory.\n'
        message += '\nThe results will be shown on the screen.  Would you like to save them in a file as well?'
        message += '\n\n(Click "Cancel" to do neither)'
        ##
        ## prompt user whether to show on screen
        action = messagebox.askyesnocancel(title  ='Next Steps', message=message)
        if action is None:
            print('Not showing or storing results')
        else:
            for entry in entriless:
                print("Did not find this family from the roster in the directory: ")
                entry.Print()
            if action == True:
                import_file_tools.CreateNewMemberImport(entriless)
        

    def action_1_1(self):
        ##
        ## run the action
        hubless_adults, hubless_children = actions.FindHubless([self.directory, self.hub_map])
        ##
        ## show user how many were found
        message  = 'Found '+str(len(hubless_adults))+' adults and '+str(len(hubless_children))+' children who are not in at least one classroom hub.\n'
        message += '\nThe results will be shown on the screen.  (Click "Cancel" to skip)'
        ##
        ## prompt user whether to show on screen
        action = messagebox.askokcancel(title  ='Summary', message=message)
        if not action:
            print('Not showing results')
        else:
            print('ADULTS:  ')
            for this_person in hubless_adults:
                print("%s %s <%s>" % (this_person.first_name, this_person.last_name, this_person.hubs))
            print('CHILDREN:  ')
            for this_person in hubless_children:
                print("%s %s <%s>" % (this_person.first_name, this_person.last_name, this_person.hubs))

    
    def action_2_1(self):
        ##
        ## run the action
        teacher_without_email, no_account_without_email, teacher_with_no_account, no_account_with_email = actions.FindAdultsWithoutAccounts(self.directory)
        ##
        ## print some of the counts to the screen for the user to review
        message  = 'Directory contains:\n'
        message += '  People without accounts or email:\n'
        message += ' - '+str(len(teacher_without_email))   +' work for the school\n'
        message += ' - '+str(len(no_account_without_email))+' student\'s parents\n'
        message += '  People without accounts but with email:\n'
        message += ' - '+str(len(teacher_with_no_account)) +' work for the school\n'
        message += ' - '+str(len(no_account_with_email))   +' student\'s parents\n'
        message += '\nThe results will be shown on the screen.  Would you like to save them in a file as well?'
        message += '\n\n(Click "Cancel" to do neither)'
        ##
        ## prompt user whether to show on screen
        action = messagebox.askyesnocancel(title  ='Next Steps', message=message)
        if action is None:
            print('Not showing or storing results')
        else:
            print('NO ACCOUNT, NO EMAIL, WORK FOR SCHOOL')
            for this_person in teacher_without_email:
                this_person.Print()
            print('\n-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-\n')
            print('NO ACCOUNT, NO EMAIL, STUDENT PARENT')
            for this_person in no_account_without_email:
                this_person.Print()
            print('\n-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-\n')
            print('EMAIL, BUT NO ACCOUNT, WORK FOR SCHOOL')
            for this_person in teacher_with_no_account:
                this_person.PrintWithEmail()
            print('\n-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-\n')
            print('EMAIL, BUT NO ACCOUNT, STUDENT PARENT')
            for this_person in no_account_with_email:
                this_person.PrintWithEmail()
            print('\n-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-\n')

            if action == True:
                import_file_tools.CreateAccountlessFile(teacher_without_email   , 'teachers_without_email')
                import_file_tools.CreateAccountlessFile(no_account_without_email, 'no_account_without_email')
                import_file_tools.CreateAccountlessFile(teacher_with_no_account , 'teachers_without_account')
                import_file_tools.CreateAccountlessFile(no_account_with_email   , 'no_account_with_email')


    def action_0_2(self):
        ##
        ## run the action
        mismatches = actions.FindParentChildrenHubMismatches(self.directory)
        ##
        ## show user how many were found
        message  = 'Found '+str(len(mismatches))+' families that have at least one adult who is not in all thier children\'s classroom hubs.\n'
        message += '\nThe results will be shown on the screen.  (Click "Cancel" to skip)'
        ##
        ## prompt user whether to show on screen
        action = messagebox.askokcancel(title  ='Summary', message=message)
        if not action:
            print('Not showing results')
        else:
            for this_family in mismatches:
                this_family.PrintWithHubs()


    def action_1_2(self):
        ##
        ## run the action
        hubful_children = actions.FindChildrenInMultipleClassroom([self.directory, self.hub_map])
        ##
        ## show user how many were found
        message  = 'Found '+str(len(hubful_children))+' students who are not in more than one classroom hub.\n'
        message += '\nThe results will be shown on the screen.  (Click "Cancel" to skip)'
        ##
        ## prompt user whether to show on screen
        action = messagebox.askokcancel(title  ='Summary', message=message)
        if not action:
            print('Not showing results')
        else:
            for this_person in hubful_children:
                print("%s %s <%s>" % (this_person.first_name, this_person.last_name, this_person.hubs))


    def action_2_2(self):
        ##
        ## run the action
        errata_file = self.hub_map_path+'/'+self.errata_file.get()
        roster_file = self.roster_path+'/'+self.roster_file.get()
        unused_errata, all_errata = actions.FindUnsedErrata(errata_file=errata_file, roster_file=roster_file)
        ##
        ## show user how many were found
        message  = 'Found '+str(len(unused_errata))+' entries in the default roster_errata.csv that do not correct any entries in the latest roster file.\n'
        message += '\nThe results will be shown on the screen.  (Click "Cancel" to skip)'
        ##
        ## prompt user whether to show on screen
        action = messagebox.askokcancel(title  ='Summary', message=message)
        if not action:
            print('Not showing results')
        else:
            for entry in unused_errata:
                print(entry, '|', all_errata[entry])
    
    def process_files(self):
        ##
        ## ensure the user has selected a hub map file before proceeding
        if not self.hub_map_file.get():
            print("No directory file selected")
            return
        else:
            hub_map_file = self.hub_map_path+'/'+self.hub_map_file.get()
            errata_file  = self.hub_map_path+'/'+self.errata_file.get()
        ##
        ## ensure the user has selected a directory file before proceeding
        if not self.directory_file.get():
            print("No directory file selected")
            return
        else:
            directory_file = self.directory_path+'/'+self.directory_file.get()
        ##
        ## ensure the user has selected a roster file before proceeding
        if not self.roster_file.get():
            print("No roster file selected")
            return
        else:
            roster_file = self.roster_path+'/'+self.roster_file.get()
        ##
        ## process the files
        self.hub_map   = hub_map_tools.ReadHubMapFromFile(file_name = hub_map_file)
        print('Hub map file read complete:  '+hub_map_file)

        self.directory = directory_tools.ReadDirectoryFromFile(file_name = directory_file,
                                                               hub_map   = self.hub_map)
        print('Directory file read complete:  '+directory_file)

        rosterC        = roster.Roster(show_errors='', file_name=errata_file)
        self.roster    = roster_tools.ReadRosterFromFile(file_name = roster_file,
                                                         hub_map   = self.hub_map,
                                                         rosterC   = rosterC)
        print('Roster file read complete:  '+roster_file)
        ##
        ## now that input files have been read, display the buttons to process them
        self.create_user_selection_widgets()


root = tk.Tk()

app = Application(master=root)


# Window Manager 
app.master.title("My Do-Nothing Application")
# app.redirector()
app.mainloop()