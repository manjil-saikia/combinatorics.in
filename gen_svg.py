#!/usr/bin/env python3
"""Emit the static SVG graphics used by combinatorics.in into _includes/gfx/."""
import math, os, pathlib

OUT = pathlib.Path("/home/claude/site/_includes/gfx")
OUT.mkdir(parents=True, exist_ok=True)

def write(name, body):
    (OUT / name).write_text(body.strip() + "\n", encoding="utf-8")
    print("wrote", name)

# ---------------------------------------------------------------- hooks
# Young diagram of lambda = (5,4,2,1) with hook lengths; corner hook shaded.
def hooks():
    H = [[8, 6, 4, 3, 1], [6, 4, 2, 1], [3, 1], [1]]
    c = 30
    w, h = 5 * c + 2, 4 * c + 2
    s = [f'<svg viewBox="0 0 {w} {h}" width="{w}" xmlns="http://www.w3.org/2000/svg" '
         f'role="img" aria-label="Young diagram of the partition 5,4,2,1 with hook lengths written in each cell.">']
    for i, row in enumerate(H):
        for j, hk in enumerate(row):
            hot = (i == 0) or (j == 0)
            fill = "var(--facet-top)" if hot else "var(--surface-2)"
            tf = "var(--on-amber)" if hot else "var(--muted)"
            s.append(f'<rect x="{j*c+1}" y="{i*c+1}" width="{c}" height="{c}" '
                     f'fill="{fill}" stroke="var(--line)" stroke-width="1"/>')
            s.append(f'<text class="lbl" x="{j*c+1+c//2}" y="{i*c+1+c//2+5}" '
                     f'text-anchor="middle" font-size="13" fill="{tf}">{hk}</text>')
    s.append('</svg>')
    return "\n".join(s)

# ---------------------------------------------------- Young's lattice
def younglattice():
    c = 7
    nodes = [([], 260, 326), ([1], 260, 256),
             ([2], 198, 186), ([1, 1], 322, 186),
             ([3], 140, 112), ([2, 1], 260, 112), ([1, 1, 1], 380, 112),
             ([4], 76, 32), ([3, 1], 176, 32), ([2, 2], 260, 32),
             ([2, 1, 1], 344, 32), ([1, 1, 1, 1], 446, 32)]
    edges = [(0, 1), (1, 2), (1, 3), (2, 4), (2, 5), (3, 5), (3, 6),
             (4, 7), (4, 8), (5, 8), (5, 9), (5, 10), (6, 10), (6, 11)]
    s = ['<svg viewBox="0 0 520 350" width="520" xmlns="http://www.w3.org/2000/svg" '
         'role="img" aria-label="Young\'s lattice: partitions of 0 through 4 joined by covering relations.">']
    for a, b in edges:
        s.append(f'<line x1="{nodes[a][1]}" y1="{nodes[a][2]}" x2="{nodes[b][1]}" '
                 f'y2="{nodes[b][2]}" stroke="var(--line)" stroke-width="1.2"/>')
    for lam, x, y in nodes:
        if not lam:
            s.append(f'<circle cx="{x}" cy="{y}" r="4" fill="var(--muted)"/>')
            s.append(f'<text class="lbl" x="{x+13}" y="{y+4}" font-size="10" '
                     f'fill="var(--muted)">&#8709;</text>')
            continue
        w, h = lam[0] * c, len(lam) * c
        ox, oy = x - w / 2, y - h / 2
        for i, ln in enumerate(lam):
            for j in range(ln):
                s.append(f'<rect x="{ox+j*c:g}" y="{oy+i*c:g}" width="{c}" height="{c}" '
                         f'fill="var(--facet-left)" stroke="var(--ground)" stroke-width="1"/>')
    s.append('</svg>')
    return "\n".join(s)

# ------------------------------------------------------- q-binomial
def qbinom():
    c, W, H = 32, 5, 3
    X = lambda x: 2 + x * c
    Y = lambda y: 2 + (H - y) * c
    rows = [5, 3, 2]                      # shaded cells, top row first
    s = [f'<svg viewBox="0 0 {W*c+4} {H*c+4}" width="{W*c+4}" xmlns="http://www.w3.org/2000/svg" '
         f'role="img" aria-label="A monotone lattice path in a 3 by 5 box, cutting out the partition 5,3,2.">']
    for i, ln in enumerate(rows):
        for j in range(ln):
            s.append(f'<rect x="{X(j)}" y="{2+i*c}" width="{c}" height="{c}" '
                     f'fill="var(--facet-top)" opacity="0.55"/>')
    for x in range(W + 1):
        s.append(f'<line x1="{X(x)}" y1="{Y(0)}" x2="{X(x)}" y2="{Y(H)}" stroke="var(--line)" stroke-width="1"/>')
    for y in range(H + 1):
        s.append(f'<line x1="{X(0)}" y1="{Y(y)}" x2="{X(W)}" y2="{Y(y)}" stroke="var(--line)" stroke-width="1"/>')
    path = [(0, 0), (2, 0), (2, 1), (3, 1), (3, 2), (5, 2), (5, 3)]
    pts = " ".join(f"{X(a)},{Y(b)}" for a, b in path)
    s.append(f'<polyline points="{pts}" fill="none" stroke="var(--accent)" stroke-width="3" '
             f'stroke-linejoin="round" stroke-linecap="round"/>')
    s.append(f'<circle cx="{X(0)}" cy="{Y(0)}" r="4" fill="var(--accent)"/>')
    s.append(f'<circle cx="{X(5)}" cy="{Y(3)}" r="4" fill="var(--accent)"/>')
    s.append('</svg>')
    return "\n".join(s)

