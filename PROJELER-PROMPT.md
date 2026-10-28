# Claude'a Verilecek Bağlam Prompt'u — Tüm Projeler

> Aşağıdaki metni yeni bir Claude sohbetinin başına yapıştır. Köşeli parantezli `[...]` yerleri kendi bilgilerinle doldur ya da sil.

---

Merhaba Claude. Ben Sadık Altun. Seninle (Claude Code / claude.ai üzerinde) son birkaç ayda birçok proje yaptık. Yeni bir sohbete başladığım için önceki çalışmaları hatırlamıyorsun; aşağıda hepsini özetliyorum. Bu bilgileri bağlam olarak kullan, bir projeden bahsettiğimde neyi kastettiğimi buradan anla ve kaldığımız yerden devam et.

## Benim hakkımda
- Türkiye'de çalışıyorum; işlerimin çoğu yerel işletmeler için web sitesi, marka kimliği, sosyal medya içeriği ve kendi yazılım ürünlerim.
- Güvenlik kamerası / teknoloji alanındaki firmam **Urasys** ve onunla bağlantılı ürünler (Pera PDKS, UlakPost, Tellal) ana odağım.
- Bambu Lab **H2S** 3D yazıcım var, fiziksel ürün/levha tasarımları da yapıyoruz.
- Benimle **Türkçe** konuş. Teknik terimleri gerektiğinde İngilizce bırakabilirsin.

## Projeler

### 1. Urasys (ana firma)
- **Kurumsal kimlik:** Logo seti, marka kılavuzu (PDF + "Urasys Marka Kılavuzu" sayfası), profil fotoğrafları, fatura/kartvizit kartı, kıyafet (iş giysisi) karar sayfaları, site yayın ZIP'i — hepsi `Urasys Kurumsal/` klasöründe.
  - *Açık konu:* Üretim vektörleri için kumaş rengi ve logo yerleşimi seçimi bekliyor.
- **Web sitesi ve sosyal medya:** Urasys web sitesi içerikleri, "Urasys İçerik Takvimi", sosyal medya post serileri.
- **Güvenlik kamerası uyarı levhası:** 3D baskıya uygun levha (siyah + turuncu PETG, ~3 sa 47 dk, 141,5 g siyah / 14,5 g turuncu). 3MF ve STL dosyaları hazır; önce deneme baskısı önerildi.

### 2. Pera PDKS (perapdks.com)
- Personel devam kontrol sistemi (PDKS) ürünü.
- **SEO denetimi yapıldı:** client-side rendering sorunu, eksik canonical ve JSON-LD, www/apex tekrarı, SVG og:image — 7 öncelikli düzeltme listelendi.
- **Sesli tanıtım animasyonları:** 5 Pera PDKS videosu render edildi.
  - *Açık konu:* "Urasys" kelimesinin seslendirmedeki telaffuzu seçilecek, ardından iki satır yeniden üretilecek.

### 3. UlakPost
- Mesajlaşma / gönderi otomasyonu ürünü (WhatsApp entegrasyonu dahil).
- Dokümanlar: "UlakPost Başlangıç Kılavuzu", "UlakPost Hata Rehberi", "Posta — Kullanım Kılavuzu", "UlakPost Sesli Tanıtım", `UlakPost/WHATSAPP-META-KURULUM-ADIMLARI.md` (onay kutulu, sıralı Meta/WhatsApp kurulum adımları).

### 4. Tellal (sosyal medya içerik yönetim yazılımı)
- Birden çok platforma içerik planlayıp yayınlayan kendi yazılımım.
- Dokümanlar: "Tellal Kullanım Kılavuzu", "Tellal — Platform Başvuru Rehberi".
- *Açık konular:*
  - Türkiye'de Ubuntu 24.04 VPS kiralanacak, SSH anahtarı eklenecek, `tellal` alan adı için A kaydı açılacak, VPS IP'si paylaşılacak.
  - TikTok geliştirici tarafı: Sandbox / `tellal-test` uygulaması, Login Kit + Content Posting API eklenmesi, hesabın Target Users'a eklenmesi, Client key'in yazılması, secret'ın `.env.local`'a konması.

### 5. Freya Kadın Sağlığı Merkezi
- Web sitesi / hasta platformu.
- Dokümanlar: "Freya Platform Planı", "Freya Platform", "Freya Kullanım Akışı", "Freya Dijital Tanıtım", kullanım şartları taslağı, footer güven ve CTA metinleri.
- Denetim raporları v1.1'e güncellendi (G-19, G-21, F-17 giderildi). *Açık konu:* 8 "Yüksek" öncelikli madde hâlâ açık.

### 6. Birberbere.com
- Berber randevu platformu: rezervasyon sitesi, marka varlıkları ve berberler için mobil uygulama yapıldı.
- *Açık konu:* Cihaz üzerindeki bildirim ayarları ve hesap kurulumları bende.

### 7. Diğer müşteri işleri
- **Which One Sandwich:** Web sitesi + "Which One SEO Planı".
- **Fox Bilişim (Balıkesir / Bigadiç):** Firma web sitesi.
- **İkonya:** "İkonya Web Yenileme Planı".
- **Görgülü Petrol:** Marka kiti + sosyal medya içerikleri.
- **Ecem Kuyumculuk:** Sosyal medya gönderileri ve Meta reklam kurgusu (öneri: detaylı hedeflemeyi boş bırak; istenirse takı ve özel gün ilgi alanlarıyla iki reklam setinde test et).
- **Opus Computer:** Dijital medya içeriği — 17 sosyal medya gönderisi (güvenlik kameraları, ürünler, rehberler) içeren `Paylasim-Listesi.html` (önizleme, kopyala butonu, paylaşım tarihi takibi, filtreler).
- **SAHADAYIZ:** Tesis sunumu ve durum raporu.

### 8. 3D baskı / donanım
- **Bambu Lab H2S uyumluluğu:** Yazıcı uyumluluğu incelendi, CHR tutucu için montaj animasyonu (1 dk 27 sn, 1080p, `CHR_Tutucu_Montaj_Animasyonu.mp4`) üretildi.

### 9. Kişisel
- Özgeçmiş / CV (Türkçe ve İngilizce sürümler).
- Haftalık plan ("Retro hafta planı"), paylaşım takvimi, yayın görev listesi.

## Benimle nasıl çalışmalısın
- Yeni bir iş istediğimde önce yukarıdaki projelerden hangisiyle ilgili olduğunu anla; marka renkleri, ton ve önceki kararlarla tutarlı kal.
- Çıktıları mümkünse kullanıma hazır ver (HTML sayfa, PDF, 3MF/STL, video, kopyala-yapıştır metin).
- "Açık konu" olarak işaretlenen maddeleri ben sormadan da hatırlat, sıradaki adımı öner.
- Bilmediğin bir detay varsa (domain, hesap bilgisi, renk kodu vb.) tahmin etme, bana sor.

[Buraya bu sohbette yapmak istediğin işi yaz.]
