# -*- coding: utf-8 -*-
"""ÜSTAD APK İndirme Merkezi — link listesi üretici.
apk/ klasörünü tarar ve USTAD-APK-INDIR-LINKLER.txt dosyasını yeniden yazar.
Kullanım:  python link-uret.py
"""
import pathlib

S = pathlib.Path(__file__).resolve().parent
APK = S / "apk"
CIKTI = S.parent / "USTAD-APK-INDIR-LINKLER.txt"
TABAN = "https://raw.githubusercontent.com/kenankuzucu/ustad-apk-indir/main/apk/"

dosyalar = sorted([p for p in APK.glob("*.apk")], key=lambda p: p.name.lower())
uygulama = set()
for p in dosyalar:
    # "USTAD-KOC-PRO-v2.4" → uygulama adı sürümden önceki kısım
    ad = p.name[:-4]
    uygulama.add(ad.split("-v")[0] if "-v" in ad else ad)
toplam_bayt = sum(p.stat().st_size for p in dosyalar)

satir = []
satir.append("ÜSTAD UYGULAMALARI · APK İNDİRME LİNKLERİ")
satir.append("==========================================")
satir.append("Sayfa (telefondan açılır): https://kenankuzucu.github.io/ustad-apk-indir/")
satir.append("Depo (kod burada değil, sadece APK): https://github.com/kenankuzucu/ustad-apk-indir")
satir.append("Toplam: %d uygulama · %d APK dosyası · %.0f MB" % (len(uygulama), len(dosyalar), toplam_bayt / 1048576))
satir.append("")
satir.append("Doğrudan indirme linkleri (her biri kendi APK'sı, hepsi girişsiz çalışır):")
satir.append("")
for i, p in enumerate(dosyalar, 1):
    satir.append("%2d. %s  (%s byte)" % (i, p.name, format(p.stat().st_size, ",")))
    satir.append("    " + TABAN + p.name)
satir.append("")
satir.append("© 2026 Kenan Kuzucu · Tüm hakları saklıdır (5846 FSEK).")
CIKTI.write_text("\r\n".join(satir) + "\r\n", encoding="utf-8")
print("yazıldı:", CIKTI)
print("uygulama: %d · dosya: %d · toplam: %.0f MB" % (len(uygulama), len(dosyalar), toplam_bayt / 1048576))
for p in dosyalar:
    if "KOC-PRO" in p.name or "KPSS" in p.name:
        print("   ", p.name, p.stat().st_size)
