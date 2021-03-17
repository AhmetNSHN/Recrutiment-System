import os
import tkinter as tk
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk
from languages import I18N

class profile(tk.Frame):
    def __init__(self, parent, username, l_mode):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.i18n = I18N(l_mode)


        con = sqlite3.connect("database.db")
        c = con.cursor()
        c.execute(
            "SELECT username, f_name, l_name, ssn, date_of_birth, gender, occupation, description, email, phone_n, adress ,picture, cv FROM users "
            "Where username=?", (username,))
        info = c.fetchone()

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

        main_f = tk.Frame(center)
        main_f.pack(expand=False)
        main_f.columnconfigure(0, weight=3)
        main_f.columnconfigure(1, weight=7, minsize=600)

        picture_f = tk.Frame(main_f)
        picture_f.grid(column=0, row=0)


        picture_c = tk.Canvas(picture_f,width=150, height=150, borderwidth=0, highlightthickness=0)
        picture_c.grid(row=0, column=0, padx=0, pady=0, sticky='nesw')

        with open("temporary.png", 'wb') as file:
            file.write(info[11])
        pic = Image.open('temporary.png')
        picture_c.image = ImageTk.PhotoImage(pic.resize((150, 150), Image.ANTIALIAS))
        picture_c.create_image(0, 0, image=picture_c.image, anchor='nw')
        os.remove("temporary.png")
        l_username = tk.Label(picture_f, text=username, font=(None, 15, "bold"))
        l_username.grid(column=0, row=1)

        info_f = tk.LabelFrame(main_f, width=300, height=20, bd=0)
        info_f.grid(column=1, row=0, sticky=tk.NSEW)
        info_f.grid_propagate(False)

        centeralize_f = tk.Frame(info_f, bd=0)
        centeralize_f.pack(expand=True)
        l_fullname = tk.Label(centeralize_f, text=f"{info[1]} {info[2]}", font=(None, 20))
        l_fullname.pack()
        l_occupation = tk.Label(centeralize_f, text=info[6], font=(None, 20))
        l_occupation.pack()
        l_email = tk.Label(centeralize_f, text=f"{info[8]}", font=(None, 20))
        l_email.pack()

        l_about = tk.Label(main_f, text="", wraplength=750)
        l_about.grid(column=0, row=1, columnspan=2)
        l_about["text"] = f"{self.i18n.about_me}\n{info[7]}\n{self.i18n.ssn}{info[3]}\n{self.i18n.dob} {info[4]}\n{self.i18n.gender} {info[5]}\n" \
                          f"{self.i18n.adress}{info[10]}\n{self.i18n.phone_number}{info[9]}"

        if info[12]:
            b_downloadcv = tk.Button(main_f, text=self.i18n.d_cv, font=(None, 18), command=lambda: self.open_cv(info[12]))
            b_downloadcv.grid(column=0, row=2, columnspan=2 ,pady=10)
        else:
            b_downloadcv = tk.Button(main_f, text=self.i18n.cv_disable, font=(None, 15), state="disabled")
            b_downloadcv.grid(column=0, row=2, columnspan=2 ,pady=10)

        b_goback = tk.Button(main_f, text=self.i18n.go_back, font=(None, 18), command=lambda: parent.goback_jobdetails())
        b_goback.grid(column=0, row=3, columnspan=2, pady=10)

    def open_cv(self, p_data):
        if os.path.exists("cv.pdf"):
            os.remove("cv.pdf")
        with open("cv.pdf", 'wb') as file:
            file.write(p_data)
        os.system("open cv.pdf") #--------------> for windows os.startfile("cv.pdf") -----------------

    def config_width(self):
        self.canv.itemconfig(self.frame_id, width=self.winfo_width())

