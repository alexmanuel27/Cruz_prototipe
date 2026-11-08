"""Run with Fusion's script API in the saved Cross_M2_horizontal_design copy.

Sources and dimensions remain editable. BRep parts are generated from parameters.json;
this is not an associative model of purchased components or a pressure qualification.
"""
import adsk.core
import adsk.fusion
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GROUP = 'M2_GENERATED'


def run(_context: str):
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    assert app.activeDocument.name.startswith('Cross_M2_horizontal_design'), 'Open the working copy, never overwrite cross.'
    root = design.rootComponent
    p = json.load(open(os.path.join(HERE, 'parameters.json')))
    assert p['body']['od'] > p['body']['id'] > 0
    assert p['closure']['rod_count'] == 4
    assert p['closure']['rod_cut_length'] > p['body']['length'] + 2*p['closure']['cap_thickness']
    tmp = adsk.fusion.TemporaryBRepManager.get()
    I = adsk.core.Matrix3D.create
    P = lambda x, y, z: adsk.core.Point3D.create(x/10, y/10, z/10)
    V = adsk.core.Vector3D.create
    B = adsk.fusion.BooleanTypes
    original_optics = [(o, tmp.copy(o.bRepBodies.item(0))) for o in root.occurrences if o.component.name == 'sensor']
    original_camera = next(tmp.copy(o.bRepBodies.item(0)) for o in root.occurrences if o.component.name == 'camara')
    original_holder = tmp.copy(root.bRepBodies.item(0))
    for o in list(root.occurrences):
        if o.component.name == GROUP:
            assert o.attributes.itemByName('cruz_m2', 'generated'), 'Refusing to delete unmarked geometry.'
            o.deleteMe()
    for b in root.bRepBodies:
        b.isLightBulbOn = False
    for o in root.occurrences:
        o.isLightBulbOn = False
    top_occ = root.occurrences.addNewComponent(I())
    top_occ.component.name = GROUP
    top_occ.attributes.add('cruz_m2', 'generated', 'parameters.json + build_m2.py')
    top = top_occ.component
    groups = {}
    for name in ['01_ENCLOSURE', '02_TIE_RODS_AND_CLOSURE', '03_PRINTED_FRAME', '04_OPTICS_REFERENCES', '05_ELECTRONICS_REFERENCES', '06_HYDRAULICS', '07_BALLAST_SUPPORTS']:
        o = top.occurrences.addNewComponent(I())
        o.component.name = name
        groups[name[:2]] = o.component
    manifest = []
    records = {}

    def box(center, size):
        return tmp.createBox(adsk.core.OrientedBoundingBox3D.create(P(*center), V(1,0,0), V(0,1,0), size[0]/10, size[1]/10, size[2]/10))

    def cyl(start, end, radius):
        body = tmp.createCylinderOrCone(P(*start), radius/10, P(*end), radius/10)
        assert body, ('Cylinder failed', start, end, radius)
        return body

    def boolean(body, tool, operation):
        assert tmp.booleanOperation(body, tool, operation), 'Boolean failed'
        return body

    def cut(body, tool):
        return boolean(body, tool, B.DifferenceBooleanType)

    def union(body, tool):
        return boolean(body, tool, B.UnionBooleanType)

    def ring(x0, x1, od, id_, y=0, z=0):
        return cut(cyl((x0,y,z),(x1,y,z),od/2), cyl((x0-1,y,z),(x1+1,y,z),id_/2))

    def intersect(body, tool):
        return boolean(body, tool, B.IntersectionBooleanType)

    def color(name, rgb):
        a = design.appearances.itemByName(name)
        if not a:
            a = design.appearances.addByCopy(design.appearances.itemByName('ABS (White)'), name)
            prop = adsk.core.ColorProperty.cast(a.appearanceProperties.itemById('opaque_albedo'))
            prop.value = adsk.core.Color.create(*rgb,255)
        return a

    colors = {'print': color('M2 Teal printed ASA', (30,91,107)), 'black': color('M2 Optical black',(30,32,35)), 'battery': color('M2 Battery blue',(25,85,205)), 'pcb': color('M2 PCB green',(24,95,61)), 'silicone': color('M2 Silicone grey',(86,94,99)), 'orange': color('M2 White LED reference',(230,176,63)), 'blue': color('M2 Blue LED reference',(65,103,230)), 'glass': design.appearances.itemByName('Glass (Clear)'), 'metal': design.appearances.itemByName('Steel - Satin')}

    def add(code, name, body, group, finish='print', status='DESIGN_PROPOSAL', printed=False, opacity=1):
        assert body and body.volume > 1e-7, (code,'Empty body')
        o = groups[group].occurrences.addNewComponent(I())
        c = o.component
        c.name = code + ' ' + name
        base = c.features.baseFeatures.add()
        base.name = code + ' generated solid (edit source parameters)'
        assert base.startEdit()
        b = c.bRepBodies.add(body, base)
        b.name = c.name
        assert base.finishEdit()
        b = c.bRepBodies.item(0)
        b.appearance = colors[finish]
        b.opacity = opacity
        c.attributes.add('cruz_m2','status',status)
        bb = b.boundingBox
        dims = [10*(getattr(bb.maxPoint,k)-getattr(bb.minPoint,k)) for k in 'xyz']
        if printed:
            assert all(v <= limit + 0.1 for v,limit in zip(sorted(dims),sorted(p['print_bed']))), (code,'Exceeds print bed',dims)
        manifest.append({'code':code,'name':name,'group':group,'status':status,'printed':printed,'bbox_mm':[round(v,3) for v in dims],'volume_cm3':round(b.volume,4)})
        records[code] = {'body':b,'component':c,'occurrence':o,'temporary':body}
        return b

    L = p['body']['length']
    q = p['closure']
    g = q['gasket_free_thickness'] * (1-q['gasket_compression'])
    t = q['cap_thickness']
    r = q['rod_radius']
    centers = [(r*math.cos(math.radians(a)),r*math.sin(math.radians(a))) for a in (45,135,225,315)]
    cap_front = (-g-t, -g)
    cap_rear = (L+g, L+g+t)
    assert math.isclose((p['body']['od']-p['body']['id'])/2,5)
    assert min(math.hypot(y,z) for y,z in centers) - 7 > p['body']['od']/2
    for name,value in [('Tube_OD',p['body']['od']),('Tube_ID',p['body']['id']),('Tube_length',L),('Cap_diameter',q['cap_diameter']),('Cap_thickness',t),('Rod_PCD',2*r),('Gasket_working_thickness',g)]:
        parameter = design.userParameters.itemByName('M2_'+name)
        if parameter:
            parameter.expression = str(value)+' mm'
        else:
            design.userParameters.add('M2_'+name, adsk.core.ValueInput.createByString(str(value)+' mm'), 'mm', 'Reference; regenerate BRep geometry after changing parameters.json')

    add('E01','Acrylic tube OD180 ID170 L380 proposal',ring(0,L,p['body']['od'],p['body']['id']),'01','glass',opacity=0.18)
    for label,(a,b) in [('FRONT',cap_front),('REAR',cap_rear)]:
        cap = cyl((a,0,0),(b,0,0),q['cap_diameter']/2)
        for y,z in centers:
            cut(cap,cyl((a-1,y,z),(b+1,y,z),4.5))
        if label == 'REAR':
            for port in ['intake','discharge']:
                y,z = p['rear_ports'][port]
                cut(cap,cyl((a-1,y,z),(b+1,y,z),5.1))
                cut(cap,cyl((a-0.1,y,z),(a+7,y,z),12))
            y,z = p['rear_ports']['charge_data']
            cut(cap,cyl((a-1,y,z),(b+1,y,z),7.75))
            cut(cap,cyl((a-0.1,y,z),(b-4,y,z),16))
            # Sensors are inside the closed wet circuit; only the optional vent is reserved.
            for y,z in [(0,-45)]:
                cut(cap,cyl((a-0.1,y,z),(a+2,y,z),5.1))
        add('E02' if label=='FRONT' else 'E03', label+' acrylic cap; port details HOLD',cap,'01','glass',opacity=0.28)
        x0,x1 = (-g,0) if label=='FRONT' else (L,L+g)
        add('E04' if label=='FRONT' else 'E05',label+' silicone gasket 3mm free / 2.55mm working',ring(x0,x1,q['gasket_od'],q['gasket_id']),'01','silicone')
        x0,x1 = (-g,10.45) if label=='FRONT' else (L-4,L+g)
        centering = ring(x0,x1,p['body']['id']-.8,p['body']['id']-20)
        add('P01' if label=='FRONT' else 'P02',label+' non sealing centering ring',centering,'03',printed=True)

    # Four longitudinal rods; both ends carry washers and actual dome envelopes.
    sleeve_start = -g + q['washer_thickness']
    sleeve_end = L+g-q['washer_thickness']
    for i,(y,z) in enumerate(centers,1):
        rod_lo = L/2-q['rod_cut_length']/2
        rod_hi = L/2+q['rod_cut_length']/2
        assert rod_lo > cap_front[0]-1.5-10 and rod_hi < cap_rear[1]+1.5+10, 'Rod bottoms in dome nut.'
        add('R%d'%i,'M8 A4 threaded tie rod; %gmm provisional cut'%q['rod_cut_length'],cyl((rod_lo,y,z),(rod_hi,y,z),4),'02','metal')
        add('S%d'%i,'A4 compression limiter OD14 ID9 L%g'%(sleeve_end-sleeve_start),ring(sleeve_start,sleeve_end,14,9,y,z),'02','metal')
        for side, x0,x1 in [('FI',-g,-g+1.5),('RI',L+g-1.5,L+g),('FO',cap_front[0]-1.5,cap_front[0]),('RO',cap_rear[1],cap_rear[1]+1.5)]:
            add('W%d%s'%(i,side),'M8 wide washer OD22 ID9',ring(x0,x1,22,9,y,z),'02','metal')
        for side, face, direction in [('F',cap_front[0]-1.5,-1),('R',cap_rear[1]+1.5,1)]:
            # Hexagonal flats plus closed dome; thread geometry intentionally omitted.
            nut = cyl((face,y,z),(face+direction*7.5,y,z),7.51)
            for angle in (0,60,120):
                slab = box((face+direction*3.75,y,z),(8,13,40))
                rot = I(); rot.setToRotation(math.radians(angle),V(1,0,0),P(face,y,z))
                tmp.transform(slab,rot)
                intersect(nut,slab)
            dome = tmp.createSphere(P(face+direction*7.5,y,z),6.5/10)
            intersect(dome,box((face+direction*11,y,z),(7,20,20)))
            union(nut,dome)
            cut(nut,cyl((face-direction*.1,y,z),(face+direction*10,y,z),3.4))
            add('N%d%s'%(i,side),'M8 closed dome nut; verify usable blind thread',nut,'02','metal')

    optical_transform = I()
    optical_transform.setWithArray([0,0,1,12.65, 0,1,0,-3, -1,0,0,-.192, 0,0,0,1])
    tmp.transform(original_holder,optical_transform)
    # Clear a replaceable central cell mount; the source model is only a reference.
    cut(original_holder,box((126.5,0,0),(15,15,70)))
    cut(original_holder,box((126.5,-40,0),(14,6,14)))
    add('O01','Optical carrier from original cross APPROX',original_holder,'04','black','REFERENCE_APPROX')
    for _,b in original_optics:
        tmp.transform(b,optical_transform)
        as7265 = b.boundingBox.maxPoint.y*10 > 58
        add('O02' if as7265 else 'O03','AS7265x 18-channel detector APPROX' if as7265 else 'MonoSpectro camera optics APPROX',b,'04','pcb' if as7265 else 'black','REFERENCE_APPROX')
    camera_transform = I()
    cb = original_camera.boundingBox
    camera_center = [(getattr(cb.minPoint,k)+getattr(cb.maxPoint,k))/2 for k in 'xyz']
    camera_transform.setWithArray([0,1,0,4.3-camera_center[1], 1,0,0,-camera_center[0], 0,0,-1,.8+camera_center[2], 0,0,0,1])
    tmp.transform(original_camera,camera_transform)
    add('O04','Auxiliary camera APPROX; lens toward FRONT window',original_camera,'04','black','REFERENCE_APPROX')
    add('O05','Quartz flow cell APPROX; vertical water ports',box((126.5,0,0),(12.5,12.5,40)),'04','glass','REFERENCE_APPROX',opacity=.45)
    for side in (-1,1):
        add('H_CELL_'+str(side),'Flow cell port APPROX',cyl((126.5,0,side*20),(126.5,0,side*30),3.5),'06','glass','REFERENCE_APPROX',opacity=.5)
    add('O06','430nm excitation source facing AS7265x across cell',box((126.5,-40,0),(12,4,12)),'04','blue','REFERENCE_APPROX')
    add('O07','White Optisolis source transmission axis +X',box((76,0,0),(3,16,16)),'04','orange','REFERENCE_APPROX')

    # Wide structural ledges are merged into the ribbed U-shell and split for Prusa.
    for i,y in enumerate((-39,39),1):
        for j,(a,b) in enumerate([(15,L-8)],1):
            rail = box(((a+b)/2,-55 if y<0 else 55,-45),(b-a,50,10))
            intersect(rail,cyl((a-1,0,0),(b+1,0,0),84))
            rail_holes = [22,40,64,90,102,110,224,230,248,253,290,313]
            for x in rail_holes:
                if not a+2 < x < b-2:
                    continue
                cut(rail,cyl((x,y,-51),(x,y,-43),1.7))
            add('P_R%d%d'%(i,j),'Structural side ledge; source of U chassis',rail,'03',status='CARRIER_SOURCE')
    for i,(a,b) in enumerate([(11,15),(L-8,L-4)],1):
        frame = ring(a,b,168,120)
        for y in (-39,39):
            union(frame,box(((a+b)/2,y,-47),(4,14,14)))
        intersect(frame,cyl((a-1,0,0),(b+1,0,0),84))
        if i == 1:
            cut(frame,box(((a+b)/2,0,-43),(6,60,23)))
        add('P_F%d'%i,'Removable internal frame end',frame,'03',printed=True)

    tray = box((72,0,-57),(96,72,3))
    for x in (53.5,111.5):
        for y in (-24.5,24.5):
            union(tray,cyl((x,y,-55.5),(x,y,-52.5),3.5))
            cut(tray,cyl((x,y,-59),(x,y,-51.5),1.35))
    for x in (40,110):
        for y in (-39,39):
            union(tray,box((x,y,-54),(10,12,8)))
            cut(tray,cyl((x,y,-59),(x,y,-49),1.7))
    intersect(tray,cyl((20,0,0),(126,0,0),69.2))
    add('P_PI','Raspberry Pi lower mounting tray',tray,'03',printed=True)
    add('EL_PI','Raspberry Pi 4 PCB reference; USB toward front',box((72.5,0,-51.7),(85,56,1.6)),'05','pcb','REFERENCE_APPROX')
    add('EL_PI_PORTS','Pi USB/Ethernet bodies approximate',box((41,0,-43.5),(22,56,18)),'05','metal','REFERENCE_APPROX')
    add('EL_PI_PLUG_SPACE','Pi USB plug clearance; verify cable bend',box((18,0,-43.5),(24,56,18)),'05','metal','CLEARANCE_ENVELOPE',opacity=.2)

    electronics_shift = 114
    tray = box((286.5,0,42.5),(177,70,3))
    for x in (258,280):
        cut(tray,box((x,-18.5 if x==258 else 26.5,42.5),(8,37 if x==258 else 17,5)))
    for x in (216,344):
        for y in (-28,28):
            cut(tray,cyl((x,y,40),(x,y,45),1.7))
    for x in range(226,342,18):
        for y in (-22,22):
            cut(tray,box((x,y,42.5),(10,3,5)))
    add('P_TOP','Removable electronics tray; slots for cable ties',tray,'03',printed=True)
    for code,name,center,size in [
        ('EL_ESP','ESP32 dev module',(177,0,48),(55,28,8)),
        ('EL_BUCK1','5V buck Pi approx',(169,-25,49),(27,20,10)),
        ('EL_BUCK2','5V buck standby approx',(204,-25,49),(27,20,10)),
        ('EL_BUCK3','LED buck approx',(169,25,49),(27,20,10)),
        ('EL_A4988','A4988 approximate',(203,25,49),(20,15,10)),
        ('EL_RTC','RTC module approximate',(127,25,49),(35,18,10)),
        ('EL_RS485','RS485 module approximate',(126,-25,49),(40,17,10)),
        ('EL_RELAY','Charge isolation relay approximate',(220,0,53),(29,13,18))]:
        shifted = (center[0]+electronics_shift,center[1],center[2])
        if code=='EL_BUCK3': shifted=(360,25,49)
        add(code,name,box(shifted,size),'05','pcb','REFERENCE_APPROX')
    for code,name,center,size in [
        ('EL_LED_W','White LED current regulator reserve',(100,0,49),(20,15,10)),
        ('EL_LED_B','Blue LED current regulator reserve',(95,24,49),(20,18,10)),
        ('EL_GATE','Acquisition power switch reserve',(95,-24,49),(22,20,10))]:
        add(code,name,box((center[0]+electronics_shift,center[1],center[2]),size),'05','pcb','REFERENCE_APPROX')
    for x in (216,344):
        for y in (-28,28):
            post = cyl((x,y,39),(x,y,41),3.2)
            cut(post,cyl((x,y,36),(x,y,42),1.7))
            add('P_T%d_%d'%(x,y),'Electronics tray spacer; attachment to shield',post,'03',printed=True)

    bat = p['battery']
    add('EL_BAT','CITYORK 24V 3Ah pack; advertised 70x37.5x56',box(bat['center'],(bat['length'],bat['width'],bat['height'])),'05','battery','ADVERTISED_NOT_MEASURED')
    cradle = box((283,-28,-42),(76,44.5,4))
    for x,width in [(245,4),(320,2)]:
        union(cradle,box((x,-28,-33),(width,44.5,18)))
    for x in (258,306):
        for y in (-46,-10):
            cut(cradle,box((x,y,-42),(5,3,7)))
    for x in (253,313):
        for y in (-39,):
            cut(cradle,cyl((x,y,-51),(x,y,-39),1.7))
            cut(cradle,tmp.createCylinderOrCone(P(x,y,-40),.325,P(x,y,-41.55),.17))
    add('P_BAT','Removable battery cradle; two tie straps',cradle,'03',printed=True)

    pump = p['pump']; cx,cy,cz = pump['center']
    add('EL_PUMP_MOTOR','MS11HS5L410C-01 motor APPROX',box((cx,cy,cz),(28,28,51)),'05','metal','REFERENCE_APPROX')
    add('H_PUMP_HEAD','Peristaltic head APPROX; downstream of cell',cyl((cx,cy,16),(cx,cy,31),25),'06','black','REFERENCE_APPROX')
    mount = box((269,18,-39),(50,44,6))
    cut(mount,cyl((246,0,-37),(246,0,-29),4))
    for x in (255,283):
        for y in (4,32):
            cut(mount,box((x,y,-39),(3.4,9,10)))
    for x in (248,290):
        union(mount,box((x,39,-40),(8,8,8)))
        cut(mount,cyl((x,39,-51),(x,39,-35),1.7))
    add('P_PUMP','Pump universal slotted bracket; measure mounting pattern',mount,'03',printed=True)

    camera_mount = box((43,0,-25),(65,68,4))
    cut(camera_mount,cyl((65,20,-28),(65,20,-22),3))
    for y in (-32,32):
        union(camera_mount,box((43,y,-10),(65,4,30)))
        for x in (22,64):
            cut(camera_mount,box((x,y,-8),(4,7,12)))
    for x in (22,64):
        for y in (-39,39):
            union(camera_mount,box((x,y,-33),(10,14,22)))
            cut(camera_mount,cyl((x,y,-51),(x,y,-21),1.7))
    add('P_CAM','Forward camera cradle with strap adjustment',camera_mount,'03',printed=True)

    # Split optical shroud isolates the auxiliary camera from the measuring optics.
    outer = box((158,0,-3),(164,128,80))
    intersect(outer,cyl((75,0,0),(241,0,0),68))
    cut(outer,box((158,0,-3),(159,123,75)))
    cut(outer,box((76,0,0),(8,16.5,16.5)))
    for z in (-43,37):
        cut(outer,cyl((126.5,0,z-4),(126.5,0,z+4),3.5))
        # Open assembly slots: the hoses are installed as a tested cassette.
        cut(outer,box((101,0,z),(52,6,8)))
    for x in (102,230):
        for y in (-28,28):
            cut(outer,cyl((x,y,30),(x,y,40),1.7))
    for side,zc in [('LOWER',-50),('UPPER',50)]:
        half = tmp.copy(outer)
        intersect(half,box((158,0,zc),(170,140,100)))
        if side == 'LOWER':
            for x in (90,224):
                for y in (-39,39):
                    union(half,box((x,y,-42.5),(10,12,3)))
                    cut(half,cyl((x,y,-48),(x,y,-39),1.7))
            for x,offset in [(113.5,21),(190,24)]:
                for y in (-offset,offset):
                    cut(half,cyl((x,y,-44),(x,y,-39),1.7))
        for x in (80,236):
            for y in (-48,48):
                zc2 = -2 if side=='LOWER' else 2
                union(half,box((x,y,zc2),(9,12,4)))
                cut(half,cyl((x,y,-5),(x,y,5),1.7))
        add('P_HOOD_'+side,'Opaque optical cover '+side,half,'03','black',printed=True)

    for code,x,height,target in [('P_OPT_A',113.5,32,'O01'),('P_OPT_B',190,10,'O03')]:
        width = 50 if code == 'P_OPT_A' else 60
        length = 9 if code == 'P_OPT_A' else 20
        support = box((x,0,-40.5+height/2),(length,width,height))
        before = support.volume
        cut(support,tmp.copy(records[target]['temporary']))
        assert support.volume < before, 'Optical support does not contact its reference module'
        if code == 'P_OPT_A':
            cut(support,cyl((126.5,0,-42),(126.5,0,2),8))
        offset = 21 if code == 'P_OPT_A' else 24
        for y in (-offset,offset):
            cut(support,box((x,y,-33),(6,3.4,22)))
        for y in (-width/2+2,width/2-2):
            cut(support,box((x,y,-37.5),(5,3,4)))
        add(code,'Optical saddle; contact based on approximate source',support,'03','black',printed=True)

    # Split collars guide the rod sleeves. Ballast attaches to separate metal saddles.
    for station in (40,L-45):
        collar = ring(station-10,station+10,200,180.6)
        for y,z in centers:
            union(collar,cyl((station-10,y,z),(station+10,y,z),10))
        for y in (-97,97):
            union(collar,box((station,y,0),(20,18,16)))
        cut(collar,cyl((station-11,0,0),(station+11,0,0),90.3))
        for y,z in centers:
            cut(collar,cyl((station-11,y,z),(station+11,y,z),7.5))
        for y in (-30,30):
            cut(collar,cyl((station-11,y,-89),(station+11,y,-89),2.2))
        for side,z in [('LOWER',-60),('UPPER',60)]:
            half = tmp.copy(collar)
            intersect(half,box((station,0,z),(22,210,120)))
            for y in (-99,99):
                for x in (station-5,station+5):
                    cut(half,cyl((x,y,-10),(x,y,10),2.2))
            add('P_C%d_%s'%(station,side),'Split external saddle collar',half,'07',printed=True)
    for station in (52,L-33):
        saddle = box((station,0,-85),(3,180,50))
        cut(saddle,cyl((station-2,0,0),(station+2,0,0),91))
        for y,z in centers:
            if z < 0:
                cut(saddle,cyl((station-2,y,z),(station+2,y,z),7.5))
        for y in (-30,30):
            cut(saddle,cyl((station-2,y,-99),(station+2,y,-99),4))
            cut(saddle,cyl((station-2,y,-89),(station+2,y,-89),2.2))
        add('B%d'%station,'A4 3mm ballast eye plate; load test required',saddle,'07','metal')

    # Service connector and hose penetrator envelopes; NOT manufacturing drawings.
    for port in ('intake','discharge'):
        y,z = p['rear_ports'][port]
        port_body = ring(L-6,L+g+t+8,12,5,y,z)
        union(port_body,ring(L+g+t,L+g+t+5,18,5,y,z))
        add('H_'+port.upper(),'M10 WetLink JPT envelope '+port,port_body,'06','black','REFERENCE_APPROX')
        add('H_EXTERNAL_'+port.upper(),'Continuous silicone tube through '+port+'; external cut end',ring(L-6,L+50,5,3,y,z),'06','glass','ROUTE_PROPOSAL',opacity=.65)
    y,z = p['rear_ports']['charge_data']
    connector = cyl((L+g+t-4,y,z),(L+g+t+12,y,z),7.5)
    union(connector,cyl((L+g+t,y,z),(L+g+t+3,y,z),10.3))
    add('EL_EN3','EN3P8MX 8pin charging and RS485; panel 4mm local',connector,'05','black','CATALOG_ENVELOPE')

    for x,y in [(258,-2),(280,18)]:
        barb = cyl((x,y,31),(x,y,39),3)
        cut(barb,cyl((x,y,30),(x,y,40),1.5))
        add('H_PUMP_PORT_'+str(x),'Pump nozzle reservation; actual orientation pending',barb,'06','metal','REFERENCE_APPROX')

    routes = [
        ('H_TUBE_IN','Intake -> temperature tee', 'X', [(L-6,-35,35),(321,-35,35),(321,12,35),(321,12,-14)]),
        ('H_TUBE_EC_CELL','Conductivity cell -> optical cell lower port', 'X', [(155,0,-54),(126.5,0,-54),(126.5,0,-30)]),
        ('H_TUBE_CELL_PUMP','Upper optical cell -> pump intake', 'Z', [(126.5,0,30),(126.5,0,62),(155,-20,62),(220,-20,62),(258,-2,67),(258,-2,39)]),
        ('H_TUBE_OUT','Pump discharge -> rear discharge', 'Z', [(280,18,39),(280,18,65),(310,45,58),(350,35,35),(L-6,35,35)])
    ]
    for code,name,axis,points in routes:
        occ = groups['06'].occurrences.addNewComponent(I())
        c = occ.component; c.name = code+' '+name
        sketch = c.sketches.add(c.xYConstructionPlane)
        sketch.name = '3D hydraulic centerline with tangent circular bends'
        def minus(a,b): return [a[i]-b[i] for i in range(3)]
        def norm(a): return math.sqrt(sum(v*v for v in a))
        def unit(a): return [v/norm(a) for v in a]
        corners = []
        for i in range(1,len(points)-1):
            u = unit(minus(points[i-1],points[i]))
            v = unit(minus(points[i+1],points[i]))
            angle = math.acos(max(-1,min(1,sum(a*b for a,b in zip(u,v)))))
            corners.append({'u':u,'v':v,'angle':angle,'d':15/math.tan(angle/2)})
        for i in range(len(points)-1):
            left = corners[i-1]['d'] if i else 0
            right = corners[i]['d'] if i<len(corners) else 0
            available = .95*norm(minus(points[i+1],points[i]))
            if left+right > available:
                factor = available/(left+right)
                if i: corners[i-1]['d'] *= factor
                if i<len(corners): corners[i]['d'] *= factor
        curves = adsk.core.ObjectCollection.create()
        previous = points[0]
        radii = []
        for i,corner in enumerate(corners,1):
            u,v,angle,dist = corner['u'],corner['v'],corner['angle'],corner['d']
            first = [points[i][j]+u[j]*dist for j in range(3)]
            last = [points[i][j]+v[j]*dist for j in range(3)]
            bisector = unit([u[j]+v[j] for j in range(3)])
            radius = dist*math.tan(angle/2)
            assert radius > p['tube_hose']['od']/2+0.5, (code,'Bend too tight',radius)
            radii.append(round(radius,3))
            center = [points[i][j]+bisector[j]*dist/math.cos(angle/2) for j in range(3)]
            middle = [center[j]-bisector[j]*radius for j in range(3)]
            if norm(minus(first,previous)) > .001:
                curves.add(sketch.sketchCurves.sketchLines.addByTwoPoints(P(*previous),P(*first)))
            curves.add(sketch.sketchCurves.sketchArcs.addByThreePoints(P(*first),P(*middle),P(*last)))
            previous = last
        curves.add(sketch.sketchCurves.sketchLines.addByTwoPoints(P(*previous),P(*points[-1])))
        path = c.features.createPath(curves, False)
        plane_input = c.constructionPlanes.createInput()
        basis = c.yZConstructionPlane if axis=='X' else c.xYConstructionPlane
        value = points[0][0] if axis=='X' else points[0][2]
        assert plane_input.setByOffset(basis,adsk.core.ValueInput.createByReal(value/10))
        plane = c.constructionPlanes.add(plane_input)
        section = c.sketches.add(plane)
        center = section.modelToSketchSpace(P(*points[0]))
        for radius in (p['tube_hose']['od']/20,p['tube_hose']['id']/20):
            section.sketchCurves.sketchCircles.addByCenterRadius(center,radius)
        profile = next(pr for pr in section.profiles if pr.profileLoops.count==2)
        sweep = c.features.sweepFeatures.add(c.features.sweepFeatures.createInput(profile,path,adsk.fusion.FeatureOperations.NewBodyFeatureOperation))
        body = sweep.bodies.item(0); body.name = c.name
        body.appearance = colors['glass']; body.opacity=.65
        sketch.isLightBulbOn = False; section.isLightBulbOn = False; plane.isLightBulbOn = False
        bb = body.boundingBox
        manifest.append({'code':code,'name':name,'group':'06','status':'ROUTE_PROPOSAL_BEND_RADIUS_UNVERIFIED','printed':False,'bbox_mm':[round(10*(getattr(bb.maxPoint,k)-getattr(bb.minPoint,k)),3) for k in 'xyz'],'volume_cm3':round(body.volume,4),'centerline_points_mm':points,'bend_radii_mm':radii})
        c.attributes.add('cruz_m2','status','ROUTE_PROPOSAL_BEND_RADIUS_UNVERIFIED')

    fragment = os.path.join(HERE, 'details_m2.py')
    detail_scope = dict(globals(), **locals())
    exec(compile(open(fragment).read(), fragment, 'exec'), detail_scope)

    for c in groups.values():
        c.isOriginFolderLightBulbOn = False
    top.isOriginFolderLightBulbOn = False
    root.isOriginFolderLightBulbOn = False
    report = {'revision':p['revision'],'document':app.activeDocument.name,'rod_count':4,'dome_nut_count':8,'washer_count':16,'gasket_working_mm':g,'compression_limiter_length_mm':round(sleeve_end-sleeve_start,3),'parts':manifest,'status':'PRELIMINARY — interface dimensions and pressure tests pending'}
    with open(os.path.join(HERE,'manifest.json'),'w') as out:
        json.dump(report,out,indent=2)
    app.activeViewport.fit()
    print(json.dumps({'success':True,'parts':len(manifest),'rods':4,'closed_dome_nuts':8,'limiter_length_mm':sleeve_end-sleeve_start}))
