#!/usr/bin/env python3
"""Erzeugt die Blaupause „Plätzchenhaus Nr. 1“ als SVG (A4 hoch, viewBox in mm).

Aufruf:  python3 erzeuge_blaupause.py
Ergebnis: plaetzchenhaus-blaupause.svg   (blauer Hintergrund)
          plaetzchenhaus-druck.svg       (weißer Hintergrund, blaue Linien)
Die PDFs erzeugt pdf_export.js (Chromium/Playwright).
"""
import base64
import math
import os

HIER = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- Maße ----
T = 4            # Teigdicke
UE = 5           # Dachüberstand rundum
SPALT = 4        # Mindestabstand zwischen den Teilen

W = 76                      # Hausbreite = Giebelbreite (größtmöglich, s. Layout)
D = round(0.8 * W)          # Haustiefe (außen, inkl. Giebelwände)
HE = round(0.65 * W)        # Traufhöhe (Wandhöhe)
HG = HE + W / 2             # Firsthöhe der Giebelwand (45°)
LB = D - 2 * T              # Seitenwand steht zwischen den Giebeln
LC = D + 2 * UE             # Dachlänge
SC = math.ceil(W / 2 * math.sqrt(2) + UE)   # Dachplatte entlang der Neigung
H_GES = HG + T * math.sqrt(2)               # Höhe bis Oberkante Dach-First

# Tür (vorne), rundes Fenster (hinten), Seitenfenster
TB, TH = round(0.28 * W), round(0.62 * HE)  # Tür Breite / Höhe (oben rund)
RD = round(0.22 * W)                        # Ø rundes Fenster
RZ = HE + 13                                # Höhe Mitte rundes Fenster
FB, FH = round(0.3 * LB), round(0.45 * HE)  # Seitenfenster
FZ = round(0.56 * HE)                       # Höhe Fenstermitte
# Kleinteile
SB, SH = round(0.22 * W), 14                # Schornstein: Breite, kurze Seite
SL = SH + SB                                # lange Seite (45°)
EB, EH = TB + 12, 10                        # Vordach
LFB, LFH = FB // 2, FH                      # Fensterladen
GB, GH = TB + 8, 8                          # Türstufe
H_KAMIN = H_GES - 7 + SH                    # Oberkante Schornstein

DATUM = "18.11.2026"

# --------------------------------------------------------------- Farben ---
THEMEN = {
    "blaupause": dict(bg="#0B3D91", line="#FFFFFF", dim="#CFE3FF", txt="#FFFFFF",
                      soft="#9EC3FF", grid5="#8FB8FF", grid10="#A9CAFF",
                      g5op=0.16, g10op=0.32, face="#FFFFFF", faceop=(0.05, 0.12, 0.20),
                      hole="#062a66", boxbg="#0B3D91"),
    "druck": dict(bg="#FFFFFF", line="#0B3D91", dim="#1D5BC4", txt="#0B3D91",
                  soft="#3F76D1", grid5="#6E9BE0", grid10="#4D83D8",
                  g5op=0.14, g10op=0.26, face="#0B3D91", faceop=(0.03, 0.07, 0.12),
                  hole="#C9DAF6", boxbg="#FFFFFF"),
}


