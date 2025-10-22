# 🛡️ Integrity Checker

Python ile yazılmış bir **Dosya bütünlüğü kontrol aracı**dır.  
Seçilen klasördeki dosyaların hash değerlerini kaydeder ve değişiklikleri takip eder.

## 🔍 Özellikler

- Dosyaların SHA256 hash değerlerini hesaplar
- Yeni, değişen veya silinen dosyaları tespit eder
- '.hashes.json' dosyası ile veritabanı gibi çalışır
- Basit ve kullanıcı dostu **Tkinter GUI** arayüzü
- Hızlı tarama ve raporlama

## 🚀 Kullanım

1. Projeyi bilgisayarına indir ve klasörü aç.

2. Python ile çalıştır:

python Integrity_checker_GUI.py

3.GUI penceresinde:
 .Klasör Seç: İzlemek istediğin klasörü seç
 .Taramayı Başlat: Dosyaları tarar ve değişiklikleri listeler

4.İlk taramada .hashes.json dosyası otomatik oluşturulur.
 .Bu dosya sonraki taramalarda referans olarak kullanılır.

📁 Proje Dosya Yapısı

IntegrityTool/
├── Integrity_checker_GUI.py
├── README.md
└── .hashes.json    (otomatik oluşur)
