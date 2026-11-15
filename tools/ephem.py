# Real Sun/Earth alt-az at a lunar south-pole site from JPL DE421 (positions + lunar librations)
import numpy as np, json, de421
from jplephem.ephem import Ephemeris
e = Ephemeris(de421)
EMRAT = 81.30056
R_MOON = 1737.4

def Rz(t): c, s = np.cos(t), np.sin(t); return np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]])
def Rx(t): c, s = np.cos(t), np.sin(t); return np.array([[1, 0, 0], [0, c, s], [0, -s, c]])

def altaz(lat, lon, jd):
    emb = e.position('earthmoon', jd)[:, 0]; mg = e.position('moon', jd)[:, 0]
    earth = emb - mg / (1 + EMRAT); moon = earth + mg; sun = e.position('sun', jd)[:, 0]
    phi, th, psi = e.compute('librations', jd)[:3, 0]
    M = Rz(psi) @ Rx(th) @ Rz(phi)               # ICRF -> Moon principal-axis frame
    la, lo = np.radians([lat, lon])
    up = np.array([np.cos(la)*np.cos(lo), np.cos(la)*np.sin(lo), np.sin(la)])
    east = np.cross([0, 0, 1], up); east /= np.linalg.norm(east); north = np.cross(up, east)
    out = []
    for b in (sun, earth):
        v = M @ (b - moon) - up*R_MOON; v /= np.linalg.norm(v)
        out += [np.degrees(np.arcsin(v@up)), np.degrees(np.arctan2(v@east, v@north)) % 360]
    return out

if __name__ == '__main__':
    lat, lon = -89.45, 222.7      # Shackleton–de Gerlache connecting ridge (approx.)
    jd0 = 2461406.5               # 2027-01-01
    jds = jd0 + np.arange(0, 365, 0.25)
    a = np.array([altaz(lat, lon, j) for j in jds])
    print('sun alt', a[:, 0].min().round(2), a[:, 0].max().round(2))
    print('earth alt', a[:, 2].min().round(2), a[:, 2].max().round(2))
    i = np.argmax(a[:, 0]); print('max sun at day', (jds[i]-jd0), a[i])
    json.dump({'site': [lat, lon], 'jd0': jd0, 'step': 0.25, 'rows': a.round(3).tolist()},
              open('/home/claude/nasa/tracks.json', 'w'))
