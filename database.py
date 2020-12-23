# import sqlite3
# conn = sqlite3.connect("database.db")
# c = conn.cursor()
# c.execute("""CREATE TABLE IF NOT EXISTS users(
#              username TEXT PRIMARY KEY,
#              password TEXT,
#              fullname  TEXT  NOT NULL,
#              city  TEXT,
#              country TEXT,
#              date_of_birth  TEXT,
#              gender TEXT,
#              about_me TEXT,
#              socialpoint INT,
#              biography TEXT,
#              picture BLOB);""")
#
# c.execute("""CREATE TABLE IF NOT EXISTS organizations(
#              o_num INT,,
#              org_name TEXT,
#              password TEXT,
#              description TEXT);""")
#
# c.execute("""CREATE TABLE IF NOT EXISTS event(
#              eventname TEXT PRIMARY KEY,--
#              owner TEXT,
#              date DATE,
#              duration TEXT,
#              location TEXT,
#              payment INT,
#              type TEXT,
#              max_participant INT,
#              participant_num INT,
#              description TEXT,
#              customspec INT,
#              FOREIGN KEY (owner) REFERENCES users (username));""")

# c.execute("""CREATE TABLE IF NOT EXISTS (
#              job_id INT PRIMARY KEY,
#              job_title TEXT
#              description TEXT);""")
#
# c.execute("""CREATE TABLE IF NOT EXISTS participants(
#              event_name TEXT,
#              user_name TEXT,
#              FOREIGN KEY (event_name) REFERENCES events (eventname),
#              FOREIGN KEY (user_name) REFERENCES users (username));""")
#
# conn.commit()
# conn.close()