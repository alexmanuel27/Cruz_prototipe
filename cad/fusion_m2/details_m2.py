"""Fusion build fragment, executed by build_m2.py with its geometry helpers."""

# Closed wet cassette: the enclosure stays dry, including the sensor electronics.
add('H_EC_BODY','Conductivity flow chamber PMMA OD20 ID16; seal design HOLD',ring(171.6,328.4,20,16,0,-54),'06','glass','WET_INTERFACE_PROPOSAL',opacity=.45)
for code,x0,x1 in [('H_EC_FRONT',165,171),('H_EC_REAR',329,335)]:
    cap=box(((x0+x1)/2,0,-54),(6,30,22))
    if code=='H_EC_FRONT':
        cut(cap,cyl((168,0,-54),(172,0,-54),8))
        cut(cap,cyl((164,0,-54),(169,0,-54),1.5))
    else:
        cut(cap,cyl((328,0,-54),(332,0,-54),8))
        cut(cap,cyl((328,0,-54),(336,0,-54),5.1))
        cut(cap,cyl((335,9,-50),(329,5,-50),1.5))
    for y in (-12,12): cut(cap,cyl((x0-1,y,-54),(x1+1,y,-54),1.7))
    add(code,'Machined wet end block; dimensions and O rings HOLD',cap,'06','black','WET_INTERFACE_PROPOSAL')
for code,a,b in [('H_EC_SEAL_F',171,171.6),('H_EC_SEAL_R',328.4,329)]:
    add(code,'Flat wet chamber seal; material/compression HOLD',ring(a,b,20,16,0,-54),'06','silicone','WET_INTERFACE_PROPOSAL')
add('ENV_EC','Atlas K1 probe envelope; actual generation to verify',cyl((176,0,-54),(327,0,-54),6),'06','black','CATALOG_ENVELOPE_VARIANT_PENDING')
add('H_EC_OUT','EC outlet 3mm bore; side facing optical cell',ring(155,165,6,3,0,-54),'06','metal','WET_INTERFACE_PROPOSAL')
add('H_EC_IN','EC inlet 3mm bore; rear end block',ring(335,345,6,3,9,-50),'06','metal','WET_INTERFACE_PROPOSAL')
gland=ring(329,343,10,2.8,0,-54)
union(gland,ring(335,338,14,2.8,0,-54))
add('H_EC_GLAND','Wet gland for 2.6mm EC cable; model selection HOLD',gland,'06','black','WET_INTERFACE_PROPOSAL')
for y in (-12,12):
    add('H_EC_ROD_'+str(y),'M3 through rod for wet cassette end caps',cyl((161,y,-54),(339,y,-54),1.5),'06','metal','DESIGN_PROPOSAL')
    for x0,x1 in [(158.6,161),(339,341.4)]:
        add('H_EC_NUT_%s_%s'%(y,x0),'M3 nut; simplified outside envelope',ring(x0,x1,6.2,3,y,-54),'06','metal')

tee=box((321,12,-30),(18,14,20))
cut(tee,cyl((321,12,-41),(321,12,-19),2.5))
cut(tee,cyl((317,12,-30),(331,12,-30),4))
add('H_TEMP_TEE','Temperature flow tee POM; seal and fittings HOLD',tee,'06','black','WET_INTERFACE_PROPOSAL')
for code,z0,z1 in [('H_TEMP_IN',-20,-14),('H_TEMP_OUT',-46,-40)]:
    port=cyl((321,12,z0),(321,12,z1),3)
    cut(port,cyl((321,12,z0-1),(321,12,z1+1),1.5))
    add(code,'Temperature tee 3mm bore port',port,'06','metal','WET_INTERFACE_PROPOSAL')
add('ENV_TEMP','DS18B20 6x50 envelope; tip wet / cable dry',cyl((318,12,-30),(368,12,-30),3),'06','metal','REFERENCE_APPROX')
add('H_TEMP_GLAND','Compression gland around DS18B20 case; HOLD',ring(330,340,12,6.2,12,-30),'06','black','WET_INTERFACE_PROPOSAL')

# Separate conductivity electronics, on a removable lateral plate.
add('EL_EZO','Atlas isolated EZO carrier 56.2x32; 20mm height reserve',box((342,-54,10),(56.2,20,32)),'05','pcb','CATALOG_XY_HEIGHT_PROVISIONAL')
ec_plate=box((342,-66,10),(64,4,40))
for x in (316,368):
    for z in (-4,24): cut(ec_plate,cyl((x,-69,z),(x,-63,z),1.7))
for x in (316,368):
    union(ec_plate,box((x,-66,-24),(10,4,28)))
    cut(ec_plate,cyl((x,-70,-37),(x,-62,-37),1.7))
