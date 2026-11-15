# Blender (bpy) banner scene: lunar south pole, real DE421 Sun/Earth geometry
import bpy, numpy as np, json, sys, math
from scipy.ndimage import map_coordinates
RES = int(sys.argv[1]) if len(sys.argv) > 1 else 640
SAMPLES = int(sys.argv[2]) if len(sys.argv) > 2 else 16
OUT = sys.argv[3] if len(sys.argv) > 3 else '/home/claude/nasa/test.png'
T = json.load(open('/home/claude/nasa/tracks.json')); A = np.array(T['rows'])
I = 1046                                    # 2027-09-19 12:00 UTC
SUN_ALT, SUN_AZ, E_ALT, E_AZ = A[I]
R_MOON = 1737.4
rng = np.random.default_rng(7)

def dirv(az, alt):
    az, alt = np.radians(az), np.radians(alt)
    return np.array([np.sin(az)*np.cos(alt), np.cos(az)*np.cos(alt), np.sin(alt)])

# ---------- terrain heightfield (km) ----------
def noise(x, y, scale, amp, seed):
    g = np.random.default_rng(seed).standard_normal((260, 260))
    u = x/scale + 130; v = y/scale + 130
    return amp*map_coordinates(g, [u, v], order=3, mode='grid-wrap')

def crater(x, y, cx, cy, R, D, rim):
    r = np.hypot(x-cx, y-cy)/R
    inside = rim + D*(r**2 - 1)
    outside = rim*np.exp(-((r-1)/0.35)**2)
    return np.where(r < 1, np.minimum(inside, rim), outside)

SHK = dirv(75, 0)[:2]*10.6                    # Shackleton centre, ~12 km from site
craters = [(*(rng.uniform(-110, 110, 2)), R) for R in (rng.pareto(1.6, 260)+1)*0.25]
def height(x, y):
    h = sum(noise(x, y, s, a, k) for k, (s, a) in enumerate([(6, .35), (2.5, .15), (.9, .05), (.3, .015), (.1, .005)]))
    h += crater(x, y, *SHK, 10.5, 4.2, 0.35)
    for cx, cy, R in craters:
        if R < 6: h += crater(x, y, cx, cy, R, 0.2*R, 0.04*R)
    # distant massifs on the polar horizon (Malapert / Leibnitz-like)
    for az, d, H, w in [(45, 75, 3.0, 12), (150, 90, 3.4, 14), (165, 70, 2.4, 12), (20, 80, 2.8, 16)]:
        mx, my = dirv(az, 0)[:2]*d
        h += H*np.exp(-((x-mx)**2+(y-my)**2)/(2*w**2)) * (1+noise(x, y, 4, .25, 99))
    return h - (x**2+y**2)/(2*R_MOON)          # lunar curvature

# polar mesh around the camera, log-spaced in range
nr, nt = 340, 420
r = np.geomspace(0.01, 140, nr); t = np.radians(np.linspace(5, 195, nt))
RR, TT = np.meshgrid(r, t, indexing='ij')
X, Y = RR*np.sin(TT), RR*np.cos(TT)
Z = height(X, Y)
cam_z = float(height(np.array([0.0]), np.array([0.0]))[0]) + 0.45

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
verts = np.c_[X.ravel(), Y.ravel(), Z.ravel()]
idx = np.arange(nr*nt).reshape(nr, nt)
faces = np.c_[idx[:-1, :-1].ravel(), idx[1:, :-1].ravel(), idx[1:, 1:].ravel(), idx[:-1, 1:].ravel()]
me = bpy.data.meshes.new('terrain'); me.from_pydata(verts.tolist(), [], faces.tolist()); me.update()
me.shade_smooth()
ter = bpy.data.objects.new('LunarTerrain', me); sc.collection.objects.link(ter)
m = bpy.data.materials.new('regolith'); m.use_nodes = True; nt_ = m.node_tree
b = nt_.nodes['Principled BSDF']; b.inputs['Base Color'].default_value = (0.16, 0.155, 0.15, 1); b.inputs['Roughness'].default_value = 1
nz = nt_.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 900; nz.inputs['Detail'].default_value = 8
bm = nt_.nodes.new('ShaderNodeBump'); bm.inputs['Strength'].default_value = 0.4
nt_.links.new(nz.outputs['Fac'], bm.inputs['Height']); nt_.links.new(bm.outputs['Normal'], b.inputs['Normal'])
ter.data.materials.append(m)

def emit_mat(name, col, strength):
    mm = bpy.data.materials.new(name); mm.use_nodes = True; n = mm.node_tree.nodes
    n.remove(n['Principled BSDF']); e = n.new('ShaderNodeEmission')
    e.inputs['Color'].default_value = (*col, 1); e.inputs['Strength'].default_value = strength
    mm.node_tree.links.new(e.outputs[0], n['Material Output'].inputs[0]); return mm

