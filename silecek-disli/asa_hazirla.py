"""
Gönderilen 'Audi_gear_wipe_motor_rear.stl' dosyasını onarır ve ASA baskısına hazırlar.

  pip install trimesh manifold3d mapbox_earcut numpy scipy networkx shapely
  python3 -I asa_hazirla.py GIRDI.stl CIKTI.stl

Yapılanlar:
  1. Kopuk/çakışan gövdeler tek, su geçirmez (manifold) katıya birleştirilir.
  2. Üstteki bozuk yay çıkıntısı (stop kamı, z 8-9) temiz olarak yeniden oluşturulur.
  3. ASA delik telafisi: delikler baskıda küçüldüğü için çaplar büyütülür.
  4. Tablaya değen deliklere fil ayağı (elephant foot) pahı eklenir.
  5. Model tablaya oturacak şekilde z=0'a taşınır (orijinal yön: krank kolu altta).
"""
import sys
import numpy as np
import trimesh
import mapbox_earcut as earcut
from manifold3d import Manifold, Mesh, CrossSection, set_circular_segments

set_circular_segments(128)

# ---- ASA telafileri (mm, çap) ----
MERKEZ_UST = 10.10 + 0.20     # mil yatağı (boşluklu dönmeli)
MERKEZ_ALT = 7.00 + 0.20      # alt kademe
KRANK_PIM = 7.00 + 0.05       # metal krank pimi (sıkı geçme)
KUCUK = 2.80 + 0.20           # 3 küçük delik
PAH = 0.5                     # tabla tarafı delik ağzı pahı

C_KRANK = (0.0, -16.38)
KUCUKLER = [(2.40, 19.90), (16.03, -12.03), (-18.43, -7.87)]


def to_manifold(tm):
    return Manifold(Mesh(vert_properties=np.asarray(tm.vertices, np.float32),
                         tri_verts=np.asarray(tm.faces, np.uint32)))


def cap_planar_holes(tm):
    """z sabit düzlemdeki açık delikleri earcut ile kapat."""
    from collections import Counter
    e = tm.edges_sorted
    cnt = Counter(map(tuple, e))
    # sınır kenarlarını yönlü olarak al (yüz yönüne göre)
    bset = {k for k, v in cnt.items() if v == 1}
    directed = [(a, b) for a, b in tm.edges if tuple(sorted((a, b))) in bset]
    nxt = {a: b for a, b in directed}
    faces = []
    seen = set()
    for start in list(nxt):
        if start in seen:
            continue
        loop = [start]
        seen.add(start)
        cur = nxt[start]
        while cur != start:
            loop.append(cur); seen.add(cur); cur = nxt[cur]
        pts = tm.vertices[loop][:, :2].astype(np.float64)
        tri = earcut.triangulate_float64(pts, np.array([len(pts)], np.uint32)).reshape(-1, 3)
        idx = np.array(loop)[tri]
        # yeni yüzler sınırın tersine dönmeli
        faces.append(idx[:, ::-1])
    new = trimesh.Trimesh(tm.vertices, np.vstack([tm.faces] + faces), process=True)
    trimesh.repair.fix_normals(new)
    return new


def main(src, dst):
    m = trimesh.load(src)
    m.merge_vertices()
    parts = m.split(only_watertight=False)
    big = max(parts, key=lambda p: len(p.faces)).copy()
    big = cap_planar_holes(big)
    assert big.is_watertight, "ana gövde kapatılamadı"

    solid = to_manifold(big)
    for p in parts:
        if p.is_watertight and len(p.faces) > 4 and p is not big:
            if p.volume < 0:
                p.invert()
            solid = solid + to_manifold(p)

    # stop kamı: z=8.5 kesitinden yeniden çıkar
    sec = m.section(plane_origin=[0, 0, 8.5], plane_normal=[0, 0, 1])
    polys = []
    for e in sec.discrete:
        c = e[:, :2].mean(0)
        if np.hypot(*c) > 9:          # merkez göbek değil, yay parçası
            polys.append([tuple(p) for p in e[:-1, :2]])
    cs = CrossSection(polys)
    if cs.area() <= 0:
        cs = CrossSection([list(reversed(p)) for p in polys])
    kam = Manifold.extrude(cs, 1.3).translate((0, 0, 7.7))   # 7.7 -> 9.0
    solid = solid + kam

    # delik telafileri
    def cyl(d, z0, z1, c=(0, 0)):
        # dikiş çizgileri mevcut kenarlarla çakışmasın diye hafif döndür
        return Manifold.cylinder(z1 - z0, d / 2).rotate((0, 0, 1.7)).translate((c[0], c[1], z0))

    solid = solid - cyl(MERKEZ_UST, -2.9, 14)
    solid = solid - cyl(MERKEZ_ALT, -6, 0)
    solid = solid - cyl(KRANK_PIM, -6, 6.4, C_KRANK)
    for c in KUCUKLER:
        solid = solid - cyl(KUCUK, -6, 14, c)

    # tabla tarafı pahlar (z = -4.8)
    def pah(d, c=(0, 0)):
        return Manifold.cylinder(PAH * 2, d / 2 + PAH, d / 2 - PAH).translate((c[0], c[1], -4.8 - PAH))
    solid = solid - pah(MERKEZ_ALT) - pah(KRANK_PIM, C_KRANK)

    solid = solid.translate((0, 0, 4.8))     # tabla z=0
    out = solid.to_mesh()
    tm = trimesh.Trimesh(np.asarray(out.vert_properties)[:, :3], np.asarray(out.tri_verts))
    tm.merge_vertices()
    print("su geçirmez:", tm.is_watertight, " gövde sayısı:", len(tm.split()),
          " hacim:", round(tm.volume, 1), "mm3", " boyut:", np.round(tm.extents, 2))
    tm.export(dst)
    print("yazıldı:", dst)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
