import sqlite3
from typing import List, Tuple, Optional

class Database:
    def __init__(self, db_name: str = "gym.db"):
        self.db_name = db_name
        self.init_database()

    def get_connection(self):
        """Veritabanı bağlantısını aç"""
        return sqlite3.connect(self.db_name)

    def init_database(self):
        """Veritabanı tablolarını oluştur"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Members tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                balance REAL NOT NULL DEFAULT 0
            )
        ''')

        # Activities tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (member_id) REFERENCES members(id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_member(self, name: str, balance: float) -> int:
        """Yeni üye ekle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO members (name, balance) VALUES (?, ?)', (name, balance))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    def get_members(self) -> List[Tuple]:
        """Tüm üyeleri getir"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, balance FROM members')
        members = cursor.fetchall()
        conn.close()
        return members

    def get_member_by_id(self, member_id: int) -> Optional[Tuple]:
        """ID'ye göre üye getir"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, balance FROM members WHERE id = ?', (member_id,))
        member = cursor.fetchone()
        conn.close()
        return member

    def delete_member(self, member_id: int):
        """Üyeyi sil"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM members WHERE id = ?', (member_id,))
        conn.commit()
        conn.close()

    def update_balance(self, member_id: int, new_balance: float):
        """Üye bakiyesini güncelle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE members SET balance = ? WHERE id = ?', (new_balance, member_id))
        conn.commit()
        conn.close()

    def add_activity(self, member_id: int, action: str):
        """Aktivite kaydı ekle"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO activities (member_id, action) VALUES (?, ?)', (member_id, action))
        conn.commit()
        conn.close()

    def get_statistics(self) -> Tuple[int, float]:
        """İstatistikleri getir (aktif üye sayısı, toplam bakiye)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Aktif üye sayısı
        cursor.execute('SELECT COUNT(*) FROM members')
        count = cursor.fetchone()[0]
        
        # Toplam bakiye
        cursor.execute('SELECT SUM(balance) FROM members')
        result = cursor.fetchone()[0]
        revenue = result if result is not None else 0
        
        conn.close()
        return count, revenue
