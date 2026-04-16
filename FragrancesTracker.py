import sqlite3
import time
import smtplib
import random
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- 1. MAİL AYARLARI ---
GONDERICI_MAIL = "ozguraltinisik999@gmail.com" 
UYGULAMA_SIFRESI = "vrhkxjlzaxkhxyvk" 

# --- 2. MAİL GÖNDERME FONKSİYONU ---
def mail_gonder(alici_mail, urun_adi, urun_linki, guncel_fiyat):
    try:
        mesaj = MIMEMultipart()
        mesaj["From"] = GONDERICI_MAIL
        mesaj["To"] = alici_mail
        mesaj["Subject"] = f"🔥 İndirim Alarmı: {urun_adi} Fiyatı Düştü!"

        govde = f"""
        Merhaba,
        
        Takip ettiğin parfümün fiyatı beklediğin seviyeye veya altına düştü!
        
        Ürün: {urun_adi}
        Güncel Fiyat: {guncel_fiyat} TL
        
        Hemen incelemek veya satın almak için linke tıkla:
        {urun_linki}
        
        İyi alışverişler,
        ParfumBot
        """
        
        mesaj.attach(MIMEText(govde, "plain", "utf-8"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GONDERICI_MAIL, UYGULAMA_SIFRESI)
        server.send_message(mesaj)
        server.quit()
        print(f"📧 MAİL BAŞARIYLA GÖNDERİLDİ -> {alici_mail}")
    except Exception as e:
        print(f"❌ Mail gönderilirken hata oluştu: {e}")

# --- 3. PARFÜM LİSTESİ ---
PARFUMLER = [
    {
        "isim": "Armani Stronger With You Intensly 50ml",
        "url": "https://www.boyner.com.tr/armani-stronger-with-you-intensely-50-ml-erkek-parfum-p-797958"
    },
    {
        "isim": "Yves Saint Lauren MYSLF EDP 60ml",
        "url": "https://www.boyner.com.tr/myslf-edp-60ml-erkek-parfum-p-1731365"
    },
    {
        "isim": "Jean Paul Gaultier Le Beau EDT 125ml",
        "url": "https://www.boyner.com.tr/jean-paul-gaultier-le-beau-edt-125-ml-parfum-p-898062"
    },
    {
        "isim": "Dior Sauvage EDP 100ml",
        "url": "https://www.boyner.com.tr/dior-sauvage-edp-erkek-parfum-100-ml-p-755619"
    },
    {
        "isim": "Rabanne Invictus Victory Absolu 100ml",
        "url": "https://www.boyner.com.tr/rabanne-invictus-victory-absolu-100-ml-erkek-parfum-p-15537364"
    },
    {
        "isim": "Tom Ford Ombre Leather EDP 100ml",
        "url": "https://www.boyner.com.tr/ombre-leather-eau-de-parfum-100ml-p-783897"
    },
    {
        "isim": "Kenzo Homme Marine EDT 100ml",
        "url": "https://www.boyner.com.tr/homme-marine-edt-110ml-erkek-parfum-p-1671668"
    },
    {
        "isim": "Valentino Born In Roma Uomo EDT 100ml",
        "url": "https://www.boyner.com.tr/valentino-born-in-roma-uomo-edt-100-ml-erkek-parfum-p-959121"
    },
    {
        "isim": "Rabanne 1 Million Parfum EDP 100ml",
        "url": "https://www.boyner.com.tr/rabanne-1-million-parfum-edp-100-ml-erkek-parfum-p-987874"
    },
    {
        "isim": "Armani Code EDP 125ml",
        "url": "https://www.boyner.com.tr/armani-code-edp-125-ml-erkek-parfum-p-15056888"
    },
    {
        "isim": "Versace Eros Najim Parfum 100ml",
        "url": "https://www.boyner.com.tr/versace-eros-najim-parfum-100-ml-erkek-parfum-p-15539816"
    },
    {
        "isim": "Carolina Herrera Bad Boy Cobalt EDP 100ml",
        "url": "https://www.boyner.com.tr/carolina-herrera-bad-boy-cobalt-edp-100-ml-parfum-p-1129858"
    }
]

# --- 4. VERİTABANI HAZIRLIĞI ---
def veritabanini_hazirla():
    db = sqlite3.connect("parfum_fiyatlari.db")
    cursor = db.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fiyat_gecmisi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        urun_adi TEXT,
        magaza TEXT,
        url TEXT,
        fiyat REAL,
        tarih TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fiyat_takibi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kullanici_mail TEXT,
        urun_adi TEXT,
        hedef_fiyat REAL,
        aktif_mi BOOLEAN DEFAULT 1
    )
    """)
    db.commit()
    return db, cursor

db, cursor = veritabanini_hazirla()

# --- 5. TARAYICI AYARLARI ---
print("Tarayıcı Ninja Modunda başlatılıyor...")
options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
wait = WebDriverWait(driver, 15)

def fiyati_temizle(fiyat_metni):
    try:
        temiz = fiyat_metni.replace("TL", "").replace("₺", "").strip()
        temiz = temiz.replace(".", "")
        temiz = temiz.replace(",", ".")
        return float(temiz)
    except:
        return 0.0

bugunun_tarihi = datetime.now().strftime("%Y-%m-%d")

# --- 6. ANA İŞLEM DÖNGÜSÜ ---
try:
    for parfum in PARFUMLER:
        urun_adi = parfum["isim"]
        url = parfum["url"]
        
        print(f"\n[{urun_adi}] için siteye gidiliyor...")
        driver.get(url)
        time.sleep(4) 
        
        fiyat_metni = ""
        try:
            fiyat_elementi = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2[class*='price_priceMain']")))
            fiyat_metni = fiyat_elementi.text
        except Exception as e:
            print(f"HATA: {urun_adi} fiyatı bulunamadı. Stokta olmayabilir.")

        if fiyat_metni:
            temiz_fiyat = fiyati_temizle(fiyat_metni)
            print(f"✅ Fiyat Bulundu: {temiz_fiyat} TL")
            
            # 1. Fiyatı geçmiş tablosuna kaydet
            cursor.execute("INSERT INTO fiyat_gecmisi (urun_adi, magaza, url, fiyat, tarih) VALUES (?, ?, ?, ?, ?)", 
                           (urun_adi, "Boyner", url, temiz_fiyat, bugunun_tarihi))
            
            # 2. ALARM KONTROLÜ (YENİ EKLENDİ)
            # Bu parfümü takip eden, hedef fiyatı güncel fiyattan büyük/eşit olan ve alarmı aktif olan kişileri bul
            cursor.execute("""
                SELECT id, kullanici_mail, hedef_fiyat 
                FROM fiyat_takibi 
                WHERE urun_adi = ? AND hedef_fiyat >= ? AND aktif_mi = 1
            """, (urun_adi, temiz_fiyat))
            
            alarmlar = cursor.fetchall()
            
            for alarm_id, alici_mail, hedef_fiyat in alarmlar:
                print(f"🔔 Hedef fiyata ulaşıldı! {alici_mail} adresine bildirim atılıyor...")
                
                # Maili gönder
                mail_gonder(alici_mail, urun_adi, url, temiz_fiyat)
                
                # Her gün aynı maili atmamak için alarmı pasife (0) çek
                cursor.execute("UPDATE fiyat_takibi SET aktif_mi = 0 WHERE id = ?", (alarm_id,))
            
            db.commit()


        bekleme_suresi = random.uniform(3, 6)
        print(f"Uyarı yememek için {bekleme_suresi:.1f} saniye bekleniyor...\n")
        time.sleep(bekleme_suresi)

finally:
    driver.quit()
    db.close()
    print("\nTüm parfümler tarandı, işlem başarıyla tamamlandı!")