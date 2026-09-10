import os
import sqlite3

# Dinamik Yol (Windows/Linux/Docker sorunsuz çalışır)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_YOLU = os.path.join(BASE_DIR, "Database.db")

def tabloyu_olustur():
    """Abonelik ve Kullanıcı tablolarını oluşturur."""
    with sqlite3.connect(DB_YOLU, timeout=10) as conn:
        cursor = conn.cursor()
        
        # Abonelik Tablosu
        cursor.execute('''CREATE TABLE IF NOT EXISTS subscribers (
                            user_id INTEGER PRIMARY KEY,
                            is_subscribed BOOLEAN DEFAULT 0,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )''')
        conn.commit()

def set_subscription(user_id: int, status: bool):
    """Kullanıcının abonelik durumunu günceller."""
    with sqlite3.connect(DB_YOLU, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO subscribers (user_id, is_subscribed) 
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET is_subscribed = excluded.is_subscribed
        """, (user_id, status))
        conn.commit()

def get_active_subscribers():
    """Aboneliği aktif olan kullanıcı ID'lerini getirir."""
    with sqlite3.connect(DB_YOLU, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM subscribers WHERE is_subscribed = 1")
        rows = cursor.fetchall()
        return [row[0] for row in rows]