def f(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def mm(v):
    """Maßzahl als Text (ganze mm, sonst 1 Nachkommastelle)."""
    return f"{round(v)}" if abs(v - round(v)) < 0.05 else f"{v:.1f}".replace(".", ",")


class Blatt:
    def __init__(self, th):
        self.th = th
        self.o = []

    def add(self, s):
        self.o.append(s)

    # -- Grundelemente --------------------------------------------------
    def poly(self, pts, cls="cut", close=True, extra=""):
        d = "M" + " L".join(f"{f(x)},{f(y)}" for x, y in pts) + (" Z" if close else "")
        self.add(f'<path class="{cls}" d="{d}" {extra}/>')

    def line(self, a, b, cls="dimln"):
        self.add(f'<line class="{cls}" x1="{f(a[0])}" y1="{f(a[1])}" x2="{f(b[0])}" y2="{f(b[1])}"/>')

    def text(self, x, y, s, size=2.4, cls="t", anchor="start", rot=0, weight=None):
        tr = f' transform="rotate({f(rot)} {f(x)} {f(y)})"' if rot else ""
        w = f' font-weight="{weight}"' if weight else ""
        self.add(f'<text class="{cls}" x="{f(x)}" y="{f(y)}" font-size="{f(size)}" '
                 f'text-anchor="{anchor}"{w}{tr}>{s}</text>')

    def arrow(self, tip, d, cls="arr", L=2.2, Wd=0.55):
        """Gefüllter Maßpfeil, Spitze bei tip, zeigt in Richtung d."""
        ux, uy = d
        n = math.hypot(ux, uy)
        ux, uy = ux / n, uy / n
        bx, by = tip[0] - ux * L, tip[1] - uy * L
        self.poly([tip, (bx - uy * Wd, by + ux * Wd), (bx + uy * Wd, by - ux * Wd)], cls)

    def dim(self, p1, p2, off, txt=None, size=2.3):
        """Klassische Bemaßung: Maßhilfslinien, Maßlinie, Pfeile, Maßzahl."""
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        nx, ny = -uy, ux
        s = 1 if off >= 0 else -1
        a = (p1[0] + nx * off, p1[1] + ny * off)
        b = (p2[0] + nx * off, p2[1] + ny * off)
        for p, q in ((p1, a), (p2, b)):
            self.line((p[0] + nx * 0.8 * s, p[1] + ny * 0.8 * s),
                      (q[0] + nx * 1.4 * s, q[1] + ny * 1.4 * s))
        if L >= 7.5:
            self.line(a, b)
            self.arrow(a, (-ux, -uy))
            self.arrow(b, (ux, uy))
        else:   # kurze Maße: Pfeile von außen
            self.line((a[0] - ux * 4, a[1] - uy * 4), (b[0] + ux * 4, b[1] + uy * 4))
            self.arrow(a, (ux, uy))
            self.arrow(b, (-ux, -uy))
        ang = math.degrees(math.atan2(dy, dx))
        if ang > 90.01 or ang <= -90.01:
            ang -= 180 if ang > 0 else -180
        r = math.radians(ang)
        upx, upy = math.sin(r), -math.cos(r)
        mx, my = (a[0] + b[0]) / 2 + upx * 0.7, (a[1] + b[1]) / 2 + upy * 0.7
        self.text(mx, my, txt if txt is not None else mm(L), size, "dimt", "middle", ang)

    def mittel(self, a, b, ext=3):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        self.line((a[0] - ux * ext, a[1] - uy * ext), (b[0] + ux * ext, b[1] + uy * ext), "ctr")

    def marke(self, x, y, buchst, titel, anzahl, size=1.0):
        """Teilekennung: Buchstabe im Kreis + Name + Stückzahl."""
        r = 3.4 * size
        self.add(f'<circle class="mk" cx="{f(x)}" cy="{f(y)}" r="{f(r)}"/>')
        self.text(x, y + 1.55 * size, buchst, 4.4 * size, "t", "middle", weight=700)
        if titel:
            self.text(x, y + r + 3.3 * size, titel, 2.3 * size, "t", "middle", weight=700)
        if anzahl:
            self.text(x, y + r + 6.2 * size, anzahl, 2.3 * size, "ts", "middle")


# ------------------------------------------------------- Schablonen -------
def to_page(ox, oy, pts):
    """Teilkoordinaten (x rechts, y hoch, Ursprung unten links) -> Blatt."""
    return [(ox + x, oy - y) for x, y in pts]


def kreisbogen_tuer(cx, unten, b, h, n=18):
    """Tür mit Rundbogen oben (Teilkoordinaten)."""
    r = b / 2
    pts = [(cx - r, unten), (cx + r, unten), (cx + r, unten + h - r)]
    for i in range(1, n):
        a = math.pi * i / n
        pts.append((cx + r * math.cos(a), unten + h - r + r * math.sin(a)))
    pts.append((cx - r, unten + h - r))
    return pts


def giebel(bl, ox, oy, vorn, dims_links=True, dims_rechts=False):
    umriss = [(0, 0), (W, 0), (W, HE), (W / 2, HG), (0, HE)]
    bl.poly(to_page(ox, oy, umriss), "cut")
    bl.mittel((ox + W / 2, oy - HG), (ox + W / 2, oy), 3)
    # Breite unten
    bl.dim((ox, oy), (ox + W, oy), 6)
    if dims_links:
        bl.dim((ox, oy - HE), (ox, oy), 5)                      # Traufhöhe
    if dims_rechts:
        xh = ox + W / 2 + 17
        bl.dim((xh, oy), (xh, oy - HG), 0.01)                   # Firsthöhe
        bl.line((ox + W / 2 + 1, oy - HG), (xh + 1.4, oy - HG))
    # 45°-Winkel an der linken Traufe
    r = 9
    a0 = (ox + r, oy - HE)
    a1 = (ox + r * math.cos(math.radians(45)), oy - HE - r * math.sin(math.radians(45)))
    bl.add(f'<path class="dimln" d="M{f(a0[0])},{f(a0[1])} A{r},{r} 0 0 0 {f(a1[0])},{f(a1[1])}"/>')
    bl.line((ox, oy - HE), (ox + r + 2, oy - HE), "dimln")
    bl.text(ox + r + 0.8, oy - HE - 2.4, "45°", 2.3, "dimt")
    if vorn:
        tuer = kreisbogen_tuer(W / 2, 0, TB, TH)
        bl.poly(to_page(ox, oy, tuer), "hole")
        bl.dim((ox + W / 2 - TB / 2, oy - TH - 1), (ox + W / 2 + TB / 2, oy - TH - 1), -3)
        bl.dim((ox + W / 2 + TB / 2, oy), (ox + W / 2 + TB / 2, oy - TH), 4)
        bl.text(ox + W / 2, oy - TH / 2 + 3.0, "ausstechen", 1.9, "ts", "middle")
        bl.text(ox + W / 2, oy - 3.2, "TÜR", 1.9, "ts", "middle")
        bl.marke(ox + 15, oy - HE + 15, "A", "GIEBEL", "VORN · 1×")
        bl.text(ox + W / 2, oy - TH + TB / 2 + 1.0, "R " + mm(TB / 2), 1.9, "dimt", "middle")
    else:
        cx, cy = ox + W / 2, oy - RZ
        bl.add(f'<circle class="hole" cx="{f(cx)}" cy="{f(cy)}" r="{f(RD / 2)}"/>')
        bl.mittel((cx - RD / 2, cy), (cx + RD / 2, cy), 2.5)
        bl.dim((cx - RD / 2, cy), (cx + RD / 2, cy), 0.01, "Ø" + mm(RD), 2.0)
        bl.dim((ox + W / 2 - RD / 2 - 3, oy), (ox + W / 2 - RD / 2 - 3, oy - RZ), 0.01)
        bl.text(cx, cy + RD / 2 + 3.2, "ausstechen", 1.9, "ts", "middle")
        bl.marke(ox + W / 2, oy - HE / 2 - 4, "A", "GIEBEL", "HINTEN · 1×")


def seitenwand(bl, ox, oy):
    bl.poly(to_page(ox, oy, [(0, 0), (LB, 0), (LB, HE), (0, HE)]), "cut")
    fx0 = (LB - FB) / 2
    fy0 = FZ - FH / 2
    bl.poly(to_page(ox, oy, [(fx0, fy0), (fx0 + FB, fy0), (fx0 + FB, fy0 + FH), (fx0, fy0 + FH)]), "hole")
    bl.mittel((ox + LB / 2, oy - HE), (ox + LB / 2, oy), 2)
    bl.mittel((ox, oy - FZ), (ox + LB, oy - FZ), 2)
    bl.dim((ox, oy), (ox + LB, oy), 6)
    bl.dim((ox, oy - HE), (ox, oy), 5)
    bl.dim((ox + fx0, oy - fy0 - FH), (ox + fx0 + FB, oy - fy0 - FH), -2.5)
    bl.dim((ox + fx0 + FB, oy - fy0), (ox + fx0 + FB, oy - fy0 - FH), -3)
    bl.dim((ox + fx0 - 3.5, oy), (ox + fx0 - 3.5, oy - fy0), 0.01)
    bl.text(ox + LB / 2, oy - FZ + 4.3, "ausstechen", 1.7, "ts", "middle")
    bl.marke(ox + 7, oy - HE + 6, "B", None, None, 0.8)
    bl.text(ox + LB / 2 + 4, oy - HE + 6.0, "", 1)
    bl.text(ox + LB / 2, oy - 7.5, "SEITENWAND · 2×", 2.2, "t", "middle", weight=700)
    bl.text(ox + LB / 2, oy - 4.2, f"= Tiefe {D} − 2×{T}", 1.8, "ts", "middle")


def dach(bl, ox, oy):
    bl.poly(to_page(ox, oy, [(0, 0), (LC, 0), (LC, SC), (0, SC)]), "cut")
    bl.mittel((ox + LC / 2, oy - SC), (ox + LC / 2, oy), 2)
    bl.dim((ox, oy), (ox + LC, oy), 6)
    bl.dim((ox, oy - SC), (ox, oy), 5)
    bl.text(ox + LC / 2, oy - SC + 4.5, "FIRST", 2.0, "ts", "middle")
    bl.text(ox + LC / 2, oy - 2.5, "TRAUFE (5 mm Überstand)", 1.8, "ts", "middle")
    bl.marke(ox + LC / 2, oy - SC / 2 - 7, "C", "DACHPLATTE", "2×")


def schornstein(bl, ox, oy):
    # Teilkoordinaten: links kurze Seite (firstseitig), unten 45°-Schräge
    pts = [(0, SB), (SB, 0), (SB, SL), (0, SL)]   # y hoch
    pts = [(0, SL - SH), (SB, 0), (SB, SL), (0, SL)]
    bl.poly(to_page(ox, oy, pts), "cut")
    bl.dim((ox, oy - SL), (ox + SB, oy - SL), -4)
    bl.dim((ox + SB, oy), (ox + SB, oy - SL), 4)
    bl.dim((ox, oy - SL), (ox, oy - (SL - SH)), 4)
    bl.text(ox + 3.5, oy - 3, "45°", 2.0, "dimt")
    bl.marke(ox + SB / 2, oy - SL + 7.2, "D", None, None, 0.8)
    bl.text(ox + SB / 2 + 0.6, oy - SL + 15.3, "2×", 2.2, "t", "middle", weight=700)


def rechteck_teil(bl, ox, oy, b, h, buchst, info, dl=True, db=True, marke_rechts=None):
    bl.poly(to_page(ox, oy, [(0, 0), (b, 0), (b, h), (0, h)]), "cut")
    if db:
        bl.dim((ox, oy), (ox + b, oy), 4.5)
    if dl:
        bl.dim((ox, oy - h), (ox, oy), 4.5)
    if h >= 9:
        bl.text(ox + b / 2, oy - h / 2 + 1.5, buchst, 3.6, "t", "middle", weight=700)
    else:
        bl.text(ox + b / 2, oy - h / 2 + 1.2, buchst, 3.0, "t", "middle", weight=700)


# ---------------------------------------------------- Isometrie -----------
C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))
SICHT = (1, -1, 1)


def sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def add3(a, b): return (a[0] + b[0], a[1] + b[1], a[2] + b[2])
def mul(a, k): return (a[0] * k, a[1] * k, a[2] * k)
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def norm(a):
    n = math.sqrt(dot(a, a))
    return (a[0] / n, a[1] / n, a[2] / n)


class Prisma:
    def __init__(self, name, basis, n, dicke, versatz, buchst=None, oeffnung=None, label_off=(0, 0)):
        self.name, self.basis, self.n = name, basis, norm(n)
        self.dicke, self.versatz, self.buchst = dicke, versatz, buchst
        self.oeffnung = oeffnung or []      # Liste von 3D-Polygonen (auf Basisfläche)
        self.label_off = label_off

    def ecken(self, explodiert=True):
        v = self.versatz if explodiert else (0, 0, 0)
        unten = [add3(p, v) for p in self.basis]
        oben = [add3(p, mul(self.n, self.dicke)) for p in unten]
        return unten, oben

    def mitte(self, explodiert=True):
        u, o = self.ecken(explodiert)
        pts = u + o
        return tuple(sum(p[i] for p in pts) / len(pts) for i in range(3))


def iso(p, ox, oy, s):
    x, y, z = p
    return (ox + s * (x + y) * C30, oy - s * (z + (y - x) * S30))


