# Precompute Sun (unit) and Earth (km) vectors in the Moon principal-axis frame, JPL DE421
import numpy as np, base64, json, de421
from jplephem.ephem import Ephemeris
e = Ephemeris(de421); EMRAT = 81.30056
def Rz(t): c, s = np.cos(t), np.sin(t); return np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]])
def Rx(t): c, s = np.cos(t), np.sin(t); return np.array([[1, 0, 0], [0, c, s], [0, -s, c]])
JD0 = 2461406.5            # 2027-01-01 00:00 TDB
STEP_H = 2
N = int(2*365.25*24/STEP_H)
out = np.zeros((N, 6), np.float32)
for i in range(N):
    jd = JD0 + i*STEP_H/24
    emb = e.position('earthmoon', jd)[:, 0]; mg = e.position('moon', jd)[:, 0]
    earth = emb - mg/(1+EMRAT); moon = earth + mg; sun = e.position('sun', jd)[:, 0]
    phi, th, psi = e.compute('librations', jd)[:3, 0]
    M = Rz(psi) @ Rx(th) @ Rz(phi)
    s = M @ (sun - moon); s /= np.linalg.norm(s)
    out[i, :3] = s; out[i, 3:] = M @ (earth - moon)
b64 = base64.b64encode(out.tobytes()).decode()
open('/home/claude/nasa/eph.js', 'w').write(f'const EPH={{jd0:{JD0},stepH:{STEP_H},n:{N},b64:"{b64}"}};')
print(N, len(b64)/1e3, 'kB', out[0])
