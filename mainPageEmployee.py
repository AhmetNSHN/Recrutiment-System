import tkinter as tk
import sqlite3
from tkinter import ttk
from languages import I18N

class main_page_employee(tk.Frame):
    def __init__(self, parent, username, l_mode):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        jobs = self.get_jobs()

        self.i18n = I18N(l_mode)

        x = 0
        y = 0
        z = 3
        buttons = []
        row_job_frames = []
        single_job_frames = []

        self.canv = tk.Canvas(self, bd=0)
        self.canv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scr_bar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canv.yview)
        self.scr_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canv.configure(yscrollcommand=self.scr_bar.set)
        self.canv.bind("<Configure>", lambda e: self.canv.configure(scrollregion=self.canv.bbox("all")))

        self.container = tk.Frame(self.canv)
        self.frame_id = self.canv.create_window((0, 0), window=self.container, anchor=tk.NW)

        # center = tk.Frame(self.container)
        # center.pack(expand=True)

        self.bind("<Configure>", lambda x: self.config_width())

        # main_f = tk.Frame(center)
        # main_f.pack(expand=True)

        titleLabel = tk.Label(self.container, text=self.i18n.job_adds, font="Times 25 bold")
        titleLabel.pack(side=tk.TOP, padx=(10, 40))

        while x < len(jobs) :
            row_job_frames.append(tk.Frame(self.container,bg="red"))
            if x > len(jobs)-3:
                z = len(jobs) - x
            for _ in range(z):
                single_job_frames.append(tk.Frame(row_job_frames[y], width=360, height=190,bg="green"))
                single_job_frames[x].grid_propagate(False)
                center_f = tk.Frame(single_job_frames[x])
                jobtitle = tk.Label(center_f, text=f"{jobs[x][1]}\n{self.i18n.category}{jobs[x][2]}\n{self.i18n.company}{jobs[x][3]}\n{self.i18n.location}{jobs[x][7]}", anchor=tk.CENTER, justify=tk.CENTER, width=40)
                jobtitle.grid(row=0, column=0, sticky=tk.NS)
                buttons.append(tk.Button(center_f, text=self.i18n.details,
                                         command=lambda job=jobs[x][1]: parent.goto_applypage(username, job, l_mode)))
                buttons[x].grid(column=0, row=1, pady=(10, 35), sticky=tk.NS)
                single_job_frames[x].rowconfigure(0, weight=1)
                single_job_frames[x].columnconfigure(0, weight=1)
                center_f.grid(column=0,row=0,sticky=tk.NSEW)
                single_job_frames[x].pack(side=tk.LEFT, pady=10,padx=10, expand=True)
                x += 1

            row_job_frames[y].pack(side=tk.TOP)
            y += 1

    def config_width(self):
        self.canv.itemconfig(self.frame_id, width=self.winfo_width())






    def get_jobs(self):
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute("SELECT*  FROM jobs")
            results = c.fetchall()
            return results

