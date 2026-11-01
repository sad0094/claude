"""
Audi A3 8P arka silecek motoru (Valeo, 8E9 955 711E) - büyük dişli (sonsuz vida çarkı)
Parametrik model -> STL üretir.

Kullanım:  pip install manifold3d numpy
           python3 disli.py            (disli.stl dosyasını yazar)

ÖNEMLİ: Ölçüler referans görselden oranlanarak tahmin edildi. Baskıdan önce
aşağıdaki "ÖLÇ" yazan değerleri kumpasla orijinal parçadan ölçüp güncelleyin.
"""
import math
import numpy as np
from manifold3d import CrossSection, Manifold, set_circular_segments

set_circular_segments(96)

# ---------------- ANA PARAMETRELER ----------------
Z = 105                 # diş sayısı (görselden sayıldı)
DIS_CAP = 64.2          # ÖLÇ: dişlerin uçtan uca dış çapı (mm)
MODUL = DIS_CAP / (Z + 2)
BASINC_ACISI = 20.0     # derece
HELIS_ACISI = 5.0       # ÖLÇ/KONTROL: dişlerin eğimi (sonsuz vida adımı). 0 = düz diş
HELIS_YONU = 1          # 1 = sağ, -1 = sol (orijinal dişlerin eğim yönüne bakın)
BOSLUK = 0.10           # diş kalınlığından radyal boşluk (mm), baskı toleransı

DISLI_YUKSEKLIK = 8.0   # ÖLÇ: diş/çember genişliği (mm)
TABAN_KALINLIK = 1.6    # ÖLÇ: arka düz diskin kalınlığı (mm)
KABURGA_YUKSEKLIK = 6.0 # ÖLÇ: iç kaburgaların tabandan yüksekliği (mm)
GOBEK_YUKSEKLIK = 8.0   # ÖLÇ: orta göbek/krank kolunun yüksekliği (mm)

MERKEZ_DELIK = 6.7      # ÖLÇ: orta mil deliği çapı (mm)
KRANK_DELIK = 6.6       # ÖLÇ: krank pimi deliği çapı (mm)
KUCUK_DELIK = 2.5       # ÖLÇ: 3 küçük delik çapı (mm)
DELIK_TOLERANS = 0.2    # deliklere eklenen baskı payı (mm)

# --------------- görsel ölçek (px -> mm) ---------------
S = DIS_CAP / 741.0     # referans görselde dış çap 741 px


def P(px, py):
    """Görsel koordinatı -> model koordinatı (mm, merkez orijin, y yukarı)."""
    return ((px - 369.0) * S, -(py - 844.5) * S)


def involute_tooth_profile():
    m, z = MODUL, Z
    a = math.radians(BASINC_ACISI)
    rp = m * z / 2
    rb = rp * math.cos(a)
    ra = rp + m
    rf = rp - 1.25 * m
    # diş kalınlığı açısı (pitch çemberinde), boşluk dahil
    half_t = (math.pi / (2 * z)) - BOSLUK / (2 * rp)
    inv = lambda al: math.tan(al) - al
    half_base = half_t + inv(a)          # temel çemberde yarım açı
    pts_r = []
    for r in np.linspace(max(rb, rf), ra, 10):
        al = math.acos(min(1.0, rb / r))
        th = half_base - inv(al)
        pts_r.append((r, th))
    right = [(r * math.cos(-th), r * math.sin(-th)) for r, th in pts_r]
    left = [(r * math.cos(th), r * math.sin(th)) for r, th in reversed(pts_r)]
    r0 = rf - 0.3
    th0 = half_base + 0.02
    pts_poly = [(r0 * math.cos(-th0), r0 * math.sin(-th0))] + right + left + \
           [(r0 * math.cos(th0), r0 * math.sin(th0))]
    return poly(pts_poly), rf, ra, rp


def gear_ring_2d():
    tooth, rf, ra, rp = involute_tooth_profile()
    sec = CrossSection.circle(rf)
    for i in range(Z):
        sec = sec + tooth.rotate(360.0 * i / Z)
    return sec, rf, rp


def poly(pts):
    """Yön fark etmeksizin çokgen oluştur."""
    c = CrossSection([pts])
    return c if c.area() > 0 else CrossSection([list(reversed(pts))])


def rib(p1, p2, w):
    (x1, y1), (x2, y2) = p1, p2
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    nx, ny = -dy / L * w / 2, dx / L * w / 2
    return poly([(x1 + nx, y1 + ny), (x2 + nx, y2 + ny),
                 (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)])


