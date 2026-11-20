"""Mass and submerged equilibrium from measured envelope and Fusion data."""

import json, math, pathlib, sys
import numpy as np

HERE = pathlib.Path(__file__).parent
G = 9.80665
rows = json.loads((HERE / 'geometria' / 'volumenes_y_centros_fusion_v12.json').read_text())
rod_count = int(sys.argv[2]) if len(sys.argv)>2 else 4
axial = float(sys.argv[3]) if len(sys.argv)>3 else 20.
mass_rows = []
volume_rows = []

def mass(group, kg, xyz, low=None, high=None):
    mass_rows.append((group, float(kg), list(xyz), kg if low is None else low, kg if high is None else high))

def displacement(liters, xyz):
    volume_rows.append((float(liters), list(xyz)))

# Actual inventory dimensions and cap drawing replace old CAD ID and machining.
tube_cm3 = math.pi*(90**2-86**2)*380/1000
cap_blank_cm3 = math.pi*115**2*10/1000
cap_fasteners_cm3 = 4*math.pi*4.5**2*10/1000
cap_groove_cm3 = math.pi*(90.6**2-85.4**2)*3.2/1000
mass('PMMA y tóricas',tube_cm3*1.19/1000,(190,0,0))
for x, ports in [(-5,0),(385,6)]:
    mass('PMMA y tóricas',(cap_blank_cm3-cap_fasteners_cm3-cap_groove_cm3-ports)*1.19/1000,(x,0,0))
mass('PMMA y tóricas',.030,(190,0,0),.022,.042)
displacement(math.pi*90**2*380/1e6,(190,0,0))
for x in (-5,385):
    displacement((cap_blank_cm3-cap_fasteners_cm3-cap_groove_cm3)/1000,(x,0,0))
for row in rows:
    path=row['path']
    group=path[1][:2]
    name=path[-1]
    v=row['cm3']
    xyz=row['xyz_mm']
    if group=='02' and (rod_count==4 or name[1] in '13'):
        factor=.85 if name.startswith('R') else 1
        kg=v*factor*.00798
        mass('Metal exterior',kg,xyz,kg*.9,kg*1.05)
        displacement(v*factor/1000,xyz)
    if group=='03':
        solid=name.startswith('M3_')
        fractions=(1,1,1) if solid else (.55,.74,.95)
        reference_density=.00798 if solid else .00107
        low,base,high=[v*reference_density*x for x in fractions]
        mass('Chasis y soportes impresos',base,xyz,low,high)
# Install two collars on each side of each ring, on two opposed sleeves.
# 25x14x8 mm is a volume envelope, with a modest deduction for the split.
for station in (40,335):
    for x in (station-axial/2-4.2,station+axial/2+4.2):
        for sign in (-1,1):
            v=math.pi*(12.5**2-7**2)*8/1000*.9
            xyz=(x,sign*71.418,sign*71.418)
            mass('Topes axiales estimados',v*.00798,xyz,v*.00798*.65,v*.00798*1.30)
            displacement(v/1000,xyz)
ring_cm3=float(sys.argv[1]) if len(sys.argv)>1 else 125.843839
for x in (40,335):
    kg=ring_cm3*.00127
    mass('Aros PETG',kg,(x,0,0),kg*.90,kg*1.08)
    displacement(ring_cm3/1000,(x,0,0))
# Pinpoint measured CAD coordinates, provisional component masses.
for group,kg,low,high,xyz in [
    ('Batería',.36,.25,.55,(283,-28,-12)),
    ('Bomba completa',.26,.18,.38,(269,32,-13)),
    ('Electrónica y cámaras',.055,.045,.065,(146,31,47)),
    ('Electrónica y cámaras',.17,.095,.29,(279,12,64)),
    ('Electrónica y cámaras',.075,.040,.12,(186,1,-3)),
    ('Electrónica y cámaras',.065,.035,.115,(49,0,8)),
    ('Electrónica y cámaras',.085,.055,.13,(278,-22,42)),
    ('Óptica, sensores, fluidos y cableado',.16,.09,.26,(230,0,-30)),
    ('Óptica, sensores, fluidos y cableado',.10,.055,.17,(190,0,0)),
    ('Óptica, sensores, fluidos y cableado',.04,.025,.065,(126,0,0)),
    ('Óptica, sensores, fluidos y cableado',.045,.025,.08,(391,0,15)),
]:
    mass(group,kg,xyz,low,high)
