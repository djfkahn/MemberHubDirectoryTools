import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from subprocess import Popen, PIPE, STDOUT
import os
import sys
import actions
import directory_tools
import roster_tools
import roster
import hub_map_tools
import import_file_tools

def do_cmdline(cmd, text):
    """Execute program in 'cmd' and pass 'text' to STDIN.
    Returns STDOUT output.
    Code from: https://stackoverflow.com/questions/8475290/how-do-i-write-to-a-python-subprocess-stdin
    Note that any prompt the program writes is included in STDOUT.
    """

    process = Popen([cmd], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    result = process.communicate(input=bytes(text, 'utf-8'))[0].decode('utf-8')
    return result.strip()

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
        self.pack()
        self.frame_width = 800
        self.input_files_frame    = tk.Frame(master=master,
                                             width=self.frame_width, height= 100, bg="light gray",
                                             relief=tk.RAISED, borderwidth=1)
        self.input_files_frame.pack(pady=5)

        self.user_selection_frame = tk.Frame(master=master,
                                             width=self.frame_width, height= 90, 
                                             relief=tk.RAISED, borderwidth=1)
        self.user_selection_frame.pack(pady=5)
        
        self.output_display_frame = tk.Frame(master=master, width=self.frame_width, height= 500,
                                             relief=tk.RAISED, borderwidth=1)
        self.output_display_frame.pack()
        
        self.master_hub_map       = hub_map_tools.ReadHubMap()

        self.create_widgets()

    def create_widgets(self):
        self.create_input_file_widgets()
        self.create_text_output_widgets()

    def create_input_file_widgets(self):
        
        self.directory_label = tk.Label(master=self.input_files_frame, text="Directory File:")
        self.directory_label.place(x=0, y=0)

        self.directory_file = ttk.Combobox(master=self.input_files_frame)
        self.directory_file.place(x=100, y=0)
        self.directory_file["width"] = 50
        self.directory_path = os.path.abspath("./Directory/")
        print(self.directory_path)
        with os.scandir(self.directory_path) as raw_files:
            files = [file for file in raw_files \
                        if not(file.name.startswith('~')) and (file.name.endswith('.csv'))]
            files.sort(key=lambda x: os.stat(x).st_mtime, reverse=True)
            file_names = []
            for f in files:
                file_names.append(f.name)
        self.directory_file["values"] = file_names
        
        
        self.roster_label = tk.Label(master=self.input_files_frame, text="Roster File:")
        self.roster_label.place(x=0, y=30)

        self.roster_file = ttk.Combobox(master=self.input_files_frame)
        self.roster_path = os.path.abspath("./Roster/")
        self.roster_file.place(x=100, y=30)
        self.roster_file["width"] = 50
        with os.scandir(self.roster_path) as raw_files:
            files = [file for file in raw_files \
                        if not(file.name.startswith('~')) and (file.name.endswith('.xlsx'))]
            files.sort(key=lambda x: os.stat(x).st_mtime, reverse=True)
            file_names = []
            for f in files:
                file_names.append(f.name)
        self.roster_file["values"] = file_names
        
        
        self.btn_process_inputs = tk.Button(master  = self.input_files_frame,
                                            text    = "Process Files",
                                            command = self.process_files)
        self.btn_process_inputs.place(x=200, y=60)
        

        self.quit = tk.Button(master  = self.input_files_frame,
                              text    = "QUIT", fg="red",
                              command = self.master.destroy)
        self.quit.place(x=400, y=60)
#         self.quit["command"] = quit



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
                label.pack()

    def action_0_0(self):
        ##
        ## run the action
        total_adult_count, no_email_person, no_email_family, partial_family, emailless_map = \
            actions.FindMissingEmail([self.directory, self.master_hub_map])
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
        action = messagebox.askyesnocancel(title  ='Next Steps', message=message)
        if action is None:
            print('Not showing or storing results')
        else:
            for this_list in emailless_map.keys():
                for this_person in emailless_map[this_list]:
                    this_person.PrintWithHubs()
            if action == True:
                import_file_tools.CreateEmaillessByHubFile(emailless_map, self.master_hub_map, "emailless_by_hub")


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
        hubless_adults, hubless_children = actions.FindHubless([self.directory, self.master_hub_map])
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
            print('NO ACCOUNT, NO EMAIL, STUDENT PARENT')
            for this_person in no_account_without_email:
                this_person.Print()
            print('EMAIL, BUT NO ACCOUNT, WORK FOR SCHOOL')
            for this_person in teacher_with_no_account:
                this_person.PrintWithEmail()
            print('EMAIL, BUT NO ACCOUNT, STUDENT PARENT')
            for this_person in no_account_with_email:
                this_person.PrintWithEmail()

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
        hubful_children = actions.FindChildrenInMultipleClassroom([self.directory, self.master_hub_map])
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
        unused_errata, all_errata = actions.FindUnsedErrata()
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
        self.directory = directory_tools.ReadDirectoryFromFile(file_name = directory_file,
                                                               hub_map   = self.master_hub_map)
        print('Directory file read complete:  '+directory_file)
        self.roster    = roster_tools.ReadRosterFromFile(file_name = roster_file,
                                                         hub_map   = self.master_hub_map,
                                                         rosterC   = roster.Roster(show_errors=''))
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