import sqlite3

# Veritabanı dosya yolunu tek bir değişkenden yönetiyoruz
DB_YOLU = r'C:\Users\MrUqu\Documents\GitHub\Python\4-YapayZeka\Database.db'

# --- 1. SOHBET / ÖĞRETME SİSTEMİ VERİTABANI İŞLEMLERİ ---

def tabloyu_olustur():
    """Sohbet ve abonelik tablolarını oluşturur."""
    with sqlite3.connect(DB_YOLU, timeout=10) as conn:
        cursor = conn.cursor()
        
        # Konuşma / Öğretme Tablosu
        cursor.execute('''CREATE TABLE IF NOT EXISTS metinler 
                         (konusma TEXT PRIMARY KEY, cevap TEXT)''')
        
        # Abonelik Tablosu
        cursor.execute('''CREATE TABLE IF NOT EXISTS subscribers (
                            user_id INTEGER PRIMARY KEY,
                            is_subscribed BOOLEAN DEFAULT 0,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )''')
        conn.commit()

def cevap_bul(soru: str): 
    """Veritabanından öğretilen cevabı getirir."""
    with sqlite3.connect(DB_YOLU, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT cevap FROM metinler WHERE konusma = ?", (soru,))
        sonuc = cursor.fetchone()
        return sonuc[0] if sonuc else None

def yeni_ogret(soru: str, cevap: str):
    """Soru ve cevabı veritabanına kaydeder/günceller."""
    with sqlite3.connect(DB_YOLU, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO metinler (konusma, cevap) VALUES (?, ?)
            ON CONFLICT(konusma) DO UPDATE SET cevap = excluded.cevap
        """, (soru, cevap))
        conn.commit()

# --- 2. TELEGRAM ABONELİK SİSTEMİ VERİTABANI İŞLEMLERİ ---

def set_subscription(user_id: int, status: bool):
    """Kullanıcının abonelik durumunu günceller veya yeni kullanıcı ekler."""
    with sqlite3.connect(DB_YOLU, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO subscribers (user_id, is_subscribed) 
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET is_subscribed = excluded.is_subscribed
        """, (user_id, status))
        conn.commit()

def get_active_subscribers():
    """Aboneliği True (1) olan kullanıcıların ID'lerini listeler."""
    with sqlite3.connect(DB_YOLU, timeout=10) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM subscribers WHERE is_subscribed = 1")
        rows = cursor.fetchall()
        return [row[0] for row in rows]