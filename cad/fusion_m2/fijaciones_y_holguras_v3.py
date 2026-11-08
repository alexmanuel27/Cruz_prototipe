"""Mechanical completion of V3 placement. No document save; mm dimensions.
Includes simple prototype fasteners and extra routing space, not pressure validation.
"""
import adsk.core, adsk.fusion, math

def run(_context):
    d=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    root=d.rootComponent
    tmp=adsk.fusion.TemporaryBRepManager.get()
    B=adsk.fusion.BooleanTypes
    P=lambda x,y,z:adsk.core.Point3D.create(x/10,y/10,z/10)
    V=adsk.core.Vector3D.create
    def occ(p):return next(o for o in root.allOccurrences if o.component.name.startswith(p))
    def box(p,s):return tmp.createBox(adsk.core.OrientedBoundingBox3D.create(P(*p),V(1,0,0),V(0,1,0),s[0]/10,s[1]/10,s[2]/10))
    def cyl(a,b,r):return tmp.createCylinderOrCone(P(*a),r/10,P(*b),r/10)
    def op(a,b,k):
        assert tmp.booleanOperation(a,b,k)
        return a
    def cut(a,b):return op(a,b,B.DifferenceBooleanType)
    def union(a,b):return op(a,b,B.UnionBooleanType)
    def copy(p):return tmp.copy(occ(p).component.bRepBodies.item(0))
    def update(p,b):
        c=occ(p).component
        assert not c.attributes.itemByName('assembly_adjustment','v3'),p+' already adjusted'
        f=c.features.baseFeatures.item(0)
        assert f.startEdit();assert f.updateBody(f.bodies.item(0),b);assert f.finishEdit()
        c.attributes.add('assembly_adjustment','v3','fijaciones_y_holguras_v3.py')
        print('Adjusted',c.name)
    def newbody(c,b,n,appearance):
        f=c.features.baseFeatures.add();f.name=n
        assert f.startEdit();c.bRepBodies.add(b,f);assert f.finishEdit()
        c.bRepBodies.item(c.bRepBodies.count-1).appearance=d.appearances.itemByName(appearance)

    # Rear chassis: open 8 mm passages in the crossbeam, instead of bending tightly.
    rear=copy('P_CHASSIS_REAR ')
    for y in [-35,35]:cut(rear,cyl((338,y,35),(350,y,35),4))
    cut(rear,box((365,-9,-68),(10,12,17)))
    cut(rear,box((342,-71.95,0),(65,4.1,48.4)))
    # Simple integrated shelf supports the temperature tee, retained with two ties.
    seat=box((321,25,-41.5),(24,24,3))
    union(rear,seat)
    cut(rear,cyl((321,25,-52),(321,25,-38),4))
    for x in [314,328]:
        for y in [15,35]:cut(rear,box((x,y,-41.5),(3,1.8,7)))
    update('P_CHASSIS_REAR ',rear)

    # Raspberry Pi fits vertically beside the front camera, on four bolted posts.
    front=copy('P_CHASSIS_FRONT ')
    cut(front,box((72,0,-54.5),(97,94,10)))
    for x in [53.5,111.5]:
        for z in [-24.5,24.5]:
            union(front,cyl((x,-79,z),(x,-52,z),3.5))
            cut(front,cyl((x,-83,z),(x,-48,z),1.35))
            # Slide-in nut pocket. M2.5 nut flats retained along Z.
            cut(front,box((x,-73.8,z),(8,2.3,5.3)))
    update('P_CHASSIS_FRONT ',front)

    # PCB edge clips fasten outside the board: no holes through unfinished PCB.
    tray=copy('P_TOP ')
    for x in [216,344]:
        for side in [-1,1]:
            union(tray,box((x,side*41.5,42.5),(14,21,3)))
            cut(tray,cyl((x,side*48,40),(x,side*48,45),1.7))
    for x in [197.5,370.5]:union(tray,box((x,32.5,51.7),(2,4,15.4)))
    update('P_TOP ',tray)
    group=occ('06_3D_FIJACIONES_REVISADAS').component
    for x in [216,344]:
        for side in [-1,1]:
            foot=box((x,side*41,45.5),(12,22,3))
            union(foot,box((x,side*39.5,52.7),(12,4,11.4)))
            union(foot,box((x,side*37,55.15),(12,9,1.3)))
            union(foot,box((x,side*37,58.6),(12,9,1.6)))
            union(foot,cyl((x,side*48,44),(x,side*48,59.4),4))
            cut(foot,cyl((x,side*48,43),(x,side*48,61),1.7))
            o=group.occurrences.addNewComponent(adsk.core.Matrix3D.create())
            o.component.name='P_PCB_CLIP_%d_%s M3x25 - ranura para borde PCB'%(x,'L' if side<0 else 'R')
            newbody(o.component,foot,'Clip PCB - 2 mm slot, no board drill','M2 Teal printed ASA')
            o.component.attributes.add('assembly_adjustment','fixing','1 x M3x25 + nut and washers; board-edge slot 2.0 mm')

    # A recognizable Raspberry reference, keeping mechanical mounting dimensions.
    update('EL_PI_PORTS ',box((38.5,18,-44.15),(17,16,13.5)))
    c=occ('EL_PI_PORTS ').component
    for y in [-18,0]:newbody(c,box((39,y,-42.9),(18,15,16)),'USB stack approximate','Steel - Satin')
    c=occ('EL_PI ').component
    newbody(c,box((82,0,-49.65),(15,15,2.5)),'CPU envelope approximate','M2 Optical black')
    newbody(c,box((85,24,-47.4),(50,5,7)),'40 pin GPIO header envelope approximate','M2 Optical black')
    # Apply and capture placement after all base edits have finished.
    rotation=adsk.core.Matrix3D.create()
    rotation.setToRotation(math.pi/2,V(1,0,0),P(0,0,0))
    rotation.translation=V(0,-10.29,0)
    for prefix in ['EL_PI ','EL_PI_PORTS ','EL_PI_PLUG_SPACE ']:
        occ(prefix).transform2=rotation
    occ('EL_PI ').component.attributes.add('assembly_adjustment','fixing','4 x M2.5x25 + captive nuts in lateral posts; 58 x 49 mm pattern')
    if d.snapshots.hasPendingSnapshot:d.snapshots.add()
    print('Raspberry positioned vertically; clips and simple through fasteners added')
