import tkinter as tk
from tkinter import *
from tkinter import ttk, scrolledtext, filedialog
import sqlite3
from tkinter import messagebox as msg
from functions import center_screen_geometry, days, months, years
import mainPageEmployee as main
import apply_page as ap
import mainPageCompany as comp
import job_details_page as jb
import user_profile as up
import add_adv as ad
from languages import I18N


class login_frame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.i18n = I18N("EN")
        self.language = "EN"
        self.parent = parent

        lf_radiobuttons = tk.LabelFrame(self)
        lf_radiobuttons.grid(column=1, row=0, pady=5, columnspan=2)
        self.mode = 0
        self.rd_var = tk.IntVar()
        self.rd1 = tk.Radiobutton(lf_radiobuttons, text=self.i18n.employer, variable=self.rd_var, value=1,command=self.radio_handler)
        self.rd1.pack(side=tk.RIGHT)
        self.rd2 = tk.Radiobutton(lf_radiobuttons, text=self.i18n.job_seeker, variable=self.rd_var, value=0, command=self.radio_handler)
        self.rd2.pack(side=tk.RIGHT)
        self.rd2.select()

        self.l_warning = tk.Label(self, text="", font=44)
        self.l_warning.grid(column=1, row=1)

        self.usernameLabel = tk.Label(self, text=self.i18n.username, font=44)
        self.username = tk.StringVar()
        self.usernameTextField = tk.Entry(self, width=35, textvariable=self.username)
        self.usernameLabel.grid(column=0, row=2)
        self.usernameTextField.grid(column=1, row=2)

        self.showPassPhoto = PhotoImage(
            file='hidePassword.jpg')
        self.showPassPhoto = self.showPassPhoto.subsample(30, 30)
        self.hidePassPhoto = PhotoImage(
            file='Hide Password.png')
        self.hidePassPhoto = self.hidePassPhoto.subsample(50, 50)

        self.passwordLabel = tk.Label(self, text=self.i18n.password, font=44)
        self.password = tk.StringVar()
        self.passwordTextField = tk.Entry(self, width=35, textvariable=self.password, show="*")
        self.passwordLabel.grid(column=0, row=3)
        self.passwordTextField.grid(column=1, row=3)



        self.b_language = tk.Button(self, text="EN", command=lambda: self.reload_gui_text("TR" if self.language == "EN" else "EN"))
        self.b_language.grid(column=2, row=2)

        self.showPassword = tk.Button(self, image=self.showPassPhoto, command=self.showPasword_Handler)
        self.showPassword.grid(column=2, row=3)



        self.loginButton = tk.Button(self, text=self.i18n.login, width=50, command=self.check_user)
        self.loginButton.grid(column=0, row=4, columnspan=2, pady=(25, 0))

        self.createAccountButton = tk.Label(self, text=self.i18n.do_you_have_account)
        self.createAccountButton.bind("<Button-1>", lambda event : parent.login_to_register(self.mode, self.language))
        self.createAccountButton.grid(column=0, row=5, columnspan=2)


    def radio_handler(self):
        selection = self.rd_var.get()
        if selection == 0:
            self.mode = 0# normal mode
        else:
            self.mode = 1# employer mode


    def showPasword_Handler(self):
        if (self.showPassword.cget('image')[0] == 'pyimage2'):
            self.showPassword.configure(image=self.hidePassPhoto)
            self.passwordTextField.configure(show='')
            # print(showPassword.cget('image'))
        else:
            self.showPassword.configure(image=self.showPassPhoto)
            self.passwordTextField.configure(show='*')
            # print(showPassword.cget('image'))


    def check_user(self):
        username = self.username.get()
        password = self.password.get()
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        if self.mode == 0:
            c.execute("SELECT username, password, f_name, l_name FROM users WHERE username = ? AND password = ?",
                      (username, password))
        else:
            c.execute("SELECT username, password FROM employer WHERE username = ? AND password = ?",
                      (username, password))
        results = c.fetchone()
        if results:
            self.l_warning.configure(text=self.i18n.please_wait, fg="green")
            conn.close()
            if(self.mode == 0):#employee mode
                self.parent.login_to_main(results[0], self.language)  # calling this function to change frame

            if (self.mode == 1):  # employer mode
                self.parent.login_to_main_company(results[0], self.language)

        else:
            self.l_warning.configure(text=self.i18n.invalid_u_p, fg="red")
            conn.close()

    def reload_gui_text(self, language):
        self.language = language
        self.i18n = I18N(language)
        self.rd1.configure(text=self.i18n.job_seeker)
        self.rd2.configure(text=self.i18n.employer)
        self.usernameLabel.configure(text=self.i18n.username)
        self.passwordLabel.configure(text=self.i18n.password)
        self.loginButton.configure(text=self.i18n.login)
        self.createAccountButton.configure(text=self.i18n.do_you_have_account)
        self.b_language["text"] = language



