# Audi A3 8P arka silecek motoru – büyük dişli (Valeo 8E9 955 711E)

- `disli.stl` – Bambu Studio'ya doğrudan atılabilir (taslak ölçülerle).
- `disli.py` – parametrik model. Ölçüleri güncelleyip `python3 disli.py` ile STL'yi yeniden üretin
  (`pip install manifold3d numpy`).
- `onizleme.png` – önizleme.

Diş sayısı 105 (referans görselden sayıldı). Dış çap, yükseklikler ve delik çapları **tahmindir**;
`ÖLÇ` yazan parametreleri kumpasla orijinal parçadan ölçüp güncelleyin.

Baskı: PA6-CF / PAHT-CF (yoksa PETG/ASA), 0.12 mm katman, 5–6 duvar, %100 doluluk, düz disk tarafı tabla üzerinde.

## ASA sürümü (gönderilen orijinal STL'den)
- `disli_ASA.stl` – onarılmış, tek gövde, su geçirmez; baskı yönünde (krank kolu tablada).
- `asa_hazirla.py` – orijinal STL'den bu dosyayı üreten betik.
- Delik telafisi: orta Ø10,1→10,3 / alt Ø7,0→7,2, krank pimi Ø7,0→7,05 (sıkı geçme), küçük Ø2,8→3,0; tabla tarafı delik ağızlarına 0,5 mm pah.
- Dişler, dış çap (64,76 mm, 105 diş, helisel) ve diğer ölçüler orijinalle aynı.
