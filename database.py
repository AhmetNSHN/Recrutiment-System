import sqlite3
conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS users(
             username TEXT PRIMARY KEY,
             password TEXT,
             f_name  TEXT  NOT NULL,
             l_name  TEXT  NOT NULL,
             SSN TEXT,
             date_of_birth  TEXT,
             gender TEXT,
             occupation TEXT,
             description TEXT,
             phone_n TEXT,
             email TEXT,
             adress TEXT,
             picture BLOB,
             cv BLOB);""")

c.execute("""CREATE TABLE IF NOT EXISTS employer(
             username TEXT PRIMARY KEY,
             password TEXT,
             company_name TEXT UNIQUE,
             company_details TEXT);""")

c.execute("""CREATE TABLE IF NOT EXISTS jobs(
             job_id INTEGER PRIMARY KEY AUTOINCREMENT,
             job_title TEXT UNIQUE,
             job_category TEXT,
             company_name TEXT,
             job_description TEXT,
             required_qualifications TEXT,
             responsibilities TEXT,
             location TEXT,
             view INT,
             applicants_num INT,
             FOREIGN KEY (company_name) REFERENCES employer (company_name));""")


c.execute("""CREATE TABLE IF NOT EXISTS applicants(
             job_id INT,
             username INT,
             FOREIGN KEY (job_id) REFERENCES jobs (job_id),
             FOREIGN KEY (username) REFERENCES users (username));""")


conn.commit()
conn.close()