def circ(c, d):
    return CrossSection.circle(d / 2).translate(c)


def build():
    gear2d, rf, rp = gear_ring_2d()
    rim_in = 294 * S
    H = DISLI_YUKSEKLIK

    # --- dişli çember (helisel) ---
    ring2d = gear2d - CrossSection.circle(rim_in)
    twist = 0.0
    if HELIS_ACISI:
        twist = math.degrees(H * math.tan(math.radians(HELIS_ACISI)) / rp) * HELIS_YONU
    ring = Manifold.extrude(ring2d, H, n_divisions=24, twist_degrees=twist)

    # --- arka disk ---
    base = Manifold.extrude(CrossSection.circle(rim_in + 0.5), TABAN_KALINLIK)

    # --- kaburgalar ---
    C = P(369, 844.5)
    w = 20 * S
    R = rim_in + 0.3

    def at(ang_deg, r=R):  # görsel açısı (y aşağı) -> model noktası
        a = math.radians(ang_deg)
        return (r * math.cos(a), -r * math.sin(a))

    ribs = CrossSection()
    for ang in (0, 180, 32, 59, 120, 148):
        ribs = ribs + rib(C, at(ang), w)
    ribs = ribs + rib(C, P(396, 1071.5), w)            # alttaki boşa giden kaburga
    ribs = ribs + rib(P(396, 1071.5), at(90), w)
    yk = 665                                           # üstteki yatay kirişler
    xk = math.sqrt(max(R ** 2 - ((844.5 - yk) * S) ** 2, 0)) / S
    ribs = ribs + rib(P(369 - xk, yk), P(369 + xk, yk), w)
    ribs = ribs + rib(P(369, 658), at(250), w) + rib(P(369, 658), at(290), w)
    ribs = ribs ^ CrossSection.circle(R)
    rib3d = Manifold.extrude(ribs, KABURGA_YUKSEKLIK)

    # --- göbek + krank kolu ---
    hub_c, crank_c = P(369, 844.5), P(369, 658)
    arm = (circ(hub_c, 180 * S) + circ(crank_c, 144 * S)).hull()
    tri_l = poly([P(312, 705), P(360, 745), P(312, 772)])
    tri_r = poly([P(426, 705), P(426, 772), P(378, 745)])
    arm = arm - tri_l - tri_r
    hub3d = Manifold.extrude(arm, GOBEK_YUKSEKLIK)

    # --- 3 küçük boss ---
    small = [P(551.7, 706.7), P(158.7, 754.7), P(396.4, 1071.5)]
    boss = CrossSection()
    for c in small:
        boss = boss + circ(c, 70 * S)
    boss3d = Manifold.extrude(boss, KABURGA_YUKSEKLIK)

    part = ring + base + rib3d + hub3d + boss3d

    # --- delikler ---
    big = H * 3
    holes = [Manifold.cylinder(big, (MERKEZ_DELIK + DELIK_TOLERANS) / 2).translate((*hub_c, -H)),
             Manifold.cylinder(big, (KRANK_DELIK + DELIK_TOLERANS) / 2).translate((*crank_c, -H))]
    for c in small:
        holes.append(Manifold.cylinder(big, (KUCUK_DELIK + DELIK_TOLERANS) / 2).translate((*c, -H)))
    for h in holes:
        part = part - h
    return part


def write_stl(m, path):
    mesh = m.to_mesh()
    v = np.asarray(mesh.vert_properties)[:, :3]
    f = np.asarray(mesh.tri_verts)
    with open(path, "wb") as fh:
        fh.write(b"silecek disli".ljust(80, b" "))
        fh.write(np.uint32(len(f)).tobytes())
        rec = np.zeros(len(f), dtype=[("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")])
        tri = v[f]
        n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
        rec["n"], rec["v"] = n, tri
        fh.write(rec.tobytes())


if __name__ == "__main__":
    import sys
    part = build()
    out = sys.argv[1] if len(sys.argv) > 1 else "disli.stl"
    write_stl(part, out)
    bb = part.bounding_box()
    print(f"modül={MODUL:.4f}  dış çap={DIS_CAP}  hacim={part.volume():.1f} mm3  "
          f"bbox={tuple(round(x, 2) for x in bb)}  genus={part.genus()}")
    print("yazıldı:", out)
