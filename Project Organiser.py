from tkinter import *
import tkinter as tk
import sqlite3
from datetime import datetime

###### BACK BUTTON DOES NOT WORK YET #######
TITLE_FONT = ('Calibri', 16, "bold")
ALL_FONT = ('Calibri', 12, "bold")
SMALL_FONT = ('Calibri', 12)


class PageTurner(tk.Tk):
    #CONTENTS: PO_PT.pageturning
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        from tkinter import ttk
        container = ttk.Frame(self)

        container.pack(side=TOP, fill=BOTH, expand=TRUE)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (NavigationPage, InProgress, NewProject, CompletedProjects):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky=N + S + E + W)
    # UNDERNEATH: INITIAL PAGE AFTER LOGIN
        self.show_page(NavigationPage)

# CREATING THE BUTTON FUNCTION TO SWAP TO A DIFFERENT PAGE
    def show_page(self, cont):
        ## CONTENTS: PO_PT.show_page
        frame = self.frames[cont]
        frame.tkraise()

# TEST TO SEE IF YOU CAN USE THE OPPOISTE OF ABOVE FOR A BACK BUTTON
    def prev_page(self, cont):
        frame = self.frames[cont]
        frame.tklower()

# CREATING THE INITAL NAVIGATION PAGE


class NavigationPage(Frame):
    def __init__(self, parent, controller):
        from tkinter import ttk
        style = ttk.Style()
        style.configure("Title.TLabel", background="grey", width=67, font=TITLE_FONT)
        style.configure("Navi.TFrame", background="lightgrey")
        style.configure("Navi.TButton", background="thistle4", foreground="grey28", font=ALL_FONT, relief='raised')

        ## CONTENTS: PO_NP.title_layout
        ttk.Frame.__init__(self, parent)

        container = ttk.Frame(self, relief=SUNKEN, style="Navi.TFrame")

        container.pack(side=TOP, fill=BOTH, expand=TRUE)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        title_label = ttk.Label(container, text="Nav Page", style="Title.TLabel", anchor="center")

        ## CONTENTS: PO_NP.navigation_buttons
        button_container = ttk.Frame(self, relief=GROOVE, style="Navi.TFrame")
        button_container.pack(side=BOTTOM, fill=X)
        button_container.grid_rowconfigure(0, weight=1)
        button_container.grid_columnconfigure(0, weight=1)
        button_container.grid_columnconfigure(1, weight=1)

        page_one_button = ttk.Button(button_container,
                                     command=lambda: controller.show_page(InProgress),
                                     text="Projects in Progress", style="Navi.TButton")
        page_two_button = ttk.Button(button_container,
                                     command=lambda: controller.show_page(CompletedProjects),
                                     text="Completed Projects", style="Navi.TButton")

        title_label.grid(row=0, column=0, sticky=E + W)

        page_one_button.grid(row=0, column=0, sticky=E)
        page_two_button.grid(row=0, column=1, sticky=W)


