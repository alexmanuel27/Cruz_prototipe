"""Raspberry above optical hood, close to PiCam, with four M2.5 fasteners."""
import adsk.core, adsk.fusion

def run(_context):
    d=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    d.activateRootComponent()
    tmp=adsk.fusion.TemporaryBRepManager.get();B=adsk.fusion.BooleanTypes
    P=lambda x,y,z:adsk.core.Point3D.create(x/10,y/10,z/10)
    V=adsk.core.Vector3D.create
    def occ(p):return next(o for o in d.rootComponent.allOccurrences if o.component.name.startswith(p))
    def box(c,s):return tmp.createBox(adsk.core.OrientedBoundingBox3D.create(P(*c),V(1,0,0),V(0,1,0),s[0]/10,s[1]/10,s[2]/10))
    def cy(a,b,r):return tmp.createCylinderOrCone(P(*a),r/10,P(*b),r/10)
    def op(a,b,t):assert tmp.booleanOperation(a,b,t);return a
    def cut(a,b):return op(a,b,B.DifferenceBooleanType)
    def un(a,b):return op(a,b,B.UnionBooleanType)
    def copy(p):return tmp.copy(occ(p).component.bRepBodies.item(0))
    def put(c,b,index=0):
        f=c.features.baseFeatures.item(index)
        assert f.startEdit();assert f.updateBody(f.bodies.item(0),b);assert f.finishEdit()
    # Restore the front from preserved construction sources, retaining the rod clearance.
    fixed=['P_U_SOURCE ','P01 FRONT','P02 REAR','P_F1 ','P_F2 ','P_R11 ','P_R21 ','P_PI ','P_BAT ','P_PUMP ','P_CAM ','P_HOOD_LOWER ']
    front=copy(fixed[0])
    for p in fixed[1:]:un(front,copy(p))
    for x in [53.5,111.5]:
        for y in [-24.5,24.5]:cut(front,cy((x,y,-59),(x,y,-56.5),2.95))
    for x in [216,344]:
        for y in [-28,28]:cut(front,cy((x,y,34),(x,y,40),1.7))
    op(front,box((-56,0,0),(500,200,200)),B.IntersectionBooleanType)
    for y in [-39,39]:un(front,box((196.5,y,-45),(5,10,6)))
    for y in [-12,12]:cut(front,cy((157,y,-54),(344,y,-54),2.5))
    # Delete unused original Pi tray from the one-piece front chassis.
    cut(front,box((72,0,-54.5),(97,94,10)))
    put(occ('P_CHASSIS_FRONT ').component,front)

    # Rebuild the removable upper optical cover from its simple source surfaces.
    hood=box((158,0,-3),(164,128,80))
    op(hood,cy((75,0,0),(241,0,0),68),B.IntersectionBooleanType)
    cut(hood,box((158,0,-3),(159,123,75)))
    cut(hood,box((76,0,0),(8,16.5,16.5)))
    for z in [-43,37]:
        cut(hood,cy((126.5,0,z-4),(126.5,0,z+4),3.5))
        cut(hood,box((101,0,z),(52,6,8)))
    for x in [102,230]:
        for y in [-28,28]:cut(hood,cy((x,y,30),(x,y,40),1.7))
    op(hood,box((158,0,50),(170,140,100)),B.IntersectionBooleanType)
    for x in [80,236]:
        for y in [-48,48]:
            un(hood,box((x,y,2),(9,12,4)))
            cut(hood,cy((x,y,-5),(x,y,5),1.7))
    cut(hood,box((216,0,37),(12,140,10.8)))
    step=box((216,0,32.85),(12.2,128,2.7))
    op(step,cy((209,0,0),(223,0,0),68),B.IntersectionBooleanType)
    un(hood,step)
    for x in [141.5,199.5]:
        for y in [7.5,56.5]:
            un(hood,cy((x,y,36.8),(x,y,42),3.5))
            cut(hood,cy((x,y,33),(x,y,44),1.35))
    # Internal dry CSI passage; close the slit with black foam after assembly.
    cut(hood,box((185,-15,36),(20,2,8)))
    put(occ('P_HOOD_UPPER ').component,hood)
    # Rear 5 mm of Pi board overlaps the tray outline; keep it clear.
    tray=copy('P_TOP ')
    cut(tray,box((201,32,42.5),(6.5,57,5)))
    put(occ('P_TOP ').component,tray)
    # Envelope of the GPIO header; keep clear of the board mounting holes.
    put(occ('EL_PI ').component,box((82,24,-47.4),(49.5,5,7)),2)
    d.activateRootComponent()
    for p in ['EL_PI ','EL_PI_PORTS ','EL_PI_PLUG_SPACE ']:
        o=occ(p)
        if o.isGroundToParent:o.isGroundToParent=False
        m=adsk.core.Matrix3D.create();m.translation=V(8.8,3.2,9.45)
        o.transform2=m
        if d.snapshots.hasPendingSnapshot:d.snapshots.add()
    occ('EL_PI ').component.attributes.add('assembly_adjustment','fixing','4 x M2.5x12 + nuts; four 5 mm posts integral to optical cover; 58 x 49 mm pattern')
    print('Pi near MonoSpectro: board X118..203 Y4..60 Z42..43.6 mm; CSI slit X185 Y-15')