# ---------------------------------------------------------- Catalan
def catalan():
    s = ['<svg viewBox="0 0 560 175" width="560" xmlns="http://www.w3.org/2000/svg" '
         'role="img" aria-label="Three families counted by the fourth Catalan number: a Dyck path, a triangulated hexagon, and a binary tree.">']
    # Dyck path
    c, ox, oy = 18, 14, 104
    x = y = 0
    pts = [(0, 0)]
    for ch in "UUDUDDUD":
        x += 1
        y += 1 if ch == "U" else -1
        pts.append((x, y))
    s.append(f'<line x1="{ox}" y1="{oy}" x2="{ox+8*c}" y2="{oy}" stroke="var(--line)" stroke-width="1.2"/>')
    pp = " ".join(f"{ox+a*c},{oy-b*c}" for a, b in pts)
    s.append(f'<polyline points="{pp}" fill="none" stroke="var(--facet-left)" stroke-width="3" '
             f'stroke-linejoin="round" stroke-linecap="round"/>')
    for a, b in pts:
        s.append(f'<circle cx="{ox+a*c}" cy="{oy-b*c}" r="2.6" fill="var(--facet-left)"/>')
    s.append(f'<text class="lbl" x="{ox+4*c}" y="140" text-anchor="middle" font-size="11" fill="var(--muted)">Dyck path</text>')
    # triangulated hexagon
    cx, cy, R = 290, 68, 54
    V = [(cx + R * math.cos(math.radians(-90 + k * 60)),
          cy + R * math.sin(math.radians(-90 + k * 60))) for k in range(6)]
    poly = " ".join(f"{a:.1f},{b:.1f}" for a, b in V)
    s.append(f'<polygon points="{poly}" fill="var(--facet-right)" opacity="0.28" '
             f'stroke="var(--facet-right)" stroke-width="2.4"/>')
    for a, b in [(0, 2), (2, 4), (4, 0)]:
        s.append(f'<line x1="{V[a][0]:.1f}" y1="{V[a][1]:.1f}" x2="{V[b][0]:.1f}" '
                 f'y2="{V[b][1]:.1f}" stroke="var(--accent)" stroke-width="2.4"/>')
    for a, b in V:
        s.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="3.4" fill="var(--facet-left)"/>')
    s.append(f'<text class="lbl" x="{cx}" y="140" text-anchor="middle" font-size="11" fill="var(--muted)">Triangulation</text>')
    # binary tree
    T = [(470, 22), (440, 58), (500, 58), (416, 94), (464, 94), (440, 124), (488, 124)]
    for a, b in [(0, 1), (0, 2), (1, 3), (1, 4), (4, 5), (4, 6)]:
        s.append(f'<line x1="{T[a][0]}" y1="{T[a][1]}" x2="{T[b][0]}" y2="{T[b][1]}" '
                 f'stroke="var(--line)" stroke-width="2"/>')
    for i, (a, b) in enumerate(T):
        leaf = i in (2, 3, 5, 6)
        s.append(f'<circle cx="{a}" cy="{b}" r="{4 if leaf else 6}" '
                 f'fill="{"var(--facet-right)" if leaf else "var(--facet-top)"}" '
                 f'stroke="var(--facet-left)" stroke-width="1.6"/>')
    s.append('<text class="lbl" x="470" y="152" text-anchor="middle" font-size="11" fill="var(--muted)">Binary tree</text>')
    s.append('</svg>')
    return "\n".join(s)