class register_frame(tk.Frame):
    def __init__(self, parent, p_mode, l_mode):  #mode 1 is employer 0 is employee
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.mode = p_mode
        self.i18n = I18N(l_mode)

        self.l_username = tk.Label(self, text=self.i18n.username, font=44)
        self.l_username.grid(column=0, row=0, pady=5)
        self.s_username = tk.StringVar()
        tb_username = tk.Entry(self, width=35, textvariable=self.s_username)
        tb_username.grid(column=1, row=0, columnspan=4)

        self.l_password = tk.Label(self, text=self.i18n.password, font=44)
        self.l_password.grid(column=0, row=1, pady=5)
        self.s_password = tk.StringVar()
        tb_password = tk.Entry(self, width=35, textvariable=self.s_password)
        tb_password.grid(column=1, row=1, columnspan=4)

        if p_mode == 0:
            self.l_firstname = tk.Label(self, text=self.i18n.fname, font=44)
            self.l_firstname.grid(column=0, row=2, pady=5)
            self.s_firstname = tk.StringVar()
            tb_firstname = tk.Entry(self, width=35, textvariable=self.s_firstname)
            tb_firstname.grid(column=1, row=2, columnspan=4)

            self.l_lastname = tk.Label(self, text=self.i18n.lname, font=44)
            self.l_lastname.grid(column=0, row=3, pady=5)
            self.s_lastname = tk.StringVar()
            tb_lastname = tk.Entry(self, width=35, textvariable=self.s_lastname)
            tb_lastname.grid(column=1, row=3, columnspan=4)

            self.l_ssn = tk.Label(self, text=self.i18n.ssn, font=44)
            self.l_ssn.grid(column=0, row=4, pady=5)
            self.s_ssn = tk.StringVar()
            tb_ssn = tk.Entry(self, width=35, textvariable=self.s_ssn)
            tb_ssn.grid(column=1, row=4, columnspan=4)

            self.l_dob = tk.Label(self, text=self.i18n.dob_gender, font=44)
            self.l_dob.grid(column=0, row=5, pady=5)
            self.s_day = tk.StringVar()
            c_day = ttk.Combobox(self, width=3, textvariable=self.s_day, values=days(), state="readonly")
            c_day.grid(column=1, row=5, sticky=tk.W)
            self.s_month = tk.StringVar()
            c_month = ttk.Combobox(self, width=3, textvariable=self.s_month, values=months(),
                                   state="readonly")
            c_month.grid(column=2, row=5, sticky=tk.W)
            self.s_year = tk.StringVar()
            c_year = ttk.Combobox(self, width=5, textvariable=self.s_year, values=years(),
                                  state="readonly")
            c_year.grid(column=3, row=5, sticky=tk.W)

            self.s_gender = tk.StringVar()
            self.c_gender = ttk.Combobox(self, width=5, textvariable=self.s_gender, values=("Male", "Female"),
                                         state="readonly")
            self.c_gender.grid(column=4, row=5, sticky=tk.W)

            self.l_email = tk.Label(self, text=self.i18n.email, font=44)
            self.l_email.grid(column=0, row=6, pady=5)
            self.s_email = tk.StringVar()
            tb_email = tk.Entry(self, width=35, textvariable=self.s_email)
            tb_email.grid(column=1, row=6, columnspan=4)

            self.l_phone = tk.Label(self, text=self.i18n.phone_number, font=44)
            self.l_phone.grid(column=0, row=7, pady=5)
            self.s_phone = tk.StringVar()
            tb_phone = tk.Entry(self, width=35, textvariable=self.s_phone)
            tb_phone.grid(column=1, row=7, columnspan=4)

            self.l_adress = tk.Label(self, text=self.i18n.adress, font=44)
            self.l_adress.grid(column=0, row=8, pady=5)
            self.s_adress = tk.StringVar()
            tb_adress = tk.Entry(self, width=35, textvariable=self.s_adress)
            tb_adress.grid(column=1, row=8, columnspan=4)

            self.l_occupation = tk.Label(self, text=self.i18n.occupation, font=44)
            self.l_occupation.grid(column=0, row=9, pady=5)
            self.s_occupation = tk.StringVar()
            tb_occupation = tk.Entry(self, width=35, textvariable=self.s_occupation)
            tb_occupation.grid(column=1, row=9, columnspan=4)

            self.l_about = tk.Label(self, text=self.i18n.write_about_yourself)
            self.l_about.grid(column=0, row=10, pady=5, stick=tk.N)
            self.about_text = scrolledtext.ScrolledText(self, width=45, height=15, wrap=tk.WORD)
            self.about_text.grid(column=1, row=10, columnspan=4)

            self.b_picture = tk.Button(self, text=self.i18n.upload_picture, command=lambda: self.gets_picture())
            self.b_picture.grid(column=0, row=11, pady=5)
            self.s_picture = tk.StringVar()
            self.tb_picture = tk.Entry(self, width=35, textvariable=self.s_picture)
            self.tb_picture.grid(column=1, row=11, columnspan=3)

            self.b_cv = tk.Button(self, text=self.i18n.upload_cv, command=lambda: self.gets_cv())
            self.b_cv.grid(column=0, row=12, pady=5)
            self.s_cv = tk.StringVar()
            self.tb_cv = tk.Entry(self, width=35, textvariable=self.s_cv)
            self.tb_cv.grid(column=1, row=12, columnspan=3)

            self.l_warn = tk.Label(self, text="")
            self.l_warn.grid(column=1, row=13, columnspan=4, pady=5, stick=tk.N)

            self.b_register = tk.Button(self, text=self.i18n.register, command=lambda: self.database_register())
            self.b_register.grid(column=2, row=14, pady=5)

            self.b_cancel = tk.Button(self, text=self.i18n.cancel, command=lambda: self.parent.register_to_login())
            self.b_cancel.grid(column=3, row=14, pady=5)

        else:
            l_companyname = tk.Label(self, text=self.i18n.company_name, font=44)
            l_companyname.grid(column=0, row=2, pady=5)
            self.s_companyname = tk.StringVar()
            tb_companyname = tk.Entry(self, width=35, textvariable=self.s_companyname)
            tb_companyname.grid(column=1, row=2, columnspan=4)

            l_about = tk.Label(self, text=self.i18n.write_about_your_company)
            l_about.grid(column=0, row=3, pady=5, stick=tk.N)
            self.about_text = scrolledtext.ScrolledText(self, width=45, height=15, wrap=tk.WORD)
            self.about_text.grid(column=1, row=3, columnspan=4, sticky=tk.W)

            self.l_warn = tk.Label(self, text="")
            self.l_warn.grid(column=1, row=7, columnspan=4, pady=5, stick=tk.N)

            b_register = tk.Button(self, text=self.i18n.register, command=lambda: self.database_register())
            b_register.grid(column=2, row=4, pady=5)

            b_cancel = tk.Button(self, text=self.i18n.cancel, command=lambda: self.parent.register_to_login())
            b_cancel.grid(column=3, row=4, pady=5)







    def gets_picture(self):
        file_path = filedialog.askopenfilename()
        self.tb_picture.insert(0, file_path)


    def gets_cv(self):
        file_path = filedialog.askopenfilename()
        self.tb_cv.insert(0, file_path)


    def database_register(self):
        if self.mode == 0:
            entry_list = [
                self.s_username.get(),
                self.s_password.get(),
                self.s_firstname.get(),
                self.s_lastname.get(),
                self.s_ssn.get(),
                f"{self.s_year.get()}-{self.s_month.get()}-{self.s_day.get()}",
                self.s_gender.get(),
                self.s_occupation.get(),
                self.about_text.get('1.0', tk.END),
                self.s_phone.get(),
                self.s_email.get(),
                self.s_adress.get()]

        else:
            entry_list = [
                self.s_username.get(),
                self.s_password.get(),
                self.s_companyname.get(),
                self.about_text.get('1.0', tk.END)]


        if "" in entry_list:
            self.l_warn.configure(text=self.i18n.please_fill_all_required_fields, fg="red")
        else:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            if self.mode == 0:
                c.execute("SELECT username FROM users WHERE username = ?", (entry_list[0],))
            else:
                c.execute("SELECT username FROM employer WHERE username = ?", (entry_list[0],))
            results = c.fetchone()
            if results:
                self.l_warn.configure(text=self.i18n.username_taken, fg="red")
            else:
                if self.mode == 0:
                    if self.s_picture.get():
                        with open(self.s_picture.get(), 'rb') as file:
                            d_picture = file.read()
                            entry_list.append(d_picture)
                            c.execute(
                                "insert into users (username, password, f_name, l_name, SSN, date_of_birth, gender,"
                                " occupation, description, phone_n, email, adress, picture)"
                                " VALUES (?, ?, ?, ?, ?, ?, ?, ? ,? ,? ,?, ?, ?)", (entry_list))
                    else:
                        with open("default_profile_pic.png", 'rb') as file:
                            d_picture = file.read()
                            entry_list.append(d_picture)
                            c.execute(
                                "insert into users (username, password, f_name, l_name, SSN, date_of_birth, gender,"
                                " occupation, description, phone_n, email, adress, picture)"
                                " VALUES (?, ?, ?, ?, ?, ?, ?, ? ,? ,? ,?, ?, ?)", (entry_list))
                    if self.s_cv.get():
                        with open(self.s_cv.get(), 'rb') as file:
                            d_cv = file.read()
                        c.execute("UPDATE users SET cv = ? WHERE  username=?", (d_cv, entry_list[0],))
                    else:
                        pass
                else:
                    c.execute(
                        "insert into employer (username, password, company_name, company_details)"
                        " VALUES (?, ?, ?, ?)", (entry_list))

                conn.commit()
                conn.close()
                msg.showinfo("info!", "registration completed!")
                self.parent.register_to_login()






