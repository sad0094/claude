# yonetior.com sosyal medya paketi

- `videos/` — 5 adet 1080×1920 MP4 (Reels, TikTok, Shorts)
- `covers/` — her video için kapak PNG
- `content/` — gönderi metinleri, içerik takvimi, seslendirme metinleri
- `animations/` — videoların HTML/CSS kaynağı (`base.js` içindeki `LOGO` resmi logoyla değiştirilebilir)
- `tools/render.cjs` — kaynakları MP4'e çevirir

Yeniden render: `node tools/render.cjs animations/01-uc-adimda-canliya-gec.html videos/01-uc-adimda-canliya-gec.mp4`
Önizleme karesi: `node tools/render.cjs <html> <png> --still <saniye>`
Gereksinimler: Node, Playwright, Chromium, ffmpeg, Inter yazı tipi.