def zeichne_prisma(bl, pr, ox, oy, s):
    th = bl.th
    unten, oben = pr.ecken()
    c = pr.mitte()
    faces = [(oben, pr.n), (list(reversed(unten)), mul(pr.n, -1))]
    k = len(unten)
    for i in range(k):
        q = [unten[i], unten[(i + 1) % k], oben[(i + 1) % k], oben[i]]
        nn = norm(cross(sub(q[1], q[0]), sub(q[3], q[0])))
        mq = mul(add3(add3(q[0], q[1]), add3(q[2], q[3])), 0.25)
        if dot(nn, sub(mq, c)) < 0:
            nn = mul(nn, -1)
        faces.append((q, nn))
    sicht = norm(SICHT)
    for poly, nn in faces:
        d = dot(nn, sicht)
        if d <= 1e-6:
            continue
        # Helligkeit nach Ausrichtung
        if nn[2] > 0.5:
            op = th["faceop"][2]
        elif nn[0] > 0.5:
            op = th["faceop"][1]
        else:
            op = th["faceop"][0]
        pts = [iso(p, ox, oy, s) for p in poly]
        bl.poly(pts, "isobg")
        bl.poly(pts, "isof", extra=f'fill-opacity="{op}"')
    # Öffnungen auf der sichtbaren Großfläche
    oben_sichtbar = dot(pr.n, sicht) > 0
    for oe in pr.oeffnung:
        pts3 = [add3(p, pr.versatz) for p in oe]
        if oben_sichtbar:
            pts3 = [add3(p, mul(pr.n, pr.dicke)) for p in pts3]
        bl.poly([iso(p, ox, oy, s) for p in pts3], "isohole")


