import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("CC.db")
        self.c = self.conn.cursor()
        try:
            self.c.execute(
                '''CREATE TABLE LOGTRANSLATION(id TEXT , latency integer , response TEXT, success integer, request TEXT, time DATE )''')
            self.c.execute(
                '''CREATE TABLE LOGRANDOM(id TEXT , latency integer , response TEXT, success integer, request TEXT, time DATE )''')
            self.c.execute(
                '''CREATE TABLE LOGSE(id TEXT , latency integer , response TEXT, success integer, request TEXT, time DATE )''')
            self.conn.commit()
        except sqlite3.OperationalError:
            pass

    def insert_translation(self, log):
        values = (log.id, log.latency, log.response, log.success, log.request, log.date)
        self.c.execute("INSERT INTO LOGTRANSLATION VALUES (?,?,?,?,?,?)", values)
        self.conn.commit()

    def insert_random(self, log):
        values = (log.id, log.latency, log.response, log.success, log.request, log.date)
        self.c.execute("INSERT INTO LOGRANDOM VALUES (?,?,?,?,?,?)", values)
        self.conn.commit()

    def insert_se(self, log):
        values = (log.id, log.latency, log.response, log.success, log.request, log.date)
        self.c.execute("INSERT INTO LOGSE VALUES (?,?,?,?,?,?)", values)
        self.conn.commit()
