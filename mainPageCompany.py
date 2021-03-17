import tkinter as tk
import sqlite3
from languages import I18N
from tkinter import ttk
class main_page_company(tk.Frame):
    def __init__(self, parent, username, l_mode):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.i18n = I18N(l_mode)
        jobs = self.get_jobs(username)
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT company_name FROM employer WHERE username =?", (username,))
        comp_name = c.fetchone()

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

        titleLabel = tk.Label(self.container, text= self.i18n.job_listing + comp_name[0], font = "Times 25 bold")
        titleLabel.pack(side=tk.TOP)
        j = 0
        buttons = []
        for i in range(len(jobs)):
            j = j + i
            jobFrame = tk.Frame(self.container)
            jobFrame.pack(side=tk.TOP)
            jobtitle = tk.Label(jobFrame, text=f"{jobs[i][1]}\n{self.i18n.category}{jobs[i][2]}\n{self.i18n.company}{jobs[i][3]}\n{self.i18n.location}{jobs[i][7]}")
            jobtitle.grid(row=0, column=0)
            buttons.append(tk.Button(jobFrame, text= self.i18n.details,
                                     command=lambda job=jobs[i][1]: parent.goto_jobDetails(job, l_mode)))

            buttons[i].grid(column=0, row=1, pady=(10,35))

        b_addjob = tk.Button(self.container, text=self.i18n.add_new_job, font=(None, 18), command=lambda : parent.create_newjob(username, l_mode))
        b_addjob.pack(side=tk.TOP)




    def get_jobs(self, username):
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute("SELECT*  FROM jobs INNER JOIN employer ON jobs.company_name = employer.company_name WHERE username=? ", (username,))
            results = c.fetchall()
            print (username)
            return results

    def get_job_details(self,jobName):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(
            "SELECT*  FROM jobs INNER JOIN applicants ON jobs.job_id = applicants.job_id WHERE job_title=? ",
            (jobName,))
        results = c.fetchall()
        print(jobName)
        return results

    def config_width(self):
        self.canv.itemconfig(self.frame_id, width=self.winfo_width())