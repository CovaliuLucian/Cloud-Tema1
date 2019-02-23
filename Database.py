import sqlite3

from Metric import Metric, Metrics
from config import Config


class Database:
    config = Config().data

    def __init__(self):
        self.conn = sqlite3.connect("CC.db")
        self.c = self.conn.cursor()
        try:
            self.c.execute(self.config["create_translation"])
            self.c.execute(self.config["create_random"])
            self.c.execute(self.config["create_se"])
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

    def metric(self, title):
        self.c.execute("SELECT COUNT(*) FROM '%s'" % title)
        count = self.c.fetchone()[0]

        self.c.execute("SELECT COUNT(*) FROM '%s' WHERE SUCCESS = 0" % title)
        failed = self.c.fetchone()[0]

        self.c.execute("SELECT AVG(LATENCY) FROM '%s'" % title)
        average_latency = self.c.fetchone()[0]

        self.c.execute("SELECT MAX(LATENCY) FROM '%s'" % title)
        max_latency = self.c.fetchone()[0]

        self.c.execute("SELECT MIN(LATENCY) FROM '%s'" % title)
        min_latency = self.c.fetchone()[0]

        return Metric(count, failed, average_latency, min_latency, max_latency)

    def metrics(self):
        return Metrics(self.metric("LOGTRANSLATION"), self.metric("LOGRANDOM"), self.metric("LOGSE"))
