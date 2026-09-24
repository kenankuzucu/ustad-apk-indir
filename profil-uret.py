# -*- coding: utf-8 -*-
"""ÜSTAD APK İndirme Merkezi — animasyonlu profil madalyonu üretir ve sayfaya ekler.
Kaynak: ÜSTAD kafa logosu (tasarim/ustad-kafa.png) — Kenan'ın fotoğrafı DEĞİL.
Çıktı: profil-kafa.png (saydam köşeli, 256px) + index.html başlık bloğu.
"""
import pathlib
from PIL import Image, ImageDraw, ImageFilter

S = pathlib.Path(r"C:\Users\kenan\OneDrive\Desktop\USTAD-APK-INDIR")
KAYNAK = pathlib.Path(r"C:\Users\kenan\OneDrive\Desktop\USTAD-MOTOR-2\tasarim\ustad-kafa.png")
BOY = 256

kafa = Image.open(KAYNAK).convert("RGBA")
# logoyu daire içine sığdır
olcek = min(BOY * 0.80 / kafa.width, BOY * 0.80 / kafa.height)
kucuk = kafa.resize((int(kafa.width * olcek), int(kafa.height * olcek)), Image.LANCZOS)

taban = Image.new("RGBA", (BOY, BOY), (0, 0, 0, 0))
# yumuşak açık zemin (krem) + iç halka
zemin = Image.new("RGBA", (BOY, BOY), (0, 0, 0, 0))
d = ImageDraw.Draw(zemin)
d.ellipse((0, 0, BOY - 1, BOY - 1), fill=(255, 252, 245, 255))
d.ellipse((6, 6, BOY - 7, BOY - 7), outline=(206, 168, 92, 255), width=3)
taban.alpha_composite(zemin)
taban.alpha_composite(kucuk, ((BOY - kucuk.width) // 2, (BOY - kucuk.height) // 2))

# dış altın halka
d2 = ImageDraw.Draw(taban)
d2.ellipse((2, 2, BOY - 3, BOY - 3), outline=(212, 175, 96, 255), width=4)
parlak = taban.filter(ImageFilter.GaussianBlur(6))
sonuc = Image.alpha_composite(parlak, taban)
sonuc.save(S / "profil-kafa.png")
print("profil-kafa.png üretildi:", (S / "profil-kafa.png").stat().st_size, "byte", sonuc.size)

BLOK_ESKI = '<header>\n  <h1>⬇ ÜSTAD UYGULAMALARI · APK İNDİRME MERKEZİ</h1>'
BLOK_YENI = '''<header>
  <div class="kimlik">
    <div class="madalyon" aria-hidden="true">
      <span class="halka"></span>
      <img src="profil-kafa.png" alt="ÜSTAD amblemi">
    </div>
    <div class="kimlik-yazi">
      <h1>⬇ ÜSTAD UYGULAMALARI · APK İNDİRME MERKEZİ</h1>'''
CSS_EK = '''
.kimlik{display:flex;align-items:center;gap:18px;flex-wrap:wrap}
.madalyon{position:relative;width:112px;height:112px;flex:0 0 auto;
  animation:sallan 6s ease-in-out infinite;transform-style:preserve-3d}
.madalyon img{position:absolute;inset:10px;width:92px;height:92px;border-radius:50%;
  box-shadow:0 8px 22px rgba(0,0,0,.45);animation:nabiz 3.2s ease-in-out infinite}
.madalyon .halka{position:absolute;inset:0;border-radius:50%;
  background:conic-gradient(from 0deg,#f6d98a,#b8860b,#fff3c4,#d4af37,#8a6a12,#f6d98a);
  -webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 7px),#000 calc(100% - 6px));
          mask:radial-gradient(farthest-side,transparent calc(100% - 7px),#000 calc(100% - 6px));
  animation:don 7s linear infinite;filter:drop-shadow(0 0 6px rgba(246,217,138,.55))}
.kimlik-yazi{min-width:220px}
@keyframes don{to{transform:rotate(360deg)}}
@keyframes nabiz{0%,100%{box-shadow:0 8px 22px rgba(0,0,0,.45)}50%{box-shadow:0 8px 30px rgba(246,217,138,.75)}}
@keyframes sallan{0%,100%{transform:translateY(0) rotateY(0deg)}25%{transform:translateY(-5px) rotateY(9deg)}
  50%{transform:translateY(0) rotateY(0deg)}75%{transform:translateY(-5px) rotateY(-9deg)}}
@media (prefers-reduced-motion:reduce){.madalyon,.madalyon img,.madalyon .halka{animation:none}}
'''
yol = S / "index.html"
h = yol.read_text(encoding="utf-8")
if BLOK_ESKI not in h:
    raise SystemExit("başlık bloğu bulunamadı")
h = h.replace(BLOK_ESKI, BLOK_YENI, 1)
# h1'den sonra gelen <p> satırını kimlik-yazi içine al, header'ı kapat
eski_p = '<p>Kenan Kuzucu\'nun Android uygulamaları — hepsi kendi anahtarıyla imzalı, doğrudan kuruluma hazır.</p>'
yeni_p = ('<p>Kenan Kuzucu\'nun Android uygulamaları — hepsi kendi anahtarıyla imzalı, doğrudan kuruluma hazır.</p>\n'
          '    </div>\n  </div>')
h = h.replace(eski_p, yeni_p, 1)
h = h.replace("</style>", CSS_EK + "</style>", 1)
yol.write_text(h, encoding="utf-8")
print("index.html güncellendi:", yol.stat().st_size, "byte")
print("madalyon:", '<div class="madalyon"' in h, "| css animasyon:", "@keyframes don" in h)
