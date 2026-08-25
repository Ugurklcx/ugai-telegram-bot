import sqlite3

DB_YOLU = r'C:\Users\MrUqu\Documents\GitHub\Python\4-YapayZeka\Database.db'

def tabloyu_olustur():
    conn = sqlite3.connect(DB_YOLU, timeout=10)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS metinler 
                 (konusma TEXT, cevap TEXT)''')
    conn.commit()
    conn.close()

def cevap_bul(soru): 
    conn = sqlite3.connect(DB_YOLU, timeout=10)
    c = conn.cursor()
    c.execute("SELECT cevap FROM metinler WHERE konusma = ?", (soru,))
    sonuc = c.fetchone()
    conn.close()
    return sonuc[0] if sonuc else None

def yeni_ogret(soru, cevap):
    with sqlite3.connect(DB_YOLU, timeout=10) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM metinler WHERE konusma = ?", (soru,))
        c.execute("INSERT INTO metinler (konusma, cevap) VALUES (?, ?)", (soru, cevap))
        conn.commit()