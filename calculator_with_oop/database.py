import sqlite3


class Database(object):
    def __init__(self):
        self.conn = sqlite3.connect('calculator.db')
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS operations (
                        id INTEGER PRIMARY KEY,
                        operation TEXT,
                        operands TEXT,
                        result TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')
        self.conn.commit()

    def log_operation(self, operation, operands, result):
        self.cursor.execute("INSERT INTO operations (operation, operands, result) VALUES (?, ?, ?)",
                            (operation, operands, result))
        self.conn.commit()
