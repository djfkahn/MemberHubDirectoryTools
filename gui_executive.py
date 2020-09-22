import tkinter as tk
import tkinter.ttk as ttk
from subprocess import Popen, PIPE, STDOUT
import os
import sys
import menu
import directory_tools
import roster_tools
import hub_map_tools

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
        frame_width = 800
        self.input_files_frame    = tk.Frame(master=master,
                                             width=frame_width, height= 100, bg="light gray",
                                             relief=tk.RAISED, borderwidth=1)
        self.input_files_frame.pack(pady=5)

        self.user_selection_frame = tk.Frame(master=master,
                                             width=frame_width, height= 90, 
                                             relief=tk.RAISED, borderwidth=1)
        self.user_selection_frame.pack(pady=5)
        
        self.input_display_frame  = tk.Frame(master=master, width=frame_width, height=40,
                                              relief=tk.RAISED, borderwidth=1)
        self.input_display_frame.pack()
        
        self.output_display_frame = tk.Frame(master=master, width=frame_width, height= 500,
                                             relief=tk.RAISED, borderwidth=1)
        self.output_display_frame.pack()
        
        self.master_hub_map       = hub_map_tools.ReadHubMap()

        self.create_widgets()

    def create_widgets(self):
        self.create_input_file_widgets()
        self.create_user_selection_widgets()
        self.create_input_display_frame()

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
        self.quit["command"] = quit


    def create_input_display_frame(self):
        self.user_inputs = tk.Entry(self.input_display_frame, width=30)
        self.user_inputs.pack(side="left")

        self.btn_redirect_input = tk.Button(self.input_display_frame, text="Enter", command=self.redirect_input)
        self.btn_redirect_input.pack(side="right")

    def redirect_input(self):
        pass
#         # get the text we have to ROT13
#         plaintext = self.user_inputs.get()
# 
#         # use the commandline program to do the translation
#         rot13text = do_cmdline('./rot13.py', plaintext)
# 
#         # strip off the prompt stuff
#         (_, rot13text) = rot13text.split(': ')
# 
#         # update the ROT13 display
#         self.rot13.delete(0, END)
#         self.rot13.insert(0, rot13text)
    
    def create_user_selection_widgets(self):
        choices = [['Find Missing Email', 'Find Not in Directory'       , 'Find Adults/Children Hub Mismatches' ],
                   ['Find Orphans'      , 'Find Not In Classroom Hub'   , 'Find students in multiple classrooms'],
                   ['Find Childless'    , 'Find Adults without Accounts', 'Find Unused Errata'                  ]]
        
        commands = [[self.action_0_0    , self.action_0_1               , self.action_0_2                       ],
                    [self.action_1_0    , self.action_1_1               , self.action_1_2                       ],
                    [self.action_2_0    , self.action_2_1               , self.action_2_2                       ]]

        for i in range(3):
            for j in range(3):
                frame = tk.Frame(
                    master=self.user_selection_frame,
                    relief=tk.RAISED,
                    borderwidth=1
                )
                frame.grid(row=i, column=j)
                label = tk.Button(master=frame, text=choices[i][j], command=commands[i][j])
                label.pack()

    def action_0_0(self):
        menu.FindMissingEmail([self.directory, self.master_hub_map])
    
    def action_1_0(self):
        menu.FindOrphans(self.directory)
    
    def action_2_0(self):
        menu.FindChildless(self.directory)
    
    def action_0_1(self):
        menu.PrintNotInDirectory([self.directory, self.roster])
    
    def action_1_1(self):
        menu.FindHubless([self.directory, self.master_hub_map])
    
    def action_2_1(self):
        menu.FindAdultsWithoutAccounts(self.directory)
    
    def action_0_2(self):
        menu.FindParentChildrenHubMismatches(self.directory)
    
    def action_1_2(self):
        menu.FindChildrenInMultipleClassroom([self.directory, self.master_hub_map])

    def action_2_2(self):
        menu.FindUnsedErrata([])
    
    def redirector(self, inputStr=""):
        T = tk.Text(master=self.output_display_frame)
        sys.stdout = StdoutRedirector(text_area=T)
        T.pack()
        T.insert(tk.END, inputStr)
        
    def process_files(self):
        if not self.directory_file.get():
            print("No directory file selected")
            return
        else:
            print("Selected directory file is "+self.directory_path+'/'+self.directory_file.get())

        if not self.roster_file.get():
            print("No roster file selected")
            return
        else:
            print("Selected roster file is "+self.roster_path+'/'+self.roster_file.get())

        ## process the files
        self.directory = directory_tools.ReadDirectoryFromFile(file_name = self.directory_path+'/'+self.directory_file.get(),
                                                               hub_map   = self.master_hub_map)
        self.roster    = roster_tools.ReadRosterFromFile(file_name = self.roster_path+'/'+self.roster_file.get(),
                                                         hub_map   = self.master_hub_map)

root = tk.Tk()

app = Application(master=root)


# Window Manager 
app.master.title("My Do-Nothing Application")
# app.master.maxsize(1000, 400)
# app.redirector()
app.mainloop()