# ------------------------------------------------------ permutation
def permplot():
    c, n = 26, 6
    sig = [3, 5, 1, 4, 2, 6]
    hit = [0, 1, 2]
    X = lambda i: 2 + (i + 0.5) * c
    Y = lambda v: 2 + (n - v + 0.5) * c
    s = [f'<svg viewBox="0 0 {n*c+4} {n*c+4}" width="{n*c+4}" xmlns="http://www.w3.org/2000/svg" '
         f'role="img" aria-label="Plot of the permutation 351426 with an occurrence of the pattern 231 highlighted.">']
    for k in range(n + 1):
        s.append(f'<line x1="{2+k*c}" y1="2" x2="{2+k*c}" y2="{2+n*c}" stroke="var(--line)" stroke-width="1"/>')
        s.append(f'<line x1="2" y1="{2+k*c}" x2="{2+n*c}" y2="{2+k*c}" stroke="var(--line)" stroke-width="1"/>')
    pp = " ".join(f"{X(i):g},{Y(sig[i]):g}" for i in hit)
    s.append(f'<polyline points="{pp}" fill="none" stroke="var(--accent)" stroke-width="2" opacity="0.55"/>')
    for i, v in enumerate(sig):
        on = i in hit
        s.append(f'<circle cx="{X(i):g}" cy="{Y(v):g}" r="{7 if on else 5}" '
                 f'fill="{"var(--facet-top)" if on else "var(--facet-left)"}" '
                 f'stroke="{"var(--accent)" if on else "none"}" stroke-width="2"/>')
    s.append('</svg>')
    return "\n".join(s)

# ------------------------------------------------------- course chain
def chain():
    def box(x, label, sub, dim=False):
        return (f'<rect x="{x}" y="30" width="150" height="52" rx="4" fill="var(--surface-2)" '
                f'stroke="{"var(--line)" if dim else "var(--accent)"}" stroke-width="{1 if dim else 1.8}"/>'
                f'<text class="lbl" x="{x+75}" y="52" text-anchor="middle" font-size="11" fill="var(--muted)">{label}</text>'
                f'<text x="{x+75}" y="69" text-anchor="middle" font-size="13" fill="var(--text)">{sub}</text>')
    def arrow(x):
        return (f'<path d="M{x} 56 L{x+34} 56" stroke="var(--facet-right)" stroke-width="2"/>'
                f'<path d="M{x+34} 56 l-7 -4.5 v9 z" fill="var(--facet-right)"/>')
    return ('<svg viewBox="0 0 560 110" width="560" xmlns="http://www.w3.org/2000/svg" '
            'role="img" aria-label="MAT 315 or 515 leads to MAT 631, which leads to MAT 730.">'
            + box(6, "MAT 315 / 515", "Enumeration", True) + arrow(160)
            + box(204, "MAT 631", "Algebraic Comb.") + arrow(358)
            + box(402, "MAT 730", "Comb. Rep. Theory") + '</svg>')

# ---------------------------------- static first frame of the hero
def tiling():
    N = C = 5
    S = 22.0
    OX, OY = 110.0, 126.0
    U = (math.sqrt(3) / 2 * S, S / 2)
    V = (-math.sqrt(3) / 2 * S, S / 2)
    W = (0.0, -S)
    def P(a, b, c):
        return (OX + a * V[0] + b * U[0] + c * W[0],
                OY + a * V[1] + b * U[1] + c * W[1])
    h = [[max(0, C - i - j) for j in range(N)] for i in range(N)]
    out = ['<svg id="tiling" viewBox="0 0 220 250" xmlns="http://www.w3.org/2000/svg" '
           'role="img" aria-label="A plane partition drawn as a stack of cubes in a five by five by five box.">']
    def quad(pts, fill):
        p = " ".join(f"{a:.2f},{b:.2f}" for a, b in pts)
        out.append(f'<polygon points="{p}" fill="{fill}" stroke="var(--ground)" '
                   f'stroke-width="0.7" stroke-linejoin="round"/>')
    quad([P(0,0,0), P(0,N,0), P(N,N,0), P(N,0,0)], "var(--box-floor)")
    quad([P(0,0,0), P(N,0,0), P(N,0,C), P(0,0,C)], "var(--box-right)")
    quad([P(0,0,0), P(0,N,0), P(0,N,C), P(0,0,C)], "var(--box-left)")
    cells = sorted(((i, j) for i in range(N) for j in range(N)), key=lambda t: t[0] + t[1])
    for i, j in cells:
        k = h[i][j]
        if k == 0:
            continue
        A, B, Cc, D = P(i,j,k), P(i,j+1,k), P(i+1,j+1,k), P(i+1,j,k)
        drop = k * S
        quad([D, Cc, (Cc[0], Cc[1]+drop), (D[0], D[1]+drop)], "var(--facet-left)")
        quad([B, Cc, (Cc[0], Cc[1]+drop), (B[0], B[1]+drop)], "var(--facet-right)")
        quad([A, B, Cc, D], "var(--facet-top)")
    out.append('</svg>')
    return "\n".join(out)

write("hooks.svg", hooks())
write("younglattice.svg", younglattice())
write("qbinom.svg", qbinom())
write("catalan.svg", catalan())
write("permplot.svg", permplot())
write("chain.svg", chain())
write("tiling.svg", tiling())
