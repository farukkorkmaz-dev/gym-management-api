import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.connect_db()

    def connect_db(self):
        # We are connecting to the database
        self.connection = sqlite3.connect("gym.db", check_same_thread=False)
        self.cursor = self.connection.cursor()
        
        # 1. MEMBERS TABLE (Replaced 'isim' with 'name')
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            balance REAL
        )""")
        
        # 2. ACTIVITY LOG TABLE
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            action TEXT,
            timestamp TEXT
        )""")
        
        self.connection.commit()

    def add_member(self, name, balance):
        query = "INSERT INTO members (name, balance) VALUES (?, ?)"
        self.cursor.execute(query, (name, balance))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_members(self):
        self.cursor.execute("SELECT * FROM members")
        return self.cursor.fetchall()

    def get_member_by_id(self, member_id):
        self.cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
        return self.cursor.fetchone()

    def update_balance(self, member_id, new_balance):
        query = "UPDATE members SET balance = ? WHERE id = ?"
        self.cursor.execute(query, (new_balance, member_id))
        self.connection.commit()

    def delete_member(self, member_id):
        self.cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
        self.connection.commit()

    def add_activity(self, member_id, action):
        # Getting current time in format: YYYY-MM-DD HH:MM:SS
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        query = "INSERT INTO activity_log (member_id, action, timestamp) VALUES (?, ?, ?)"
        self.cursor.execute(query, (member_id, action, current_time))
        self.connection.commit()
    
    def get_statistics(self):
        # Count total members
        self.cursor.execute("SELECT COUNT(*) FROM members")
        total_members = self.cursor.fetchone()[0]
        
        # Sum total balance (Total revenue potential)
        self.cursor.execute("SELECT SUM(balance) FROM members")
        result = self.cursor.fetchone()[0]
        total_balance = 0 if result is None else result
        
        return total_members, total_balance