displacement(.025,(393,0,15))
m=sum(r[1] for r in mass_rows)
m_min=sum(r[3] for r in mass_rows)
m_max=sum(r[4] for r in mass_rows)
center=lambda masses,coords: np.average(np.asarray(coords),axis=0,weights=masses)
cg=center([r[1] for r in mass_rows],[r[2] for r in mass_rows])
v=sum(r[0] for r in volume_rows)
cb=center([r[0] for r in volume_rows],[r[1] for r in volume_rows])
res={'mass_kg':m,'mass_range_kg':[m_min,m_max],'displacement_l':v,'cg_mm':cg.tolist(),'cb_mm':cb.tolist(),'case':[]}
res['groups']={key:sum(row[1] for row in mass_rows if row[0]==key) for key in dict.fromkeys(row[0] for row in mass_rows)}
assert 4<m<8 and 10<v<12 and abs(cb[1])<1
# Select a half-kilo step allowing at least 0.5 kgf down at the low mass edge in seawater.
steel=7.85
stock=math.ceil((1.025*v-m_min+.5)/(1-1.025/steel)*2)/2
res['stock_kg']=stock
for rho,label in [(1.0,'dulce'),(1.025,'mar')]:
    neutral=(rho*v-m)/(1-rho/steel)
    target=(rho*v-m+.75)/(1-rho/steel)
    stock_use=math.ceil(target*2)/2
    apparent=stock_use*(1-rho/steel)
    tension=m+apparent-rho*v
    x_f,x_r=40,335
    x_t=(x_f+x_r)/2
    x_ball=(rho*v*cb[0]+tension*x_t-m*cg[0])/apparent
    x_ball=float(np.clip(x_ball,x_f,x_r))
    q=G/1000*(rho*v*cb+tension*np.array([x_t,0,103])-m*cg-apparent*np.array([x_ball,0,-103]))
    untrimmed=q+G/1000*apparent*np.array([x_ball-x_t,0,0])
    cases = []
    for deg in (5,10,15,20,30):
        rad=math.radians(deg)
        cases.append([deg,float(q[2]*math.sin(rad)),float(q[2]*math.cos(rad))])
    cases=list(cases)
    res['case'].append({'water':label,'rho_kg_l':rho,'neutral_kg':neutral,'target_kg':target,
                        'trial_kg':stock_use,'apparent_kg':apparent,'reserve_n':tension*G,
                        'reserve_with_stock_n':(m+stock*(1-rho/steel)-rho*v)*G,
                        'reserve_min_with_stock_n':(m_min+stock*(1-rho/steel)-rho*v)*G,
                        'ballast_rear_share':(x_ball-x_f)/(x_r-x_f),'ballast_x_mm':x_ball,
                        'roll_deg':math.degrees(math.atan2(q[1],q[2])),
                        'pitch_untrimmed_deg':math.degrees(math.atan2(untrimmed[0],untrimmed[2])),
                        'roll_stiffness_Nm_rad':float(q[2]),'righting_moments':cases,
                        'forces_n':{'weight':m*G,'buoyancy':rho*v*G,'lower':apparent*G,'upper':tension*G}})
assert all(r['reserve_n']>0 and r['roll_stiffness_Nm_rad']>0 for r in res['case'])
output = pathlib.Path(sys.argv[4]) if len(sys.argv)>4 else pathlib.Path(f'hidro_result_{rod_count}.json')
output.write_text(json.dumps(res,indent=2))
print(json.dumps(res,indent=2))