add('P_EZO','Removable EZO mount; through bolts and nuts',ec_plate,'03',printed=True)

# Main chassis is a deep U section, not a ladder of thin rails.
shell=ring(0,L,168,158)
cut(shell,box((L/2,0,52),(L+2,200,140)))
for x in (20,80,180,300,L-15):
    rib=box((x,0,-67),(6,150,12))
    intersect(rib,cyl((x-4,0,0),(x+4,0,0),84))
    if 150<x<340: cut(rib,cyl((x-4,0,-54),(x+4,0,-54),12))
    union(shell,rib)
# Bridges extend the cap centering rings onto the removable chassis, without cap holes.
for a,b in [(8,15),(L-8,L-3)]:
    for y in (-80,80): union(shell,cyl((a,y,0),(b,y,0),4))
# Broad cheeks and crossbeams support the electronics tray; all holes are through holes.
for x in (216,344):
    for y in (-74,74):
        cheek=box((x,y,8.5),(8,20,57))
        intersect(cheek,cyl((x-5,0,0),(x+5,0,0),84))
        union(shell,cheek)
    beam=box((x,0,37),(8,154,4))
    intersect(beam,cyl((x-5,0,0),(x+5,0,0),84))
    for y in (-28,28): cut(beam,cyl((x,y,34),(x,y,40),1.7))
    union(shell,beam)
# Four bolted bosses at the frame seam, with rectangular self-alignment keys.
split=p['frame']['split_x']
for y,z in [(-49,-35),(49,-35),(-20,-60),(20,-60)]:
    boss=box((split,y,z),(16,14,12))
    intersect(boss,cyl((split-9,0,0),(split+9,0,0),84))
    union(shell,boss)
    cut(shell,cyl((split-9,y,z),(split+9,y,z),2.2))
add('P_U_SOURCE','U chassis 5mm shell with transverse ribs; build source',shell,'03',status='CARRIER_SOURCE')

# Open clips hold silicone hoses; no hose needs to be threaded through a printed ring.
def hose_guide(code,center,axis,foot):
    x,y,z=center
    if axis=='X':
        clip=ring(x-4,x+4,11,5.8,y,z)
        cut(clip,box((x,y,z+5),(10,5.4,10)))
    else:
        clip=cyl((x,y,z-4),(x,y,z+4),5.5)
        cut(clip,cyl((x,y,z-5),(x,y,z+5),2.9))
        cut(clip,box((x+5,y,z),(10,5.4,10)))
    union(clip,box(*foot))
    # Tie slots retain the hose without compressing its lumen.
    cut(clip,box((x-2,y,z-4.5),(2,12,1.4)))
    add(code,'Open silicone hose guide; loose tie retention',clip,'03',printed=True)
hose_guide('P_GUIDE_RETURN',(185,-20,62),'X',((185,-20,47.5),(8,8,21)))
hose_guide('P_GUIDE_INTAKE',(321,12,5),'Z',((321,20,5),(12,8,8)))

# Merge fixed supports into the chassis, then split it into Prusa-sized sections.
fixed=['P_U_SOURCE','P01','P02','P_F1','P_F2','P_R11','P_R21','P_PI','P_BAT','P_PUMP','P_CAM','P_HOOD_LOWER']
carrier=tmp.copy(records[fixed[0]]['body'])
for code in fixed[1:]: union(carrier,tmp.copy(records[code]['body']))
# Provide nut access under PCB standoffs; no self tapping plastic joints.
for x in (53.5,111.5):
    for y in (-24.5,24.5): cut(carrier,cyl((x,y,-59),(x,y,-56.5),2.95))
for x in (216,344):
    for y in (-28,28): cut(carrier,cyl((x,y,34),(x,y,40),1.7))
front=tmp.copy(carrier); rear=tmp.copy(carrier)
intersect(front,box((split-250,0,0),(500,200,200)))
intersect(rear,box((split+250,0,0),(500,200,200)))
for y in (-39,39):
    union(front,box((split+2.5,y,-45),(5,10,6)))
    cut(rear,box((split+2.55,y,-45),(5.3,10.4,6.4)))
for code,name,body in [('P_CHASSIS_FRONT','Ribbed U chassis FRONT; M4 nut joint',front),('P_CHASSIS_REAR','Ribbed U chassis REAR; M4 nut joint',rear)]:
    add(code,name,body,'03',printed=True)
for code in fixed:
    records[code]['occurrence'].isLightBulbOn=False
    records[code]['component'].attributes.add('cruz_m2','merged_into','P_CHASSIS_FRONT / P_CHASSIS_REAR')
    for part in manifest:
        if part['code']==code: part['printed']=False; part['status']='MERGED_SOURCE_DO_NOT_EXPORT'