def explosion(bl, rx0, ry0, rx1, ry1, s=1/3):
    E = 20
    r2 = 1 / math.sqrt(2)
    teile = []
    # Giebel
    gieb = [(0, 0), (W, 0), (W, HE), (W / 2, HG), (0, HE)]
    tuer = kreisbogen_tuer(W / 2, 0, TB, TH, 12)
    vorn = Prisma("A vorn", [(x, 0, z) for x, z in gieb], (0, -1, 0), T, (0, -E - 6, 0), "A",
                  [[(x, 0, z) for x, z in tuer]], (-1, -3))
    # Basis vorn bei y=T, Normale -y  -> Platte von y=T bis y=0
    vorn.basis = [(x, T, z) for x, z in gieb]
    vorn.oeffnung = [[(x, T, z) for x, z in tuer]]
    kreis = [(W / 2 + RD / 2 * math.cos(a), D - T, RZ + RD / 2 * math.sin(a))
             for a in [2 * math.pi * i / 24 for i in range(24)]]
    hinten = Prisma("A hinten", [(x, D - T, z) for x, z in gieb], (0, 1, 0), T, (0, E, 0), "A",
                    [kreis], (0, -16))
    # Seitenwände (zwischen den Giebeln)
    fy0 = (LB - FB) / 2
    fz0 = FZ - FH / 2

    def wand(x0, nx, vers):
        bas = [(x0, T, 0), (x0, T + LB, 0), (x0, T + LB, HE), (x0, T, HE)]
        fen = [(x0, T + fy0, fz0), (x0, T + fy0 + FB, fz0), (x0, T + fy0 + FB, fz0 + FH), (x0, T + fy0, fz0 + FH)]
        return Prisma("B", bas, (nx, 0, 0), T, vers, "B", [fen])
    links = wand(T, -1, (-E, 0, 0))
    rechts = wand(W - T, 1, (E, 0, 0))
    rechts.label_off = (4, 2)
    # Dachplatten: Unterseite auf der Giebelschräge
    def dachplatte(seite):
        sx = -1 if seite == "l" else 1
        u = (sx * r2, 0, -r2)               # vom First zur Traufe
        R = (W / 2, 0, HG)
        tr = add3(R, mul(u, SC))
        bas = [(R[0], -UE, R[2]), (R[0], D + UE, R[2]), (tr[0], D + UE, tr[2]), (tr[0], -UE, tr[2])]
        nrm = (sx * r2, 0, r2)
        vers = add3(mul(nrm, 18), (0, 0, 8))
        return Prisma("C", bas, nrm, T, vers, "C")
    dl, dr = dachplatte("l"), dachplatte("r")
    dr.label_off = (6, 0)
    # Schornstein auf rechter Dachseite (2 Lagen à 4 mm)
    xs = W / 2 + 7
    roof = lambda x: HG + T * math.sqrt(2) - (x - W / 2)
    ztop = roof(xs) + SH
    sch = [(xs, ztop - SH), (xs + SB, roof(xs + SB)), (xs + SB, ztop), (xs, ztop)]
    yc = D * 0.55
    d1 = Prisma("D1", [(x, yc, z) for x, z in sch], (0, -1, 0), T, (0, -7, 30), "D")
    d2 = Prisma("D2", [(x, yc, z) for x, z in sch], (0, 1, 0), T, (0, 5, 30), "D")
    d1.label_off = (-6, 4)
    # Vordach (flach auf Giebel vorn)
    ez0 = TH + 3
    vd = Prisma("E", [(W / 2 - EB / 2, 0, ez0), (W / 2 + EB / 2, 0, ez0), (W / 2 + EB / 2, 0, ez0 + EH),
                      (W / 2 - EB / 2, 0, ez0 + EH)], (0, -1, 0), T, (0, -E - 6 - 22, 6), "E")
    # Türstufe
    st = Prisma("G", [(W / 2 - GB / 2, -GH, 0), (W / 2 + GB / 2, -GH, 0), (W / 2 + GB / 2, 0, 0),
                      (W / 2 - GB / 2, 0, 0)], (0, 0, 1), T, (0, -E - 6 - 24, -10), "G")
    # Fensterläden rechts (sichtbar) und links
    def laden(x0, nx, y0, vers):
        bas = [(x0, y0, fz0), (x0, y0 + LFB, fz0), (x0, y0 + LFB, fz0 + LFH), (x0, y0, fz0 + LFH)]
        return Prisma("F", bas, (nx, 0, 0), T, vers, "F")
    fl = [laden(W, 1, T + fy0 - LFB - 0.5, (E + 18, 0, 0)), laden(W, 1, T + fy0 + FB + 0.5, (E + 18, 0, 0)),
          laden(0, -1, T + fy0 - LFB - 0.5, (-E - 18, 0, 0)), laden(0, -1, T + fy0 + FB + 0.5, (-E - 18, 0, 0))]
    fl[1].buchst = None
    fl[3].buchst = None
    fl[2].label_off = (-2, -3)
    teile = [hinten, links, dl, d2, d1, dr, rechts, vorn, vd, st] + fl
    # Blatt-Ursprung so wählen, dass die Explosion mittig im Bereich sitzt
    alle = []
    for pr in teile:
        u, o = pr.ecken()
        alle += [iso(p, 0, 0, s) for p in u + o]
    bx0, bx1 = min(p[0] for p in alle), max(p[0] for p in alle)
    by0, by1 = min(p[1] for p in alle), max(p[1] for p in alle)
    ox = (rx0 + rx1) / 2 - (bx0 + bx1) / 2
    oy = (ry0 + ry1) / 2 - (by0 + by1) / 2
    print(f"Explosion: {bx1-bx0:.1f} x {by1-by0:.1f} mm (Bereich {rx1-rx0:.0f} x {ry1-ry0:.0f})")

    # Grundriss (Teller) strichpunktiert
    fp = [(0, 0, 0), (W, 0, 0), (W, D, 0), (0, D, 0)]
    bl.poly([iso(p, ox, oy, s) for p in fp], "ctr")
    # Montagelinien (hinter den Teilen)
    def montage(pr, idx):
        u, _ = pr.ecken(False)
        for i in idx:
            a = u[i]
            b = add3(a, pr.versatz)
            pa, pb = iso(a, ox, oy, s), iso(b, ox, oy, s)
            bl.line(pb, pa, "mont")
    montage(vorn, [0, 1, 3]); montage(hinten, [1, 3]); montage(links, [0, 3]); montage(rechts, [0, 2])
    montage(dl, [0, 3]); montage(dr, [0, 3]); montage(d1, [3]); montage(d2, [2])
    montage(vd, [0, 1]); montage(st, [0, 1])
    for lf in fl:
        montage(lf, [0])
    # Teile nach Tiefe sortiert zeichnen (fern -> nah)
    key = lambda pr: dot(pr.mitte(), SICHT)
    for pr in sorted(teile, key=key):
        zeichne_prisma(bl, pr, ox, oy, s)
    # Montagepfeile (über den Teilen) in Bewegungsrichtung
    def pfeil(pr, i, frac=0.5):
        u, _ = pr.ecken(False)
        a = u[i]
        b = add3(a, pr.versatz)
        pa, pb = iso(a, ox, oy, s), iso(b, ox, oy, s)
        m = (pb[0] + (pa[0] - pb[0]) * frac, pb[1] + (pa[1] - pb[1]) * frac)
        bl.arrow(m, (pa[0] - pb[0], pa[1] - pb[1]), "arr", 1.8, 0.6)
    pfeil(vorn, 0); pfeil(hinten, 1, 0.6); pfeil(links, 0); pfeil(rechts, 0)
    pfeil(dl, 3, 0.55); pfeil(dr, 3, 0.55); pfeil(d1, 3, 0.6); pfeil(d2, 2, 0.6)
    pfeil(vd, 0, 0.5); pfeil(st, 1, 0.5); pfeil(fl[0], 0, 0.55); pfeil(fl[2], 0, 0.55)
    # Kennbuchstaben
    for pr in teile:
        if not pr.buchst:
            continue
        p = iso(pr.mitte(), ox, oy, s)
        x, y = p[0] + pr.label_off[0], p[1] + pr.label_off[1]
        bl.add(f'<circle class="mkiso" cx="{f(x)}" cy="{f(y)}" r="2.5"/>')
        bl.text(x, y + 1.15, pr.buchst, 3.2, "t", "middle", weight=700)


