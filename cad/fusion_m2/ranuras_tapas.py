"""Caps from 10 mm PMMA stock with a 3 mm interior gasket groove.
Current assembly patch, not a pressure qualification or a CNC toolpath.
"""
import adsk.core, adsk.fusion, math, json
BASE='/Users/alex/Nube /repos/Cruz_prototipe/cad/fusion_m2'

def run(_context):
    app=adsk.core.Application.get()
    d=adsk.fusion.Design.cast(app.activeProduct)
    root=d.rootComponent
    d.activateRootComponent()
    tmp=adsk.fusion.TemporaryBRepManager.get()
    P=lambda x,y,z:adsk.core.Point3D.create(x/10,y/10,z/10)
    def cyl(a,b,r):
        return tmp.createCylinderOrCone(P(*a),r/10,P(*b),r/10)
    def cut(a,b):
        assert tmp.booleanOperation(a,b,adsk.fusion.BooleanTypes.DifferenceBooleanType)
    def find(prefix):
        return next(o for o in root.allOccurrences if o.component.name.startswith(prefix))
    def replace(c,b):
        f=c.features.baseFeatures.item(0)
        assert f.startEdit()
        assert f.updateBody(f.bodies.item(0),b)
        assert f.finishEdit()
    caps=[find('E02 '),find('E03 ')]
    assert abs(d.userParameters.itemByName('M2_Cap_thickness').value-1.6)<1e-6, 'Run once on the 16 mm interim caps'
    assert all(o.component.features.extrudeFeatures.count==2 for o in caps), 'Unexpected cap state'
    assert d.exportManager.execute(d.exportManager.createFusionArchiveExportOptions(BASE+'/CROSS_ANTES_TAPAS_10MM_2026-11-02.f3d'))
    before={o.fullPathName:[b.volume for b in o.bRepBodies] for o in root.allOccurrences}
    centers=[(101*math.cos(math.radians(a)),101*math.sin(math.radians(a))) for a in (45,135,225,315)]
    for o in caps:
        c=o.component
        assert c.features.extrudeFeatures.item(1).deleteMe()
        for s in list(c.sketches):
            assert s.deleteMe()
        assert c.features.extrudeFeatures.item(0).deleteMe()
    d.userParameters.itemByName('M2_Cap_thickness').expression='10 mm'
    d.userParameters.itemByName('M2_Groove_depth').expression='3 mm'
    data=[]
    for o,side in zip(caps,['FRONT','REAR']):
        c=o.component
        a,b=(-9.55,.45) if side=='FRONT' else (379.55,389.55)
        solid=cyl((a,0,0),(b,0,0),115)
        for y,z in centers:
            cut(solid,cyl((a-1,y,z),(b+1,y,z),4.5))
        if side=='REAR':
            for y,z in [(-35,35),(35,35)]:
                cut(solid,cyl((a-1,y,z),(b+1,y,z),5.1))
                cut(solid,cyl((a-.1,y,z),(a+2,y,z),12))
            cut(solid,cyl((a-1,30,-30),(b+1,30,-30),7.75))
            cut(solid,cyl((a-.1,30,-30),(b-4,30,-30),16))
            cut(solid,cyl((a-.1,0,-45),(a+2,0,-45),5.1))
        replace(c,solid)
        c.features.baseFeatures.item(0).name=side+' PMMA stock 10 mm - through holes and connector seats'
        d.activateRootComponent()
    start=d.timeline.count
    for o,side in zip(caps,['FRONT','REAR']):
        c=o.component
        b=c.bRepBodies.item(0)
        x=.045 if side=='FRONT' else 37.955
        face=next(f for f in b.faces if f.geometry.objectType=='adsk::core::Plane'
                  and abs(f.pointOnFace.x-x)<1e-6 and f.area>300)
        s=c.sketches.addWithoutEdges(face)
        s.name=side+' junta plana - ID168.8 OD181.2'
        center=s.modelToSketchSpace(adsk.core.Point3D.create(x,0,0))
        for rad,param in [(8.44,'M2_Groove_ID'),(9.06,'M2_Groove_OD')]:
            circle=s.sketchCurves.sketchCircles.addByCenterRadius(center,rad)
            dim=s.sketchDimensions.addDiameterDimension(circle,adsk.core.Point3D.create(rad,3,0))
            dim.parameter.expression=param
        area=math.pi*(9.06**2-8.44**2)
        profile=next(p for p in s.profiles if abs(p.areaProperties().area-area)<1e-5)
        inp=c.features.extrudeFeatures.createInput(profile,adsk.fusion.FeatureOperations.CutFeatureOperation)
        inp.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(adsk.core.ValueInput.createByString('M2_Groove_depth')),adsk.fusion.ExtentDirections.NegativeExtentDirection)
        inp.participantBodies=[b]
        f=c.features.extrudeFeatures.add(inp)
        f.name='CNC - ranura junta 3 mm; fondo acrilico 7 mm'
        s.isVisible=False
        assert all(f.healthState==adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState for f in c.features.extrudeFeatures)
        bb=c.bRepBodies.item(0).boundingBox
        assert abs((bb.maxPoint.x-bb.minPoint.x)*10-10)<1e-6
        data.append({'side':side,'x_limits_mm':[bb.minPoint.x*10,bb.maxPoint.x*10],
                     'stock_mm':10,'groove_depth_mm':3,'floor_mm':7,
                     'groove_id_mm':168.8,'groove_od_mm':181.2})
    # Preserve the original nut engagement with a 16 mm shorter rod.
    for i,(y,z) in enumerate(centers,1):
        o=find('R'+str(i)+' ')
        replace(o.component,cyl((-20,y,z),(400,y,z),4))
        sleeve=cyl((1.95,y,z),(378.05,y,z),7)
        cut(sleeve,cyl((1,y,z),(379,y,z),4.5))
        so=find('S'+str(i)+' ')
        replace(so.component,sleeve)
        so.component.name='S'+str(i)+' A4 compression limiter OD14 ID9 L376.1'
        so.component.bRepBodies.item(0).name=so.component.name
    d.activateRootComponent()
    moved=[]
    for o in list(root.allOccurrences):
        code=o.component.name.split(' ')[0]
        delta=0
        if code in ['W'+str(i)+'FO' for i in range(1,5)]+['N'+str(i)+'F' for i in range(1,5)]:
            delta=8
        elif code in ['W'+str(i)+'RO' for i in range(1,5)]+['N'+str(i)+'R' for i in range(1,5)]+['H_INTAKE','H_DISCHARGE','EL_EN3']:
            delta=-8
        if code in ['W'+str(i)+'FI' for i in range(1,5)]: delta=3
        if code in ['W'+str(i)+'RI' for i in range(1,5)]: delta=-3
        if delta:
            o.isGroundToParent=False
            t=o.transform2
            v=t.translation
            v.x+=delta/10
            t.translation=v
            o.transform2=t
            moved.append({'component':o.component.name,'dx_mm':delta})
    if d.snapshots.hasPendingSnapshot:d.snapshots.add()
    group=d.timeline.timelineGroups.add(start,d.timeline.count-1)
    group.name='CNC - tapas 10 mm, ranuras 3 mm y ajuste de cierre'
    for i in range(1,5):
        o=find('R'+str(i)+' ')
        o.component.name='R'+str(i)+' M8 A4 threaded tie rod; 420mm provisional cut'
        o.component.bRepBodies.item(0).name=o.component.name
    for o,side in zip(caps,['FRONT','REAR']):
        o.component.name=('E02' if side=='FRONT' else 'E03')+' '+side+' PMMA cap 10mm; gasket groove 3mm'
        o.component.bRepBodies.item(0).name=o.component.name
    result={'caps':data,'body_count':sum(o.bRepBodies.count for o in root.allOccurrences),
            'gasket_free_mm':3,'gasket_working_mm':2.55,'compression_percent':15,
            'tube_insertion_into_groove_mm':.45,'rod_cut_mm':420,
            'compression_limiter_mm':376.1,'washer_seat_pockets':False,
            'moved':moved,'cnc_status':'Editable geometry; CAM setup and pressure test pending'}
    assert result['body_count']==185
    with open(BASE+'/TAPAS_10MM_RANURA_3MM_2026-11-03.json','w') as f:
        json.dump(result,f,indent=2,ensure_ascii=False)
    app.activeViewport.refresh()
    print(json.dumps(result,ensure_ascii=False))

