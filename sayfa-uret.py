# -*- coding: utf-8 -*-
"""ÜSTAD APK İndirme Merkezi — sayfa üretici.
apk/ klasörünü tarar, index.html (animasyonlu amblemli) + README.md yazar.
Kullanım:  python sayfa-uret.py
"""
import pathlib, re, hashlib, json

S = pathlib.Path(__file__).resolve().parent
APK = S / "apk"

ADLAR = {
 "USTAD-KPSS-B": ("ÜSTAD Sınav Koçu · KPSS-B", "KPSS uzmanlık ve müfettişlik: 120 özgün soru, deneme sınavı, ders notları, anında geri bildirim."),
 "USTAD-KOC-PRO": ("ÜSTAD KPSS-B KOÇ PRO", "Sınav koçluğu paketi: KPSS ARAÇLAR + 🤖 ÜSTAD KOÇ AI (çevrimdışı koç) + SES STÜDYOSU (kadın/erkek sesi) + SESLİ DERSLER + 4 EĞİTİCİ OYUN + 🃏 KART TEKRARI (aralıklı tekrar) + 📕 YANLIŞ DEFTERİM + ⏱️ SÜRELİ MİNİ TEST + 📈 DENEME ANALİZİ (net grafiği)."),
 "USTAD-EHLIYET": ("ÜSTAD EHLİYET", "Ehliyet sınavı hazırlık: 1.100+ soru, 4 şablon, 10 tema."),
 "KALI-REHBERIM": ("KALİ REHBERİM", "Kali Linux rehberi — komut kitabı ve kullanım kılavuzu."),
 "USTAD-SIBER-EGITIM": ("ÜSTAD SİBER EĞİTİM", "Siber güvenlik eğitim içeriği."),
 "Ustad-Kenanin-Islam-Hazinesi": ("Kenan'ın İslam Hazinesi", "Dini içerik hazinesi."),
 "USTAD-KPSS": ("ÜSTAD KPSS (web sürümü)", "KPSS soru bankası ve deneme sınavı — web uygulamasının APK hâli."),
 "USTAD-KPSS-ARACLAR": ("ÜSTAD KPSS ARAÇLAR", "Sınav geri sayımı (ÖSYM takvimi + hatırlatıcı), net & puan hesaplama, not defteri, 30 kaynaklı 2026 güncel bilgi ve 2011-2021 çıkmış soru arşivi + 33 özgün soru."),
 "USTAD-SIBER": ("ÜSTAD SİBER", "Siber güvenlik paneli."),
 "Siber-ULTRA": ("SİBER ULTRA", "Siber güvenlik paketi."),
 "ustadcyber-oynatici": ("USTAD CYBER OYNATICI", "Siber içerik oynatıcı."),
 "USTAD-TV": ("ÜSTAD TV", "Kanal/IPTV oynatıcı."),
 "USTAD-TV-KOPRUSU": ("ÜSTAD TV KÖPRÜSÜ", "Telefon ile TV arasında köprü."),
 "USTAD-SALON-TV-4K": ("ÜSTAD SALON TV 4K", "Salon ekranı — QLED/OLED motoru, 4K."),
 "USTAD-PIYASA-TV": ("ÜSTAD PİYASA TV", "Piyasa ekranı (TV sürümü)."),
 "USTAD-MONITOR": ("ÜSTAD DÜNYA MONİTÖR", "Radyo + IPTV + 4 kasa paneli."),
 "USTAD-GAZETE": ("ÜSTAD GAZETE", "Gazete okuyucu."),
 "USTAD-PIYASA": ("ÜSTAD PİYASA", "Piyasa takip: döviz, altın, borsa."),
 "USTADIN-KASASI": ("ÜSTADIN KASASI", "Kasa ve gelir-gider takibi."),
 "USTAD-SALON": ("ÜSTAD SALON", "Salon (işletme) yönetimi."),
 "USTAD-KAYIT": ("ÜSTAD KAYIT", "Ses kaydı → çevrimdışı Türkçe yazıya dökme."),
 "USTAD-HATIRLATICI": ("ÜSTAD HATIRLATICI", "Hatırlatıcı — sesli okuma, 8 ses, 12 tema."),
 "USTAD-NOT": ("ÜSTAD NOTLAR", "Not uygulaması."),
 "USTAD-SIFRELI-NOTLAR": ("ÜSTAD ŞİFRELİ NOTLAR", "AES-256-GCM + PBKDF2 şifreli notlar, madalyonlu giriş."),
 "USTAD-HAVA": ("ÜSTAD HAVA", "Hava durumu."),
 "USTAD-KALEM": ("ÜSTAD KALEM", "Yazı ve şiir defteri."),
 "USTAD-TAM-KUMANDA": ("ÜSTAD TAM KUMANDA", "Kumanda aracı."),
 "USTAD-TRANSFER": ("ÜSTAD TRANSFER", "Dosya aktarım aracı."),
}
GRUP = [
 ("Sınav ve Eğitim", "#2e7d32", "📚", ["USTAD-KPSS-B", "USTAD-KOC-PRO", "USTAD-KPSS", "USTAD-KPSS-ARACLAR", "USTAD-EHLIYET", "KALI-REHBERIM", "USTAD-SIBER-EGITIM", "Ustad-Kenanin-Islam-Hazinesi"]),
 ("Siber Güvenlik", "#1565c0", "🛡️", ["USTAD-SIBER", "Siber-ULTRA", "ustadcyber-oynatici", "USTAD-TAM-KUMANDA", "USTAD-TRANSFER"]),
 ("Medya, TV ve Haber", "#6a1b9a", "📺", ["USTAD-TV", "USTAD-TV-KOPRUSU", "USTAD-SALON-TV-4K", "USTAD-PIYASA-TV", "USTAD-MONITOR", "USTAD-GAZETE"]),
 ("İşletme, Piyasa ve Kasa", "#ef6c00", "💼", ["USTAD-PIYASA", "USTADIN-KASASI", "USTAD-SALON"]),
 ("Kişisel ve Araçlar", "#ad1457", "🧰", ["USTAD-KAYIT", "USTAD-HATIRLATICI", "USTAD-NOT", "USTAD-SIFRELI-NOTLAR", "USTAD-HAVA", "USTAD-KALEM"]),
]


