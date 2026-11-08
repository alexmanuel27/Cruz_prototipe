import adsk.core,adsk.fusion
def run(_context):
    d=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    root=d.rootComponent;d.activateRootComponent()
    tmp=adsk.fusion.TemporaryBRepManager.get()
    P=lambda x,y,z:adsk.core.Point3D.create(x/10,y/10,z/10)
    V=adsk.core.Vector3D.create
    for prefix in ['P_CHASSIS_FRONT ','P_CHASSIS_REAR ','P_TOP ']:
        c=next(o.component for o in root.allOccurrences if o.component.name.startswith(prefix))
        assert not c.attributes.itemByName('caps_10mm','clearance'), 'Clearance already applied'
        for feature in list(c.features.extrudeFeatures):
            if feature.name.startswith(('Extremo chasis -','Alivios bandeja -')):
                assert feature.deleteMe()
        for s in list(c.sketches):
            if s.name.startswith(('Recorte extremo para tapa','Dos alivios bandeja')):
                assert s.deleteMe()
        for p in list(c.constructionPlanes):
            if p.name.startswith(('Limite chasis -','Inicio despeje racores')):
                assert p.deleteMe()
        assert c.bRepBodies.count==1
        body=tmp.copy(c.bRepBodies.item(0))
        if prefix=='P_TOP ':
            for y in [-35,35]:
                cutter=tmp.createCylinderOrCone(P(369,y,35),1.0,P(383,y,35),1.0)
                assert tmp.booleanOperation(body,cutter,adsk.fusion.BooleanTypes.DifferenceBooleanType)
        else:
            x=-49.05 if prefix=='P_CHASSIS_FRONT ' else 429.05
            cutter=tmp.createBox(adsk.core.OrientedBoundingBox3D.create(P(x,0,0),V(1,0,0),V(0,1,0),10,24,24))
            assert tmp.booleanOperation(body,cutter,adsk.fusion.BooleanTypes.DifferenceBooleanType)
        f=c.features.baseFeatures.item(0)
        assert f.startEdit();assert f.updateBody(f.bodies.item(0),body);assert f.finishEdit()
        c.attributes.add('caps_10mm','clearance','Chassis end 0.5mm or tray fitting relief radius10mm; native source in holguras_tapas_10mm.py')
    d.activateRootComponent()
    assert sum(o.bRepBodies.count for o in root.allOccurrences)==185
    print('Clearances corrected; original body organization preserved.')