CAM = np.array([0, 0, cam_z])
# ---------- Sun lamp + disc ----------
sd = dirv(SUN_AZ, SUN_ALT)
ld = bpy.data.lights.new('Sun', 'SUN'); ld.energy = 25; ld.angle = math.radians(0.53); ld.color = (1, .97, .92)
lo = bpy.data.objects.new('Sun', ld); sc.collection.objects.link(lo)
lo.rotation_mode = 'QUATERNION'
from mathutils import Vector
lo.rotation_quaternion = Vector(-sd).to_track_quat('-Z', 'Y')
D = 190
bpy.ops.mesh.primitive_uv_sphere_add(radius=D*math.tan(math.radians(0.265)), location=CAM+sd*D)
s = bpy.context.object; s.name = 'SunDisc'; s.data.materials.append(emit_mat('sun', (1, .95, .85), 400))
s.visible_shadow = False
# earthshine fill (real: Earth lights the shadowed crater faintly)
ld2 = bpy.data.lights.new('Earthshine', 'SUN'); ld2.energy = 0.35; ld2.color = (.55, .7, 1); ld2.angle = math.radians(2)
lo2 = bpy.data.objects.new('Earthshine', ld2); sc.collection.objects.link(lo2); lo2.rotation_mode = 'QUATERNION'
lo2.rotation_quaternion = Vector(-dirv(E_AZ, E_ALT)).to_track_quat('-Z', 'Y')
# ---------- Earth ----------
ed = dirv(E_AZ, E_ALT)
bpy.ops.mesh.primitive_uv_sphere_add(radius=D*math.tan(math.radians(0.95)), location=CAM+ed*D, segments=96, ring_count=48)
eo = bpy.context.object; eo.name = 'Earth'; eo.rotation_euler = (0.4, 0.2, 1.2)
em = bpy.data.materials.new('earth'); em.use_nodes = True; n = em.node_tree.nodes; L = em.node_tree.links
pb = n['Principled BSDF']; pb.inputs['Roughness'].default_value = .6
tn = n.new('ShaderNodeTexNoise'); tn.inputs['Scale'].default_value = 3; tn.inputs['Detail'].default_value = 10
cr = n.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].color = (.01, .06, .25, 1); cr.color_ramp.elements[1].color = (.15, .35, .12, 1)
cr.color_ramp.elements[0].position = .52; cr.color_ramp.elements[1].position = .56
cl = n.new('ShaderNodeTexNoise'); cl.inputs['Scale'].default_value = 7; cl.inputs['Detail'].default_value = 12
cr2 = n.new('ShaderNodeValToRGB'); cr2.color_ramp.elements[0].position = .5; cr2.color_ramp.elements[1].position = .68
mx = n.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.inputs['B'].default_value = (1, 1, 1, 1)
L.new(tn.outputs['Fac'], cr.inputs[0]); L.new(cl.outputs['Fac'], cr2.inputs[0])
L.new(cr2.outputs['Color'], mx.inputs['Factor']); L.new(cr.outputs['Color'], mx.inputs['A']); L.new(mx.outputs['Result'], pb.inputs['Base Color'])
eo.data.materials.append(em); bpy.ops.object.shade_smooth()
eo.visible_shadow = False
# atmosphere rim
bpy.ops.mesh.primitive_uv_sphere_add(radius=eo.dimensions.x/2*1.03, location=eo.location, segments=96, ring_count=48)
at = bpy.context.object; at.visible_shadow = False
am = bpy.data.materials.new('atmo'); am.use_nodes = True; n = am.node_tree.nodes; L = am.node_tree.links
n.remove(n['Principled BSDF']); fr = n.new('ShaderNodeLayerWeight'); fr.inputs['Blend'].default_value = .25
ee = n.new('ShaderNodeEmission'); ee.inputs['Color'].default_value = (.25, .55, 1, 1); ee.inputs['Strength'].default_value = 3
tr = n.new('ShaderNodeBsdfTransparent'); mix = n.new('ShaderNodeMixShader')
L.new(fr.outputs['Facing'], mix.inputs[0]); L.new(tr.outputs[0], mix.inputs[1]); L.new(ee.outputs[0], mix.inputs[2])
L.new(mix.outputs[0], n['Material Output'].inputs[0]); at.data.materials.append(am)

# ---------- real Sun & Earth paths (one lunar month around the date) ----------
def path_curve(name, rows, col, strength, radius, bevel):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = bevel
    sp = cu.splines.new('POLY'); sp.points.add(len(rows)-1)
    for p, (az, alt) in zip(sp.points, rows):
        v = CAM + dirv(az, alt)*radius; p.co = (*v, 1)
    o = bpy.data.objects.new(name, cu); sc.collection.objects.link(o)
    o.data.materials.append(emit_mat(name+'_m', col, strength)); o.visible_shadow = False; return o