def coz(ad):
    g = ad[:-4]
    m = re.search(r"-v(\d+(?:\.\d+)*)(.*)$", g)
    return (g[:m.start()], m.group(1), m.group(2).strip("-")) if m else (g, "—", "")


def tara():
    uyg = {}
    for p in sorted(APK.glob("*.apk")):
        k, v, ek = coz(p.name)
        uyg.setdefault(k, []).append({"ad": p.name, "ver": v, "ek": ek,
                                      "boy": p.stat().st_size,
                                      "sha": hashlib.sha256(p.read_bytes()).hexdigest()})
    for k in uyg:
        uyg[k].sort(key=lambda v: tuple(int(x) for x in v["ver"].split(".")) if v["ver"] != "—" else (0,))
    return uyg


boy = lambda n: (f"{n/1048576:.1f} MB" if n >= 1048576 else f"{n/1024:.0f} KB")


def uret(uyg):
    gruplar = [list(g) for g in GRUP]
    bilinen = {a for g in gruplar for a in g[3]}
    kalan = sorted(set(uyg) - bilinen)
    if kalan:
        gruplar.append(["Diğer", "#455a64", "📦", kalan])
    bolum = []
    for baslik, renk, simg, uygler in gruplar:
        ic = ""
        for u in uygler:
            if u not in uyg:
                continue
            ad, acik = ADLAR.get(u, (u, ""))
            son = uyg[u][-1]
            ic += f'<div class="kart" style="border-top:4px solid {renk}">\n'
            ic += f'  <h3>{ad}</h3>\n  <p class="acik">{acik}</p>\n'
            ic += (f'  <a class="indir" style="background:{renk}" href="apk/{son["ad"]}" download>'
                   f'⬇ İNDİR · sürüm {son["ver"]} · {boy(son["boy"])}</a>\n')
            ic += f'  <div class="sha">sha256 {son["sha"][:16]}…</div>\n'
            if len(uyg[u]) > 1:
                esk = " · ".join(f'<a href="apk/{v["ad"]}" download>{v["ver"]}</a> '
                                 f'<span class="kucuk">({boy(v["boy"])})</span>' for v in uyg[u][:-1])
                ic += f'  <div class="eski">Önceki sürümler: {esk}</div>\n'
            ic += '</div>\n'
        n = len([a for a in uygler if a in uyg])
        bolum.append(f'<section><h2 style="background:{renk}">{simg} {baslik} '
                     f'<span class="sayi">{n} uygulama</span></h2><div class="izgara">\n{ic}</div></section>')
    us = len(uyg); ds = sum(len(v) for v in uyg.values()); tb = sum(v["boy"] for u in uyg for v in uyg[u])
    stil = """
*{box-sizing:border-box}
body{margin:0;font-family:"Segoe UI",Tahoma,sans-serif;background:#f1f3f6;color:#1b2430}
header{background:linear-gradient(135deg,#0d1b2a,#1b3a5c 55%,#2e7d32);color:#fff;padding:26px 18px}
.kimlik{display:flex;align-items:center;gap:18px;flex-wrap:wrap}
.madalyon{position:relative;width:112px;height:112px;flex:0 0 auto;animation:sallan 6s ease-in-out infinite;transform-style:preserve-3d}
.madalyon img{position:absolute;inset:10px;width:92px;height:92px;border-radius:50%;box-shadow:0 8px 22px rgba(0,0,0,.45);animation:nabiz 3.2s ease-in-out infinite}
.madalyon .halka{position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 0deg,#f6d98a,#b8860b,#fff3c4,#d4af37,#8a6a12,#f6d98a);
 -webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 7px),#000 calc(100% - 6px));
 mask:radial-gradient(farthest-side,transparent calc(100% - 7px),#000 calc(100% - 6px));
 animation:don 7s linear infinite;filter:drop-shadow(0 0 6px rgba(246,217,138,.55))}
.kimlik-yazi{min-width:220px}
header h1{margin:0;font-size:26px;letter-spacing:.5px}
header p{margin:8px 0 0;opacity:.92;font-size:14px}
@keyframes don{to{transform:rotate(360deg)}}
@keyframes nabiz{0%,100%{box-shadow:0 8px 22px rgba(0,0,0,.45)}50%{box-shadow:0 8px 30px rgba(246,217,138,.75)}}
@keyframes sallan{0%,100%{transform:translateY(0) rotateY(0deg)}25%{transform:translateY(-5px) rotateY(9deg)}50%{transform:translateY(0) rotateY(0deg)}75%{transform:translateY(-5px) rotateY(-9deg)}}
@media (prefers-reduced-motion:reduce){.madalyon,.madalyon img,.madalyon .halka{animation:none}}
.rozet{display:inline-block;background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.35);border-radius:20px;padding:3px 10px;margin:6px 6px 0 0;font-size:12.5px}
section{max-width:1180px;margin:22px auto;padding:0 14px}
h2{color:#fff;font-size:17px;margin:0 0 12px;padding:9px 14px;border-radius:10px}
h2 .sayi{float:right;font-weight:400;font-size:13px;opacity:.9}
.izgara{display:grid;grid-template-columns:repeat(auto-fill,minmax(255px,1fr));gap:12px}
.kart{background:#fff;border-radius:12px;padding:14px;box-shadow:0 2px 8px rgba(16,32,64,.10)}
.kart h3{margin:0 0 6px;font-size:15.5px}
.acik{margin:0 0 10px;font-size:13px;color:#54606f;min-height:36px;line-height:1.35}
.indir{display:block;text-align:center;color:#fff;text-decoration:none;font-weight:600;font-size:13.5px;padding:10px;border-radius:9px}
.sha{font-family:Consolas,monospace;font-size:10.5px;color:#8593a3;margin-top:6px;word-break:break-all}
.eski{font-size:12px;margin-top:7px;color:#5a6572}
.eski a{color:#1565c0;text-decoration:none;font-weight:600}
.kucuk{color:#8b95a1}
footer{max-width:1180px;margin:26px auto 40px;padding:14px;color:#5a6572;font-size:12.5px;text-align:center;line-height:1.6}
"""
    h = ('<!DOCTYPE html><html lang="tr"><head><meta charset="utf-8">\n'
         '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
         '<title>ÜSTAD UYGULAMALARI · APK İndirme Merkezi</title>\n<style>' + stil + '</style></head><body>\n'
         '<header>\n  <div class="kimlik">\n'
         '    <div class="madalyon" aria-hidden="true"><span class="halka"></span>'
         '<img src="profil-kafa.png" alt="ÜSTAD amblemi"></div>\n'
         '    <div class="kimlik-yazi">\n      <h1>⬇ ÜSTAD UYGULAMALARI · APK İNDİRME MERKEZİ</h1>\n'
         '      <p>Kenan Kuzucu\'nun Android uygulamaları — hepsi kendi anahtarıyla imzalı, doğrudan kuruluma hazır.</p>\n'
         f'      <span class="rozet">{us} uygulama</span><span class="rozet">{ds} APK dosyası</span>\n'
         f'      <span class="rozet">toplam {round(tb/1048576)} MB</span>'
         '<span class="rozet">kaynak kod: özel (private) depolarda</span>\n    </div>\n  </div>\n</header>\n')
    h += "\n".join(bolum)
    h += ('\n<footer>© 2026 Kenan Kuzucu · ÜSTAD SALON KENAN · Tüm hakları saklıdır (5846 sayılı FSEK).<br>\n'
          'Kurulum dosyaları ücretsizdir; kopyalanıp satılamaz, tersine mühendislikle kaynak kod çıkarılıp dağıtılamaz.<br>\n'
          'İmza: CN=Ustad Kenan Kuzucu · sha256 değerlerini indirdikten sonra doğrulayabilirsiniz.</footer>\n</body></html>')
    (S / "index.html").write_text(h, encoding="utf-8")
    sat = ["# ÜSTAD Uygulamaları — APK İndirme Merkezi", "",
           "İndirme sayfası: **https://kenankuzucu.github.io/ustad-apk-indir/**", "",
           f"{us} uygulama · {ds} imzalı APK · toplam {round(tb/1048576)} MB.",
           "Burada YALNIZCA kurulum dosyaları vardır; kaynak kodlar ayrı, özel (private) depolarda tutulur.", ""]
    for baslik, renk, simg, uygler in gruplar:
        sat += [f"### {simg} {baslik}", "", "| Uygulama | Dosya | Sürüm | Byte | sha256 |", "|---|---|---|---|---|"]
        for u in uygler:
            if u not in uyg:
                continue
            for v in uyg[u]:
                sat.append(f"| {ADLAR.get(u,(u,''))[0]} | apk/{v['ad']} | {v['ver']} | {v['boy']} | `{v['sha']}` |")
        sat.append("")
    sat += ["© 2026 Kenan Kuzucu · Tüm hakları saklıdır (5846 FSEK).", ""]
    (S / "README.md").write_text("\n".join(sat), encoding="utf-8")
    return us, ds, tb


if __name__ == "__main__":
    uyg = tara()
    us, ds, tb = uret(uyg)
    for k in sorted(uyg):
        print(f"  {k:<30} {[v['ver'] for v in uyg[k]]}")
    print(f"\nsayfa üretildi: {us} uygulama · {ds} dosya · {round(tb/1048576)} MB")
