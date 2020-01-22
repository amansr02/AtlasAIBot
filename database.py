import sqlite3 
import os

class Database():
    #dictionary as database
    def __init__(self):
        self.default_path = os.path.join(os.path.dirname(__file__),'db.sqlite3')
        self.con = sqlite3.connect(self.default_path) 
        self.cursor = self.con.cursor()
        #self.cursor.execute('''CREATE TABLE IF NOT EXISTS atlas(
        #        CourseID TEXT PRIMARY KEY,
        #        CourseName TEXT, 
        #        Median TEXT,
        #        Workload INTEGER,
        #        DuringClass TEXT,
        #        AfterClass TEXT,
        #        AdvPrequisites TEXT, 
        #        EnfPrequisites TEXT, 
        #        URL TEXT,
        #        SeniorPerc INTEGER,
        #        JuniorPerc INTEGER,
        #        SophomorePerc INTEGER,
        #        FreshmenPerc INTEGER,
        #        GradPerc INTEGER,
        #        AplusPerc INTEGER,
        #        APerc INTEGER,
        #        AminusPerc INTEGER,
        #        BplusPerc INTEGER,
        #        BPerc INTEGER,
        #        BminusPerc INTEGER,
        #        CplusPerc INTEGER,
        #        CPerc INTEGER,
        #        CminusPerc INTEGER
        #        )''') 
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS atlas(
                CourseID TEXT PRIMARY KEY,
                CourseName TEXT, 
                Median TEXT,
                Workload INTEGER)''')
        self.con.commit()

    def create_entry(self,table_entry):
        s = 'insert into atlas values(?,?,?,?)'
        self.cursor.execute(s,table_entry)
        self.con.commit()

    def update_entry(self):
        pass

    def delete_entry(self):
        pass

    def read(self,class_id):
        s = "SELECT * FROM atlas WHERE CourseID =?"
        self.cursor.execute(s,(class_id,))
        return self.cursor.fetchone()

    def read_median(self,median):
        s = "Select * FROM atlas WHERE Median=?"
        self.cursor.execute(s,(median,))
        return self.cursor.fetchall()

    def read_workload(self,workload):
        s = "Select * FROM atlas WHERE Workload=?"
        self.cursor.execute(s,(workload,))
        return self.cursor.fetchone()

    def __del__(self):
        self.cursor.close()
        self.con.close()
