"""Local mechanical adjustments to the existing M2 assembly. Units in millimetres.
Run once in Fusion; does not rebuild the project or save the active document.
"""
import adsk.core
import adsk.fusion


def run(_context):
    d = adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    root = d.rootComponent
    tmp = adsk.fusion.TemporaryBRepManager.get()
    B = adsk.fusion.BooleanTypes
    P = lambda x,y,z: adsk.core.Point3D.create(x/10,y/10,z/10)
    V = adsk.core.Vector3D.create
    def occ(prefix):
        return next(o for o in root.allOccurrences if o.component.name.startswith(prefix))
    def box(center,size):
        return tmp.createBox(adsk.core.OrientedBoundingBox3D.create(P(*center),V(1,0,0),V(0,1,0),size[0]/10,size[1]/10,size[2]/10))
    def cyl(a,b,r):
        return tmp.createCylinderOrCone(P(*a),r/10,P(*b),r/10)
    def boolean(a,b,op):
        assert tmp.booleanOperation(a,b,op)
        return a
    def cut(a,b): return boolean(a,b,B.DifferenceBooleanType)
    def union(a,b): return boolean(a,b,B.UnionBooleanType)
    def update(prefix,body):
        c=occ(prefix).component
        assert not c.attributes.itemByName('assembly_adjustment','v2'), 'Already adjusted: '+prefix
        base=c.features.baseFeatures.item(0)
        assert base.startEdit()
        assert base.updateBody(base.bodies.item(0),body)
        assert base.finishEdit()
        c.attributes.add('assembly_adjustment','v2','2026-11-02; ajuste_montaje_solapamientos.py')
        print('Adjusted',c.name)
    def copy(prefix): return tmp.copy(occ(prefix).component.bRepBodies.item(0))

    # Free passage around conductivity-cassette rods, 1 mm radial clearance.
    for code in ['P_CHASSIS_FRONT ','P_CHASSIS_REAR ']:
        body=copy(code)
        for y in [-12,12]: cut(body,cyl((157,y,-54),(344,y,-54),2.5))
        if code.startswith('P_CHASSIS_REAR'):
            # Remove the old motor platform; leave the optical and battery mounts.
            cut(body,box((269,20,-38.5),(51,49,12)))
            cut(body,box((269,32,-29.5),(30,30,53)))
            # Lower pump seat: two retaining straps through four slots.
            seat=box((269,36,-57),(50,44,4))
            for x in [258,280]:
                for y in [16,48]: cut(seat,box((x,y,-57),(4,3,8)))
            for x in [253,285]: union(seat,box((x,32,-48.5),(2,30,13)))
            # The outer edge merges into the curved U chassis.
            boolean(seat,cyl((243,0,0),(295,0,0),84),B.IntersectionBooleanType)
            union(body,seat)
            # A lateral EZO mount replaces the obstructing old plate and cheek.
            cut(body,box((344,-66,4),(10,25,60)))
            # Two short M3 bosses join the curved wall to the new plate.
            for x in [316,368]:
                union(body,cyl((x,-80,-20),(x,-73.8,-20),4))
                cut(body,cyl((x,-86,-20),(x,-68,-20),1.7))
            boolean(body,cyl((190,0,0),(381,0,0),84),B.IntersectionBooleanType)
        update(code,body)

    # Lower the optical roof locally below the 216 mm cross beam.
    hood=copy('P_HOOD_UPPER ')
    cut(hood,box((216,0,37),(12,140,10.8)))
    step=box((216,0,32.85),(12.2,128,2.7))
    boolean(step,cyl((209,0,0),(223,0,0),68),B.IntersectionBooleanType)
    union(hood,step)
    update('P_HOOD_UPPER ',hood)

    # Small local relief around the actual detector envelope; no optical movement.
    holder=copy('O01 ')
    cut(holder,box((136.5,24.5,-1.9),(2,4.5,6.5)))
    update('O01 ',holder)

    # Move the EC inlet clear of the cable gland and the tie-rod nut.
    inlet=occ('H_EC_IN ')
    m=inlet.transform2; v=m.translation; v.y-=1.8; v.z+=.4; m.translation=v; inlet.transform2=m
    cap=box((332,0,-54),(6,30,22))
    cut(cap,cyl((328,0,-54),(332,0,-54),8))
    cut(cap,cyl((328,0,-54),(336,0,-54),5.1))
    cut(cap,cyl((335,-9,-46),(329,-5,-50),1.5))
    for y in [-12,12]:cut(cap,cyl((328,y,-54),(336,y,-54),1.7))
    update('H_EC_REAR ',cap)

    # Distinguish the Raspberry board and ports, and show the four mounting holes.
    pi=copy('EL_PI ')
    for x in [53.5,111.5]:
        for y in [-24.5,24.5]:cut(pi,cyl((x,y,-54),(x,y,-49),1.35))
    update('EL_PI ',pi)
    ports=box((41,0,-42.9),(22,56,16))
    update('EL_PI_PORTS ',ports)

    # New removable sensor bracket: one flat print, two M3 screws, two ties.
    main=next(o for o in root.occurrences if o.component.name=='M2_GENERATED')
    support_parent=next(o for o in main.childOccurrences if o.component.name=='03_CHASIS_Y_SOPORTES').component
    group=support_parent.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    group.component.name='06_3D_FIJACIONES_REVISADAS'
    o=group.component.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    o.component.name='P_EZO_V2 Placa lateral - 2 tornillos M3 y 2 bridas'
    plate=box((342,-72,0),(64,4,48))
    for x in [316,368]:cut(plate,cyl((x,-76,-20),(x,-68,-20),1.7))
    for x in [322,362]:
        for z in [-19,20]:cut(plate,box((x,-72,z),(5,8,1.8)))
    base=o.component.features.baseFeatures.add();base.name='EZO_V2 - editable source in adjustment script'
    assert base.startEdit();o.component.bRepBodies.add(plate,base);assert base.finishEdit()
    o.component.bRepBodies.item(0).appearance=d.appearances.itemByName('M2 Teal printed ASA')
    o.component.attributes.add('assembly_adjustment','fixing','2 x M3 through bolts + nuts; 2 cable ties; prototype fit to check')
    if d.snapshots.hasPendingSnapshot:d.snapshots.add()
    print('Mechanical supports revised; document not saved')
