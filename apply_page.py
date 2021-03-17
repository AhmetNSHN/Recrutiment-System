import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from languages import I18N
class apply(tk.Frame):
    def __init__(self, parent, username, job_title, l_mode):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.i18n = I18N(l_mode)
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("UPDATE jobs SET view = view + 1 WHERE  job_title=?", (job_title,)) #job title used in here
        c.execute(
            "SELECT j.job_title, j.job_category, e.company_name, j.location, e.company_details, j.job_description,"
            " j.required_qualifications, j.responsibilities, j.company_name, j.view, j.applicants_num, j.job_id FROM employer e, jobs j"
            " WHERE e.company_name = j.company_name AND j.job_title = ?  ",
            (job_title,))
        result = c.fetchone()
        conn.commit()
        conn.close()

        self.columnconfigure(0, weight = 1)

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

        l_title = tk.Label(center, text=f"{result[0]} {result[1]}", width=70, font=(None, 25, "bold"))
        l_title.grid(column=0, row=0)

        l_companyname_t = tk.Label(center, text=f"{self.i18n.company} {result[2]} ", font=(None, 20, "bold"))
        l_companyname_t.grid(column=0, row=1)

        l_location = tk.Label(center, text=f"{self.i18n.location} {result[3]}", font=(None, 17, "bold"))
        l_location.grid(column=0, row=2)

        l_aboutcompany_t = tk.Label(center, text=self.i18n.about_our_company, font=(None, 15, "bold"))
        l_aboutcompany_t.grid(column=0, row=3)
        l_companyname = tk.Label(center, text=result[4], wraplength=750)
        l_companyname.grid(column=0, row=4)

        l_aboutcompany_t = tk.Label(center, text=self.i18n.job_desc, font=(None, 15, "bold"))
        l_aboutcompany_t.grid(column=0, row=5)
        l_companyname = tk.Label(center, text=result[5], wraplength=750)
        l_companyname.grid(column=0, row=6)

        l_aboutcompany_t = tk.Label(center, text=self.i18n.required_q, font=(None, 15, "bold"))
        l_aboutcompany_t.grid(column=0, row=7)
        l_companyname = tk.Label(center, text=result[6], wraplength=750)
        l_companyname.grid(column=0, row=8)

        l_aboutcompany_t = tk.Label(center, text=self.i18n.respons, font=(None, 15, "bold"))
        l_aboutcompany_t.grid(column=0, row=9)
        l_companyname = tk.Label(center, text=result[7], wraplength=750)
        l_companyname.grid(column=0, row=10)

        f_bottom = tk.Frame(center, bd=1, relief=tk.SOLID)
        f_bottom.grid(column=0, row=11)
        f_bottom.rowconfigure(0, weight=1)

        f_bottom_l = tk.Frame(f_bottom)
        f_bottom_l.grid(column=0, row=0, padx=5, pady=5)
        l_view = tk.Label(f_bottom_l, text=self.i18n.no_of_view, font=(None, 20, "bold"))
        l_view.grid(column= 0, row= 0)
        l_nview = tk.Label(f_bottom_l, text=result[9], font=(None, 20))
        l_nview.grid(column= 0, row= 1)

        f_bottom_c = tk.Frame(f_bottom)
        f_bottom_c.grid(column=1, row=0, padx=5)
        l_applicant = tk.Label(f_bottom_c, text=self.i18n.no_aplicants, font=(None, 20, "bold"))
        l_applicant.grid(column= 1, row= 0)
        l_applicantnum = tk.Label(f_bottom_c, text=result[10], font=(None, 20))
        l_applicantnum.grid(column= 1, row= 1)

        f_bottom_r = tk.Frame(f_bottom)
        f_bottom_r.grid(column=0, row=1, columnspan=2, pady=20)
        b_apply = tk.Button(f_bottom_r, text=self.i18n.apply, font=(None, 25), command=lambda : self.add_applicant(result[11], username)) #username parameter used here
        b_apply.pack(side=tk.LEFT, padx=5)
        b_cancel = tk.Button(f_bottom_r,text=self.i18n.cancel, font=(None, 25), command=lambda: parent.cancel_applypage())
        b_cancel.pack(side=tk.LEFT)


    def config_width(self):
        self.canv.itemconfig(self.frame_id, width=self.winfo_width())


    def add_applicant(self, p, u):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT username FROM applicants WHERE username=?", (u,))
        username = c.fetchone()
        if not username:
            c.execute("insert into applicants (job_id, username) VALUES (?, ?)", (p, u))
            conn.commit()
            conn.close()
            msg.showinfo("info!", self.i18n.succesfull_application)
        else:
            msg.showinfo("info!", self.i18n.already_appilied)
            conn.close()