class InProgress(Frame):
    def __init__(self, parent, controller):
        from tkinter import ttk

        ## CONTENTS: PO_NP.widget_styles
        style = ttk.Style()
        style.configure("Progress.TLabel", background="grey", width=67, font=TITLE_FONT, relief='raised', borderwidth=15)
        style.configure("Progress.TFrame", background="LightSteelBlue2")
        style.configure("NavigationBut.TFrame", background="lightgrey", relief='sunken', borderwidth=5)
        style.configure("Progress.TButton", background="thistle4", foreground="grey28", font=SMALL_FONT, relief='raised')
        style.configure("SubTitle.TLabel", background="grey77", width=67, font=ALL_FONT, borderwidth=15)
        style.configure("Content.TLabel", background="grey85", width=64, font=ALL_FONT, borderwidth=15)
        style.configure("Project_list.TLabel", background="grey", width=100)
        style.configure("Project_list.TFrame", background="grey")

        ## CONTENTS: PO_NP.title_label
        ttk.Frame.__init__(self, parent, style="Progress.TFrame")
        ttk.Label(self, text="Projects in Progress", style="Progress.TLabel", anchor="center").grid(sticky=E + W)

        ## CONTENTS: PO_IP.navigation_buttons
        navigation_frame = ttk.Frame(self, style="NavigationBut.TFrame")

        back_button = ttk.Button(navigation_frame,
                                 command=lambda: controller.show_page(NavigationPage),
                                 text="Back", style="Progress.TButton")
        page_two_button = ttk.Button(navigation_frame,
                                     command=lambda: controller.show_page(CompletedProjects),
                                     text="Completed Projects", style="Progress.TButton")

        navigation_frame.grid(sticky=W, pady=5)
        back_button.grid(row=1, sticky=W, padx=1)
        page_two_button.grid(row=1, column=2, sticky=W)

        ## CONTENTS: PO_IP.show_update_frame
        self.update_button = {}
        self.project_frame = {}

        def show_update_frame(x):
            # First clear the screen of unwanted widgets, but let them be callable again
            project_frame.grid_forget()
            back_button.grid_forget()
            add_project_button.grid_forget()

            # Create a function to act as a new back button on this page - forgets added widgets and remembers the old back button
            def back_button_view_command():
                back_button_view_page.grid_forget()
                view_project_container_frame.grid_forget()
                task_frame.grid_forget()
                back_button.grid(row=1, padx=1)
                project_frame.grid()
                add_project_button.grid()

            back_button_view_page = ttk.Button(navigation_frame, text="Back", command=back_button_view_command, style="Progress.TButton")
            back_button_view_page.grid(row=1, padx=1)

            # Create a new frame for all widgets in this function to be contained in
            view_project_container_frame = ttk.Frame(self, style="Progress.TFrame")
            view_project_container_frame.grid(sticky=N + E + S + W)

            # Getting the correct project name from the database table "projects"
            conn = sqlite3.connect(r'C:\PYTHON PROJECTS\Project Organiser\project_organiser.db')
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM projects WHERE rowid=?', (x, ))
            view_project_name = cursor.fetchone()
            view_p_name = str(view_project_name)[2:-3]

            # inserting the project into labels
            view_project_label = ttk.Label(view_project_container_frame, text=view_p_name, style="Progress.TLabel", anchor="center")
            view_project_label.grid()

            # Retrieving the project description from the databse table "projects"
            cursor.execute('SELECT description FROM projects WHERE rowid=?', (x, ))
            view_project_name = cursor.fetchone()
            cursor.close()
            conn.close()

            view_p_desc = str(view_project_name)[2:-3]

            # Inserting the project description into a label
            view_description_label = ttk.Label(view_project_container_frame, text=view_p_desc, style="SubTitle.TLabel")
            view_description_label.grid(sticky=N + E + S + W)

            # Frame and Button to add tasks to the project
            task_frame = ttk.Frame(self, style="Progress.TFrame")
            task_frame.grid()

            ## CONTENTS: PO_IP.tasks
            ######TASKS TO GO HERE FROM DATABASE ######
            conn = sqlite3.connect(r'C:\PYTHON PROJECTS\Project Organiser\project_organiser.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks')
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            task_name_list = []
            id_list = []

            row_name_num = 0
            # Iterating over all rows in the table to fetch all tasks and append to a list
            for row in rows:
                conn = sqlite3.connect(r'C:\PYTHON PROJECTS\Project Organiser\project_organiser.db')
                cursor = conn.cursor()
                cursor.execute('SELECT task FROM tasks WHERE current_project=? and rowid=?', (x, row_name_num + 1))
                task_fetch = cursor.fetchone()
                task_name_list.append(task_fetch)
                cursor.execute('SELECT rowid FROM tasks WHERE current_project=? and rowid=?', (x, row_name_num + 1))
                id_fetch = cursor.fetchone()
                id_str = str(id_fetch)[1:-2]

                if id_str == "o":
                    pass
                else:
                    id_int = int(id_str)
                    id_list.append(id_int - 1)

                cursor.close()
                conn.close()
                row_name_num += 1

            # Assigning all rows with current project to a variable to iterate over later
            conn = sqlite3.connect(r'C:\PYTHON PROJECTS\Project Organiser\project_organiser.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM tasks WHERE current_project=?', (x, ))
            project_fetch = cursor.fetchall()
            cursor.close()
            conn.close()
            row_num = 0

            ## CONTENTS: PO_IP.edit_task
            # Create a function to edit
            def edit_task(correct_id):

                def confirm_edit_task():
                    # Connect to the task table in database and update task dependant on rowid
                    edit_task_set = edit_task_textvar.get()
                    conn = sqlite3.connect(r'C:\PYTHON PROJECTS\Project Organiser\project_organiser.db')
                    cursor = conn.cursor()
                    cursor.execute('''UPDATE tasks SET task=?
                        WHERE rowid=?''', (edit_task_set, correct_id + 1))
                    conn.commit()
                    cursor.close()
                    conn.close()

                    # Reapply the relevant widgets for project view
                    edit_task_frame.grid_forget()
                    task_frame.grid()
                    project_update_button.grid()

                ##CONTENTS: PO_IP.cancel_edit
                def cancel_edit_task():
                    # Readd the  widgets for project view screen
                    edit_task_frame.grid_forget()
                    task_frame.grid()
                    project_update_button.grid()

                # Ungrid all widgets irrelevant to this page
                task_frame.grid_forget()
                project_update_button.grid_forget()

                edit_task_frame = ttk.Frame(self, style="Progress.TFrame")

                edit_task_label = ttk.Label(edit_task_frame, text=("Change " + str(task_name_list[correct_id])[2:-3] + " to:"), style="Content.TLabel")
                placeholder_label = ttk.Label(edit_task_frame, style="Content.TLabel")

                edit_task_textvar = StringVar()
                edit_task_entry = ttk.Entry(edit_task_frame, width=40, textvariable=edit_task_textvar)

                confirm_edit_button = ttk.Button(edit_task_frame, text="Confirm", command=confirm_edit_task, style="Progress.TButton")
                cancel_edit_button = ttk.Button(edit_task_frame, text="Cancel", command=cancel_edit_task, style="Progress.TButton")

                edit_task_frame.grid()
                edit_task_label.grid(row=0, column=0, padx=10)
                placeholder_label.grid(row=0, column=1)
                edit_task_entry.grid(row=0, column=1, padx=10, sticky=W)
                confirm_edit_button.grid(row=1, column=0, sticky=E)
                cancel_edit_button.grid(row=1, column=1, sticky=W)

            ## CONTENTS: PO_IP.delete_task
            def delete_task(correct_id):
                # Forget the previous container of widgets
                print(task_name_list[correct_id])
                project_update_button.grid_forget()
                task_frame.grid_forget()
                # Create a new set of widgets for confirm delete page:
                delete_task_frame = ttk.Frame(self, style="Progress.TFrame")
                delete_task_frame.grid(sticky=W)

                # Make the widgets expand with the window
                delete_task_frame.grid_rowconfigure(0, weight=1)
                delete_task_frame.grid_columnconfigure(0, weight=1)
                delete_task_frame.grid_rowconfigure(3, weight=1)
                delete_task_frame.grid_columnconfigure(3, weight=1)

                confirm_delete_label = ttk.Label(delete_task_frame,
                                                 text="Are you sure you want to delete task: " + task_label_text + "?",
                                                 style="Content.TLabel")

                ## CONTENTS: PO_IP.confirm_delete(task)
                def confirm_delete():
                    correct_id + 1
                    conn = sqlite3.connect(r'C:\PYTHON PROJECTS\Project Organiser\project_organiser.db')
                    cursor = conn.cursor()
                    cursor.execute('''DELETE FROM tasks
                        WHERE rowid=?''', (correct_id + 1, ))
                    conn.commit()
                    cursor.close()
                    conn.close()

                    # Reapply the relevant widgets for project view
                    delete_task_frame.grid_forget()
                    project_update_button.grid()
                    task_frame.grid()

                ## CONTENTS: PO_IP.cancel_delete(task)
                def cancel_delete():
                    print(correct_id)
                    delete_task_frame.grid_forget()
                    project_update_button.grid()
                    task_frame.grid()

                confirm_delete_label.grid(row=0, column=0)

                confirm_delete_button = ttk.Button(delete_task_frame,
                                                   text="Delete",
                                                   style="Progress.TButton",
                                                   command=confirm_delete)
                cancel_delete_button = ttk.Button(delete_task_frame,
                                                  text="Cancel",
                                                  style="Progress.TButton",
                                                  command=cancel_delete)

                confirm_delete_button.grid(row=3, column=0, pady=7, sticky=W)
                cancel_delete_button.grid(row=3, column=0, pady=7, sticky=W, padx=98)

            ## CONTENTS: PO_IP.task_list
            # Create widgets for each task
            self.check_var = {}
            # Create dictionary for edit and delete button so that each edit goes to the correct task
            self.edit_task_button = {}
            self.delete_task_button = {}
            self.task_completebutton = {}
            self.state_val = {}
            task_id_list = []
            # get value from checkbox to update database, or to check if task has been completed.

            for row in project_fetch:
                correct_id = id_list[row_num]
                task_label_text = str(task_name_list[correct_id])[2:-3]

                self.check_var[row_num] = IntVar()

                task_label = ttk.Label(task_frame, text=task_label_text, style="Content.TLabel")  # width=80
                task_label.grid(row=row_num, column=1, sticky=W)

                self.task_completebutton[row_num] = ttk.Button(task_frame, text="Complete", style="Progress.TButton")
                self.edit_task_button[correct_id] = ttk.Button(task_frame, text="Edit Task", command=lambda correct_id=correct_id: edit_task(correct_id), style="Progress.TButton")
                self.delete_task_button[correct_id] = ttk.Button(task_frame, text="Delete Task", style="Progress.TButton", command=lambda correct_id=correct_id: delete_task(correct_id))
                self.task_completebutton[row_num].grid(row=row_num, column=2, sticky=W)
                self.edit_task_button[correct_id].grid(row=row_num, column=3, sticky=W)
                self.delete_task_button[correct_id].grid(row=row_num, column=4, sticky=W)
                row_num += 1

            ## CONTENTS: PO_IP.add_task
            def add_task():
                # Grid forget to stop users from being able to press the button multiple times
                add_task_button.grid_forget()
                conn = sqlite3.connect(r'C:\PYTHON PROJECTS\Project Organiser\project_organiser.db')
                cursor = conn.cursor()
                cursor.execute('''CREATE table IF NOT EXISTS tasks(
                                            id integer PRIMARY KEY,
                                            task text NOT NULL,
                                            completed text,
                                            current_project text
                                            )''')

                # Entry boxes for the creation of new tasks
                self.task_entry = StringVar()
                self.task_ent = ttk.Entry(task_frame, textvariable=self.task_entry, width=40)
                self.task_ent.grid(column=1, sticky=W)
                cursor.close()
                conn.close()

                ## CONTENTS: PO_IP.confirm_add_task
                def confirm_add_task():
                    task_value = self.task_entry.get()
                    conn = sqlite3.connect(r'C:\PYTHON PROJECTS\Project Organiser\project_organiser.db')
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO tasks(task, current_project) VALUES(?,?)', (task_value, x))
                    self.task_ent.grid_forget()
                    add_task_button.grid(column=1, sticky=W, pady=(15, 0))
                    confirm_task_button.grid_forget()
                    cancel_task_button.grid_forget()
                    task_frame.grid_forget()
                    update_time()
                    task_frame.grid()
                    conn.commit()
                    cursor.close()
                    conn.close()

                ## CONTENTS: PO_IP.cancel_add_task
                def cancel_add_task():
                    self.task_ent.grid_forget()
                    confirm_task_button.grid_forget()
                    cancel_task_button.grid_forget()
                    add_task_button.grid(column=1, sticky=W, pady=(15, 0))

                confirm_task_button = ttk.Button(task_frame, text="Confirm", command=confirm_add_task, style="Progress.TButton")
                confirm_task_button.grid(column=1, sticky=W)

                cancel_task_button = ttk.Button(task_frame, text="Cancel", command=cancel_add_task, style="Progress.TButton")
                cancel_task_button.grid(column=1, sticky=W)

            add_task_button = ttk.Button(task_frame, text="Add Task", command=add_task, style="Progress.TButton")
            # save_button = ttk.Button(task_frame, text="Save", command=lambda x=x: get_checkbutton(x), style="Progress.TButton")
            add_task_button.grid(row=10, column=1, sticky=W, pady=(15, 0))
            # save_button.grid(row=10, column=2, sticky=E, pady=(15, 0))

            ## CONTENTS: PO_IP.update_project
            # Function to update existing projects: Frame, Labels, Entry Boxes, Update Button, Cancel Button
            def update_project():
                # forget the view frame and button
                view_project_container_frame.grid_forget()
                back_button_view_page.grid_forget()
                task_frame.grid_forget()

                # add new frame and widgets
                update_frame = ttk.Frame(self, style="Project.TFrame")
                update_frame.grid()

                field_labels = ('Project Name:', 'Project Description:', 'Begin Date:', 'End Date:')

                # Collecting the results from row x of the database to insert into a list. Variable y is to be iterated over to prefill entry boxes
                # This list can be replaced by a for loop
                y = 0
                conn = sqlite3.connect(r'C:\PYTHON PROJECTS\Project Organiser\project_organiser.db')
                cursor = conn.cursor()
                database_n = cursor.execute('SELECT name FROM projects WHERE rowid=?', (x, ))
                database_name = str(cursor.fetchone())[2:-3]
                database_d = cursor.execute('SELECT description FROM projects WHERE rowid=?', (x, ))
                database_description = str(cursor.fetchone())[2:-3]
                database_b = cursor.execute('SELECT begin_date FROM projects WHERE rowid=?', (x, ))
                database_begin_date = str(cursor.fetchone())[2:-3]
                database_e = cursor.execute('SELECT end_date FROM projects WHERE rowid=?', (x, ))
                database_end_date = str(cursor.fetchone())[2:-3]
                cursor.close()
                conn.close()

                database_list = [database_name, database_description, database_begin_date, database_end_date]

                self.entry_text = {}
                # Creating the labels and entry boxes, just like in the NewProject class
                for fields in field_labels:
                    prefill_text = database_list[y]
                    ttk.Label(update_frame, text=fields, style="Content.TLabel").grid()
                    self.entry_text[fields] = StringVar(value=prefill_text)
                    self.ent = ttk.Entry(update_frame, textvariable=self.entry_text[fields], width=40)
                    self.ent.grid()
                    y += 1
        ############# IF ANY EXTRA FIELDS ARE ADDED, NO NEED TO CHANGE THIS FUNCTION ###############

                def confirm_update_project():
                    # get text from entry boxes - this will update row x of the projects table
                    entry_name = self.entry_text['Project Name:'].get()
                    entry_description = self.entry_text['Project Description:'].get()
                    entry_bdate = self.entry_text['Begin Date:'].get()
                    entry_edate = self.entry_text['End Date:'].get()

                    for fields in field_labels:
                        entries = self.entry_text[fields].get()
                        if entries == "":
                            print('no')
                        else:
                            # change back to that projects view page
                            update_frame.grid_forget()
                            cancel_button.grid_forget()
                            back_button_view_page.grid(row=1, padx=1)
                            view_project_container_frame.grid()
                            task_frame.grid()

                    # Update entry box data into the database at row x
                    conn = sqlite3.connect(r'C:\PYTHON PROJECTS\Project Organiser\project_organiser.db')
                    cursor = conn.cursor()
                    cursor.execute('''UPDATE projects SET name=?, description=?, begin_date=?, end_date=?
                        WHERE rowid=?''', (entry_name, entry_description, entry_bdate, entry_edate, x))
                    conn.commit()
                    cursor.close()
                    conn.close()

                confirm_button = ttk.Button(update_frame,
                                            text="Confirm",
                                            command=confirm_update_project, style="Progress.TButton")

                confirm_button.grid(row=9, column=0, pady=(10, 0), sticky=W)

                # Function and widget to cancel the update with no changes saved

                def cancel_update():
                    update_frame.grid_forget()
                    back_button_view_page.grid(row=1, padx=1)
                    view_project_container_frame.grid()
                    task_frame.grid()

                cancel_button = ttk.Button(update_frame,
                                           text="Cancel",
                                           command=cancel_update, style="Progress.TButton")
                cancel_button.grid(row=9, column=0, padx=(98, 0), pady=(10, 0), sticky=W)

            # Button to change to the update screen, where changes can be made to row x of the projects table
            project_update_button = ttk.Button(view_project_container_frame, text="Update Project", command=update_project, style="Progress.TButton")
            project_update_button.grid()

        ########### VIEW ALL PROJECTS SCREEN ###############
        project_frame = ttk.Frame(self, borderwidth=5, relief=GROOVE, style="Project_list.TFrame")
        project_frame.grid(sticky=E + W + N + S)
        Grid.rowconfigure(self, 0, weight=1)
        Grid.columnconfigure(self, 0, weight=1)
        Grid.rowconfigure(project_frame, 0, weight=1)
        Grid.grid_columnconfigure(project_frame, 0, weight=1)

        conn = sqlite3.connect(r'C:\PYTHON PROJECTS\Project Organiser\project_organiser.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects")
        rows = cursor.fetchall()
        x = 1
        for row in rows:
            cursor.execute('SELECT name FROM projects WHERE rowid=?', (x, ))
            project_name = cursor.fetchone()
            p_name = str(project_name)[2:-3] + "\n"

            cursor.execute('SELECT description FROM projects WHERE rowid=?', (x, ))
            project_description = cursor.fetchone()

            p_desc = str(project_description)[2:-3]
            project_update_button_text = str(p_name + p_desc)

            self.update_button[x] = Button(project_frame,
                                           text=project_update_button_text,
                                           justify=LEFT, anchor=W,
                                           borderwidth=5,
                                           background="grey77",
                                           command=lambda x=x: show_update_frame(x),
                                           relief=RAISED)
            self.update_button[x].grid(rowspan=2, sticky=E + W + N + S, padx=10, pady=5)

            x += 1

        # Close connection outside of the for loop
        cursor.close()
        conn.close()

################## CREATE NEW PROJECT #######################
        add_project_button = ttk.Button(self,
                                        command=lambda: controller.show_page(NewProject),
                                        text="Add Project", style="Progress.TButton")

        add_project_button.grid()


class NewProject(Frame):
    def __init__(self, parent, controller):
        from tkinter import ttk
        ttk.Frame.__init__(self, parent)
        ttk.Label(self, text="New Project").grid()

        back_button = ttk.Button(self,
                                 command=lambda: controller.show_page(InProgress),
                                 text="Back")
        page_one_button = ttk.Button(self,
                                     command=lambda: controller.show_page(InProgress),
                                     text="Projects in Progress")

        back_button.grid(sticky=W)
        page_one_button.grid()

    ####### MASS CREATE FIELDS - EASY TO ADD EXTRA FIELDS ################
        field_labels = ('Project Name', 'Project Description')

        self.entry_text = {}

        for fields in field_labels:
            Label(self, text=fields).grid()
            self.entry_text[fields] = StringVar()
            self.ent = ttk.Entry(self, textvariable=self.entry_text[fields], width=40)
            self.ent.grid()

    ############# IF ANY EXTRA FIELDS ARE ADDED, NO NEED TO CHANGE THIS FUNCTION ###############
        def confirm_new_project():
            entry_name = self.entry_text['Project Name'].get()
            entry_description = self.entry_text['Project Description'].get()
            # get text from entry boxes - this will turn into a database to show on InProgress
            for fields in field_labels:
                entries = self.entry_text[fields].get()
                if entries == "":
                    print('no')
                else:
                    # change back to the InProgress page
                    controller.show_page(InProgress)

            # Insert entry box data into the database
            conn = sqlite3.connect(r'C:\PYTHON PROJECTS\Project Organiser\project_organiser.db')
            cursor = conn.cursor()
            cursor.execute('''CREATE table IF NOT EXISTS projects(
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            description text NOT NULL,
                                            begin_date text,
                                            end_date text
                                            )'''
                           )
            cursor.execute('INSERT INTO projects(name, description) VALUES(?,?)', (entry_name, entry_description))
            conn.commit()
            cursor.close()
            conn.close()

        confirm_button = ttk.Button(self,
                                    text="confirm",
                                    command=confirm_new_project)

        confirm_button.grid()


class CompletedProjects(Frame):
    def __init__(self, parent, controller):
        from tkinter import ttk

        style = ttk.Style()
        style.configure("Progress.TLabel", background="grey", width=67, font=TITLE_FONT, relief='raised', borderwidth=15)
        style.configure("Completed.TFrame", background="LightSteelBlue2")
        style.configure("NavigationBut.TFrame", background="lightgrey", relief='sunken', borderwidth=5)
        style.configure("Completed.TButton", background="thistle4", foreground="grey28", font=SMALL_FONT, relief='raised')
        style.configure("Completed.TLabel", background="grey77", width=67, font=ALL_FONT, borderwidth=15)
        style.configure("Content.TLabel", background="grey85", width=64, font=ALL_FONT, borderwidth=15)

        ttk.Frame.__init__(self, parent, style="Completed.TFrame")
        completed_title_label = ttk.Label(self,
                                          text="Completed Projects",
                                          style="Progress.TLabel",
                                          anchor="center")
        completed_title_label.grid(sticky=E + W)

        navigation_frame = ttk.Frame(self,
                                     style="NavigationBut.TFrame")
        back_button = ttk.Button(navigation_frame,
                                 command=lambda: controller.show_page(NavigationPage),
                                 text="Back",
                                 style="Completed.TButton")
        progress_button = ttk.Button(navigation_frame,
                                     command=lambda: controller.show_page(InProgress),
                                     text="Projects in Progress",
                                     style="Completed.TButton")

        navigation_frame.grid(sticky=W, pady=5)
        back_button.grid(row=1, sticky=W, padx=1)
        progress_button.grid(row=1, column=2, sticky=W)


def update_time():
    # update displayed time
    current_time = datetime.now()
    current_time_str = current_time.strftime('%Y.%m.%d  %H:%M:%S')

    # run update_time again after 1000ms (1s)
    app.after(1000, update_time)


app = PageTurner()
app.title("Project Organiser")
# app.state("zoomed")
app.mainloop()