class MainW(tk.Tk):

    def __init__(self):
        Tk.__init__(self)
        self.geometry(center_screen_geometry(screen_width=self.winfo_screenwidth(),
                                                 screen_height=self.winfo_screenheight(),
                                                 window_width=650,
                                                 window_height=650))
        self.title("FindJob!")
        self.login = login_frame(self)
        self.login.pack(expand=True)

    def login_to_register(self, p_mode, l_mode):
        self.login.pack_forget()
        self.register = register_frame(self, p_mode, l_mode) #0 is employee mode
        self.register.pack(expand=True)
        self.update()

    def register_to_login(self):
        self.register.destroy()
        self.login.pack(expand=True)
        self.update()

    def login_to_main(self, p_username, l_mode):
        self.login.pack_forget()
        self.main = main.main_page_employee(self, p_username, l_mode)
        self.main.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.update()

    def login_to_main_company(self, p_username, l_mode):
        self.login.pack_forget()
        self.main = comp.main_page_company(self, p_username, l_mode)
        self.main.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.update()

    def goto_applypage(self, username, p_jobtitle, l_mode):
        self.main.pack_forget()
        self.jobdetails = ap.apply(self, username, p_jobtitle, l_mode)
        self.jobdetails.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.update()

    def goto_jobDetails(self, p_jobtitle, l_mode):
        self.main.pack_forget()
        self.jobdetails = jb.jobDetails(self, p_jobtitle, l_mode)
        self.jobdetails.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.update()

    def cancel_applypage(self):
        self.jobdetails.destroy()
        self.main.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.update()

    def goto_profilepage(self, username):
        self.jobdetails.pack_forget()
        self.profile = up.profile(self, username)
        self.profile.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.update()

    def goback_jobdetails(self):
        self.profile.destroy()
        self.jobdetails.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.update()

    def create_newjob(self ,p_username, l_mode):
        self.main.pack_forget()
        self.add = ad.create_job(self ,p_username, l_mode)
        self.add.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.update()

    def gobackfrom_newjob(self):
        self.add.destroy()
        self.main.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.update()


if __name__=="__main__":
    app = MainW()
    app.mainloop()