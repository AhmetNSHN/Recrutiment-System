import sqlite3
import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import messagebox as msg
from languages import I18N

class create_job(tk.Frame):
    def __init__(self, parent, username, l_mode):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.username = username
        self.i18n = I18N(l_mode)

        self.canv = tk.Canvas(self, bd=0)
        self.canv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scr_bar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canv.yview)
        self.scr_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canv.configure(yscrollcommand=self.scr_bar.set)
        self.canv.bind("<Configure>", lambda e: self.canv.configure(scrollregion=self.canv.bbox("all")))

        self.container = tk.Frame(self.canv)
        self.frame_id = self.canv.create_window((0, 0), window=self.container, anchor=tk.NW)

        center = tk.Frame(self.container)
        center.pack(expand=True)

        self.bind("<Configure>", lambda x: self.config_width())

        l_jobtitle = tk.Label(center, text=self.i18n.job_title, font=44)
        l_jobtitle.grid(column=0, row=0, pady=5)
        self.s_jobtitle = tk.StringVar()
        tb_jobtitle = tk.Entry(center, width=40, textvariable=self.s_jobtitle)
        tb_jobtitle.grid(column=1, row=0,)

        l_category = tk.Label(center, text=self.i18n.category, font=44)
        l_category.grid(column=0, row=1, pady=5)
        self.s_category = tk.StringVar()
        tb_category = tk.Entry(center, width=40, textvariable=self.s_category)
        tb_category.grid(column=1, row=1)

        l_jobdescription = tk.Label(center, text=self.i18n.job_desc)
        l_jobdescription.grid(column=0, row=2, stick=tk.N)
        self.st_jobdescription = scrolledtext.ScrolledText(center, width=50, height=15, wrap=tk.WORD, relief="solid",bd =1)
        self.st_jobdescription.grid(column=1, row=2, sticky=tk.W, pady=8)

        l_reqqualifications = tk.Label(center, text=self.i18n.required_q)
        l_reqqualifications.grid(column=0, row=3, pady=5, stick=tk.N, padx=5)
        self.st_reqqualifications = scrolledtext.ScrolledText(center, width=50, height=15, wrap=tk.WORD, relief="solid",bd =1)
        self.st_reqqualifications.grid(column=1, row=3, sticky=tk.W, pady=8)

        l_responsibilities = tk.Label(center, text=self.i18n.respons)
        l_responsibilities.grid(column=0, row=4, stick=tk.N)
        self.st_responsibilities = scrolledtext.ScrolledText(center, width=50, height=15, wrap=tk.WORD, relief="solid",bd =1)
        self.st_responsibilities.grid(column=1, row=4, sticky=tk.W, pady=8)

        l_location = tk.Label(center, text=self.i18n.location, font=44)
        l_location.grid(column=0, row=5, pady=5)
        self.s_location = tk.StringVar()
        tb_location = tk.Entry(center, width=40, textvariable=self.s_location)
        tb_location.grid(column=1, row=5)

        self.l_warn = tk.Label(center, text="")
        self.l_warn.grid(column=1, row=6, columnspan=4, pady=5, stick=tk.N)

        lf_buttons = tk.LabelFrame(center, bd=0)
        lf_buttons.grid(column=1, row=7)

        b_register = tk.Button(lf_buttons, text=self.i18n.publish, command=lambda: self.database_addjob())
        b_register.pack(side=tk.LEFT, pady=5)

        b_cancel = tk.Button(lf_buttons, text=self.i18n.cancel, command=lambda: parent.gobackfrom_newjob())
        b_cancel.pack(side=tk.LEFT)

    def config_width(self):
        self.canv.itemconfig(self.frame_id, width=self.winfo_width())


    def database_addjob(self):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT company_name from employer WHERE username = ?",(self.username,))
        company_name, = c.fetchone()
        entry_list = [
            self.s_jobtitle.get(),
            self.s_category.get(),
            str(company_name),
            self.st_jobdescription.get('1.0', tk.END),
            self.st_reqqualifications.get('1.0', tk.END),
            self.st_responsibilities.get('1.0', tk.END),
            self.s_location.get(),
            0,
            0]

        if "" in entry_list:
            self.l_warn.configure(text="Please fill in empty fields, all of them required", fg="red")
        else:

            c.execute("insert into jobs (job_title, job_category,company_name, job_description, required_qualifications, responsibilities, location, view, applicants_num)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (entry_list))
            conn.commit()
            conn.close()
            msg.showinfo("info!", "job advertisement published succesfully!")
            self.parent.gobackfrom_newjob()