w = slice(I-60, I+60)                       # ±15 days, 6-hour steps
path_curve('SunPath', A[w][:, [1, 0]], (1, .7, .2), 25, 180, .12)
path_curve('EarthPath', A[I-60:I+60][:, [3, 2]], (.2, .6, 1), 25, 182, .1)
# tick marks every 24 h on the sun path
for k in range(I-60, I+61, 4):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=.35, location=CAM+dirv(A[k, 1], A[k, 0])*180)
    o = bpy.context.object; o.data.materials.append(emit_mat('tick', (1, .8, .4), 40)); o.visible_shadow = False

# ---------- small lander on the ridge ----------
lp = dirv(112, 0)[:2]*0.045
lz = float(height(np.array([lp[0]]), np.array([lp[1]]))[0])
bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=.0016, depth=.0022, location=(lp[0], lp[1], lz+.0021))
body = bpy.context.object
gm = bpy.data.materials.new('foil'); gm.use_nodes = True
g = gm.node_tree.nodes['Principled BSDF']; g.inputs['Base Color'].default_value = (.85, .62, .2, 1); g.inputs['Metallic'].default_value = 1; g.inputs['Roughness'].default_value = .35
body.data.materials.append(gm)
for k in range(4):
    a = k*math.pi/2+.4; fx, fy = lp[0]+.0024*math.cos(a), lp[1]+.0024*math.sin(a)
    bpy.ops.mesh.primitive_cylinder_add(radius=.00012, depth=.0026, location=((fx+lp[0])/2, (fy+lp[1])/2, lz+.0011))
    leg = bpy.context.object; leg.rotation_euler = (math.atan2(fy-lp[1], 0) * 0, 0, 0)
    leg.data.materials.append(gm)
bpy.ops.mesh.primitive_cube_add(location=(lp[0], lp[1], lz+.0042))
pnl = bpy.context.object; pnl.scale = (.0025, .00004, .0012)
pnl.rotation_euler = (0, 0, -math.radians(SUN_AZ))
pm = bpy.data.materials.new('panel'); pm.use_nodes = True
q = pm.node_tree.nodes['Principled BSDF']; q.inputs['Base Color'].default_value = (.02, .04, .12, 1); q.inputs['Metallic'].default_value = .6; q.inputs['Roughness'].default_value = .2
pnl.data.materials.append(pm)

# ---------- world: black sky + stars ----------
wd = bpy.data.worlds.new('space'); sc.world = wd; wd.use_nodes = True
n = wd.node_tree.nodes; L = wd.node_tree.links; bg = n['Background']
tc = n.new('ShaderNodeTexCoord'); vo = n.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = 260
vo.feature = 'F1'; rmp = n.new('ShaderNodeMapRange'); rmp.inputs['From Min'].default_value = 0; rmp.inputs['From Max'].default_value = .09
rmp.inputs['To Min'].default_value = 1; rmp.inputs['To Max'].default_value = 0
mul = n.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'
pw = n.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 6
L.new(tc.outputs['Generated'], vo.inputs['Vector']); L.new(vo.outputs['Distance'], rmp.inputs['Value'])
L.new(vo.outputs['Color'], pw.inputs[0]); L.new(rmp.outputs['Result'], mul.inputs[0]); L.new(pw.outputs[0], mul.inputs[1])
L.new(mul.outputs[0], bg.inputs['Strength']); bg.inputs['Color'].default_value = (1, 1, 1, 1)

# ---------- camera ----------
cd = bpy.data.cameras.new('Cam'); cd.lens = 18; cd.sensor_width = 36; cd.clip_start = .0005; cd.clip_end = 600
co = bpy.data.objects.new('Cam', cd); sc.collection.objects.link(co); sc.camera = co
co.location = CAM; co.rotation_euler = (math.radians(90-5), 0, -math.radians(100))

# ---------- render ----------
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True; sc.cycles.max_bounces = 3
sc.render.resolution_x = RES; sc.render.resolution_y = int(RES*9/16)
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Punchy'; sc.view_settings.exposure = 1.3
sc.render.filepath = OUT
# glow
sc.use_nodes = True if hasattr(sc, 'use_nodes') else None
try:
    tree = bpy.data.node_groups.new('comp', 'CompositorNodeTree'); sc.compositing_node_group = tree
    rl = tree.nodes.new('CompositorNodeRLayers'); gl = tree.nodes.new('CompositorNodeGlare')
    out = tree.nodes.new('NodeGroupOutput'); tree.interface.new_socket('Image', in_out='OUTPUT', socket_type='NodeSocketColor')
    gl.inputs['Type'].default_value = 'Fog Glow' if 'Type' in gl.inputs else None
    tree.links.new(rl.outputs['Image'], gl.inputs['Image']); tree.links.new(gl.outputs['Image'], out.inputs[0])
except Exception as ex:
    print('compositor skipped:', ex)
bpy.ops.wm.save_as_mainfile(filepath='/home/claude/nasa/lunar_banner.blend')
bpy.ops.render.render(write_still=True)
print('SUN', SUN_AZ, SUN_ALT, 'EARTH', E_AZ, E_ALT, 'camz', cam_z)