# ----------------------------------------------------------- Blatt --------
def font_css():
    css = ""
    for gew, datei in ((400, "CourierPrime-Regular.ttf"), (700, "CourierPrime-Bold.ttf")):
        with open(os.path.join(HIER, "fonts", datei), "rb") as fh:
            b64 = base64.b64encode(fh.read()).decode()
        css += (f"@font-face{{font-family:'Courier Prime';font-weight:{gew};"
                f"src:url(data:font/ttf;base64,{b64}) format('truetype');}}\n")
    return css


def erzeuge(thema):
    th = THEMEN[thema]
    bl = Blatt(th)
    # Hintergrund + Raster
    bl.add(f'<rect x="0" y="0" width="210" height="297" fill="{th["bg"]}"/>')
    g5, g10 = [], []
    for x in range(10, 201, 5):
        (g10 if x % 10 == 0 else g5).append(f"M{x},10 V287")
    for y in range(10, 288, 5):
        (g10 if y % 10 == 0 else g5).append(f"M10,{y} H200")
    bl.add(f'<path d="{" ".join(g5)}" stroke="{th["grid5"]}" stroke-opacity="{th["g5op"]}" stroke-width="0.1" fill="none"/>')
    bl.add(f'<path d="{" ".join(g10)}" stroke="{th["grid10"]}" stroke-opacity="{th["g10op"]}" stroke-width="0.22" fill="none"/>')
    # Doppelrahmen
    bl.add('<rect class="frame1" x="10" y="10" width="190" height="277"/>')
    bl.add('<rect class="frame2" x="12" y="12" width="186" height="273"/>')

    # ---------- Kopf
    bl.text(15, 20.5, "PLÄTZCHENHAUS NR. 1", 6.4, "t", weight=700)
    bl.text(15, 25.6, "SCHABLONEN M 1:1 · TEIGDICKE 4 mm · SCHNITTLINIEN DURCHGEZOGEN", 2.25, "ts")
    # 50-mm-Kontrolllinie
    kx, ky = 15, 30
    bl.line((kx, ky), (kx + 50, ky), "cut")
    for i in range(0, 51, 10):
        h = 1.6 if i % 50 == 0 else 0.9
        bl.line((kx + i, ky - h), (kx + i, ky + h), "dimln")
    bl.text(kx + 52, ky + 0.8, "← 50 mm: mit 100 % gedruckt?", 1.9, "ts")
    # Endmaße-Kasten
    bx, by, bw, bh = 121, 14.5, 75, 17.5
    bl.add(f'<rect class="box" x="{bx}" y="{by}" width="{bw}" height="{bh}"/>')
    bl.text(bx + 2, by + 4.0, "ENDMASSE DES HAUSES", 2.5, "t", weight=700)
    bl.text(bx + 2, by + 9.4, f"B {W} × T {D} × H {round(H_GES)} mm", 4.3, "t", weight=700)
    bl.text(bx + 2, by + 13.0, f"Breite = Giebel · Tiefe = Seite inkl. Giebel", 1.8, "ts")
    bl.text(bx + 2, by + 15.9, f"Höhe bis First inkl. Dach · mit Schornstein ≈ {round(H_KAMIN)} mm", 1.8, "ts")

    # ---------- Reihe 1: Giebelwände
    y1 = 37
    oy1 = y1 + HG
    ax1 = 25
    giebel(bl, ax1, oy1, True, dims_links=True)
    ax2 = ax1 + W + 7
    giebel(bl, ax2, oy1, False, dims_links=False, dims_rechts=True)
    # Überschrift A in der Ecke links oben
    bl.text(15, y1 - 0.3, "A · GIEBELWAND · 2×", 2.6, "t", weight=700)
    bl.text(15, y1 + 2.6, "(vorn Tür, hinten rundes Fenster)", 1.8, "ts")

    # Kleinteile in den Zwickeln über den Traufen
    # F Fensterladen – links oben (stehend)
    fx, fy = 15.5, y1 + 9 + LFH
    rechteck_teil(bl, fx, fy, LFB, LFH, "F", "", dl=False)
    bl.dim((fx + LFB, fy), (fx + LFB, fy - LFH), 3.5)
    bl.text(15, y1 + 6.3, "F · FENSTERLADEN · 4×", 2.1, "t", weight=700)
    # E Vordach – im Zwickel zwischen den Giebeln
    vx = (ax1 + W / 2 + ax2 + W / 2) / 2
    ex, ey = vx - EB / 2, y1 + 5 + EH
    rechteck_teil(bl, ex, ey, EB, EH, "E", "")
    bl.text(vx, y1 + 3, "E · VORDACH · 1×", 2.1, "t", "middle", weight=700)
    # G Türstufe – rechts oben neben Giebel hinten
    gx, gy = ax2 + W / 2 + 17, y1 + 0.5 + GH
    rechteck_teil(bl, gx, gy, GB, GH, "G", "", dl=False)
    bl.dim((gx + GB, gy), (gx + GB, gy - GH), 2.5)
    bl.text(gx + GB, y1 + 17.5, "G · TÜRSTUFE · 1×", 2.1, "t", "end", weight=700)

    # ---------- Reihe 2: Dach, Seitenwand, Schornstein
    y2 = oy1 + 13
    oy2 = y2 + SC
    cx_ = 23
    dach(bl, cx_, oy2)
    bx_ = cx_ + LC + 13
    seitenwand(bl, bx_, oy2 - (SC - HE))
    dx_ = bx_ + LB + 13
    schornstein(bl, dx_, oy2 - (SC - SL) + 2)
    bl.text(dx_ + SB / 2, oy2 - (SC - SL) + 5.5, "SCHORNSTEIN", 1.9, "t", "middle", weight=700)
    bl.text(dx_ + SB / 2, oy2 - (SC - SL) + 8.3, "2 Teile deckungsgl.", 1.6, "ts", "middle")
    bl.text(dx_ + SB / 2, oy2 - (SC - SL) + 10.6, "zusammenkleben", 1.6, "ts", "middle")

    # ---------- Reihe 3: Explosion | Montage + Schriftfeld
    y3 = oy2 + 11
    bl.line((14, y3 - 2.5), (196, y3 - 2.5), "sep")
    bl.text(15, y3 + 3.5, "EXPLOSIONSZEICHNUNG", 3.0, "t", weight=700)
    bl.text(15, y3 + 7.3, "ISOMETRIE", 2.0, "ts")
    # M 1:2 Plakette
    bl.add(f'<rect class="box2" x="57" y="{f(y3)}" width="20" height="8"/>')
    bl.text(67, y3 + 6.0, "M 1:3", 4.2, "t", "middle", weight=700)
    explosion(bl, 14, y3 + 10, 106, 283, 1 / 3)

    # Montage
    mx, my = 110, y3 + 1
    bl.text(mx, my + 2.5, "MONTAGE", 3.0, "t", weight=700)
    schritte = [
        ("1", ["Teig 4 mm ausrollen, Schablonen auf-",
               "legen, Teile ausschneiden, backen."]),
        ("2", ["Noch WARM an der Schablone gerade",
               "nachschneiden, dann auskühlen lassen."]),
        ("3", ["Wände: B steht ZWISCHEN den Giebeln A.",
               "Mit dickem Zuckerguss verbinden, stützen."]),
        ("4", ["Mind. 1 h trocknen lassen, dann Dach-",
               "platten C aufsetzen, First verfugen."]),
        ("5", ["Schornstein: beide D aufeinanderkleben,",
               "nach dem Trocknen aufs Dach setzen."]),
        ("6", ["Extras: Vordach E über die Tür, Läden F",
               "neben die Fenster, Stufe G vor die Tür."]),
    ]
    yy = my + 7.6
    for nr, zeilen in schritte:
        bl.add(f'<circle class="mk" cx="{f(mx + 1.9)}" cy="{f(yy - 0.8)}" r="1.9"/>')
        bl.text(mx + 1.9, yy, nr, 2.3, "t", "middle", weight=700)
        for i, z in enumerate(zeilen):
            bl.text(mx + 5.2, yy + i * 2.7, z, 2.0, "t")
        yy += 6.5
    bl.text(mx, yy + 0.6, "Legende:  ── Schnittlinie   - - - ausstechen", 1.8, "ts")
    bl.text(mx, yy + 3.2, "–·–·– Mittellinie   ‒ ‒ ▸ Montagerichtung", 1.8, "ts")

    # Schriftfeld unten rechts
    sw, sh = 86, 26
    sx0, sy0 = 198 - sw, 285 - sh
    bl.add(f'<rect class="tb" x="{sx0}" y="{sy0}" width="{sw}" height="{sh}"/>')
    rows = [sy0 + 11, sy0 + 18.5]
    for r in rows:
        bl.line((sx0, r), (sx0 + sw, r), "tbl")
    bl.line((sx0 + 43, rows[0]), (sx0 + 43, sy0 + sh), "tbl")
    bl.text(sx0 + 2.5, sy0 + 4.3, "BENENNUNG", 1.6, "ts")
    bl.text(sx0 + 2.5, sy0 + 9.4, "PLÄTZCHENHAUS NR. 1", 4.6, "t", weight=700)
    zellen = [
        (sx0 + 2.5, rows[0], "MASSSTAB", "1:1 (SCHABLONEN)"),
        (sx0 + 45.5, rows[0], "DATUM", DATUM),
        (sx0 + 2.5, rows[1], "ZEICHNER", "KAI"),
        (sx0 + 45.5, rows[1], "BLATT", "1/1"),
    ]
    for x, y, k, v in zellen:
        bl.text(x, y + 2.6, k, 1.5, "ts")
        bl.text(x, y + 6.1, v, 2.7, "t", weight=700)

    style = f"""
{font_css()}
text{{font-family:'Courier Prime','Courier New',monospace;}}
.t{{fill:{th['txt']};}}
.ts{{fill:{th['soft']};}}
.dimt{{fill:{th['dim']};}}
.cut{{fill:none;stroke:{th['line']};stroke-width:0.5;stroke-linejoin:miter;}}
.hole{{fill:none;stroke:{th['line']};stroke-width:0.35;stroke-dasharray:1.6 0.9;}}
.dimln{{fill:none;stroke:{th['dim']};stroke-width:0.2;}}
.arr{{fill:{th['dim']};stroke:none;}}
.ctr{{fill:none;stroke:{th['soft']};stroke-width:0.2;stroke-dasharray:5 1 0.8 1;}}
.mk{{fill:{th['bg']};stroke:{th['line']};stroke-width:0.3;}}
.mkiso{{fill:{th['bg']};stroke:{th['line']};stroke-width:0.25;}}
.frame1{{fill:none;stroke:{th['line']};stroke-width:0.7;}}
.frame2{{fill:none;stroke:{th['line']};stroke-width:0.25;}}
.box{{fill:{th['boxbg']};stroke:{th['line']};stroke-width:0.5;}}
.box2{{fill:{th['boxbg']};stroke:{th['line']};stroke-width:0.5;}}
.tb{{fill:{th['boxbg']};stroke:{th['line']};stroke-width:0.5;}}
.tbl{{stroke:{th['line']};stroke-width:0.25;}}
.sep{{stroke:{th['soft']};stroke-width:0.2;stroke-dasharray:3 1.5;}}
.isobg{{fill:{th['bg']};stroke:none;}}
.isof{{fill:{th['face']};stroke:{th['line']};stroke-width:0.25;stroke-linejoin:round;}}
.isohole{{fill:{th['hole']};stroke:{th['line']};stroke-width:0.2;}}
.mont{{fill:none;stroke:{th['dim']};stroke-width:0.2;stroke-dasharray:1.2 0.8;}}
"""
    svg = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297">\n'
           f'<title>Plätzchenhaus Nr. 1 – Blaupause ({thema})</title>\n'
           f'<style>{style}</style>\n' + "\n".join(bl.o) + "\n</svg>\n")
    return svg


if __name__ == "__main__":
    print(f"W={W} D={D} HE={HE} HG={HG} LB={LB} LC={LC} SC={SC} H={H_GES:.1f}")
    print(f"Tür {TB}x{TH}  rund Ø{RD}  Fenster {FB}x{FH}  Schornstein {SB}x{SH}/{SL}  "
          f"E {EB}x{EH}  F {LFB}x{LFH}  G {GB}x{GH}")
    for thema, name in (("blaupause", "plaetzchenhaus-blaupause.svg"), ("druck", "plaetzchenhaus-druck.svg")):
        with open(os.path.join(HIER, name), "w", encoding="utf-8") as fh:
            fh.write(erzeuge(thema))
        print("geschrieben:", name)
