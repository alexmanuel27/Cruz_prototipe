"""Install downloaded catalog CAD in the current M2 assembly; preserve part provenance."""
import adsk.core, adsk.fusion, json, math
BASE='/Users/alex/Nube /repos/Cruz_prototipe'
def run(_context):
    app=adsk.core.Application.get()
    d=adsk.fusion.Design.cast(app.activeProduct);root=d.rootComponent
    d.activateRootComponent()
    I=adsk.core.Matrix3D.create;P=adsk.core.Point3D.create;V=adsk.core.Vector3D.create
    tmp=adsk.fusion.TemporaryBRepManager.get()
    stage=next(o for o in root.allOccurrences if o.component.name=='TEMP_REVISION_STEP_2026_11_03')
    assets={o.component.name:o.component for o in stage.childOccurrences}
    def occurrence(prefix):
        return next(o for o in root.allOccurrences if o.component.name.startswith(prefix))
    def component(name):
        return next(o.component for o in root.allOccurrences if o.component.name==name)
    def transform(origin,axes=None):
        m=I()
        if axes:assert m.setWithCoordinateSystem(P(*(v/10 for v in origin)),*[V(*v) for v in axes])
        else:m.translation=V(*(v/10 for v in origin))
        return m
    def install(asset,parent,name,m,source,status):
        c=assets[asset]
        o=parent.occurrences.addExistingComponent(c,m)
        assert o
        c.name=name
        c.attributes.add('cad_provenance','source',source)
        c.attributes.add('cad_provenance','status',status)
        o.isLightBulbOn=True
        return o
    old=[occurrence(p) for p in ['EL_PI ','EL_PI_PORTS ','EL_EZO ','EL_GATE ','EL_PUMP_MOTOR ','H_INTAKE ','H_DISCHARGE ']]
    start=d.timeline.count
    pi_parent=component('01_RASPBERRY_PI_4_JUNTO_PICAM')
    electronics=component('05_ELECTRONICA_REFERENCIAS')
    hydraulics=component('01_ENTRADA_Y_SALIDA')
    pi=install('PI4_COMUNIDAD',pi_parent,'EL_PI Raspberry Pi 4 Model B - CAD comunidad cotejado',transform((160.5,31.64793078422418,43.152069215775826),[(-1,0,0),(0,-1,0),(0,0,1)]),
        'https://github.com/multigamesystem/MGS-CAD-Files/blob/main/STEP%20files%20with%20images/Raspberry%20Pi%204%20Model%20B%20v4.step','COMMUNITY_NOT_OFFICIAL_RPI; 85x56 PCB and mounting pattern to check')
    plug=occurrence('EL_PI_PLUG_SPACE ')
    plug.isGroundToParent=False
    t=plug.transform2;v=t.translation;v.x-=.399;t.translation=v;plug.transform2=t
    pololu=install('POLOLU_2814_OFICIAL',electronics,'EL_GATE Pololu 2814 - STEP fabricante',transform((196.895,-13.68,44),[(0,-1,0),(1,0,0),(0,0,1)]),
        'https://www.pololu.com/product/2814/resources','MANUFACTURER_STEP; family Big MOSFET Slide Switch')
    atlas=assets['ATLAS_CARRIER_OFICIAL']
    pcb=next(b for o in atlas.allOccurrences if 'Board_Iso_carry' in o.component.name for b in o.bRepBodies)
    face=max([f for f in pcb.faces if f.geometry.objectType=='adsk::core::Plane'],key=lambda f:f.area)
    edge=max([e for e in face.edges if e.geometry.objectType=='adsk::core::Line3D'],key=lambda e:e.length)
    u=edge.endVertex.geometry.vectorTo(edge.startVertex.geometry)
    if u.z<0:u.scaleBy(-1)
    u.normalize();y=V(0,1,0);z=u.crossProduct(y)
    m=I();assert m.setToAlignCoordinateSystems(P(0,0,0),u,y,z,P(0,0,0),V(1,0,0),V(0,1,0),V(0,0,1))
    boxes=[]
    for sub in atlas.allOccurrences:
        for b in sub.bRepBodies:
            copy=tmp.copy(b);assert tmp.transform(copy,m);boxes.append(copy.boundingBox)
    bb=boxes[0].copy()
    for box in boxes[1:]:bb.combine(box)
    m.translation=V(34.2-(bb.minPoint.x+bb.maxPoint.x)/2,-7-bb.minPoint.y,-(bb.minPoint.z+bb.maxPoint.z)/2)
    carrier=install('ATLAS_CARRIER_OFICIAL',electronics,'EL_EZO Atlas ISCCB Gen2 - STEP fabricante; cotejar revision',m,
        'https://atlas-scientific.com/carrier-boards/electrically-isolated-ezo-carrier-board-gen-2/','MANUFACTURER_GEN2_STEP; physical kit revision and EZO daughterboard not confirmed')
    motor=install('MOONS_MS11HS5P_FAMILIA_OFICIAL',electronics,'EL_PUMP_MOTOR MOONS MS11HS5P - CAD familia; NO variante exacta',transform((254.85,17.85,-4),[(1,0,0),(0,-1,0),(0,0,-1)]),
        'https://www.moonsindustries.com/jp/p/nema-11-standard-hybrid-stepper-motors/ms11hs5p4100-000004611110015856','MANUFACTURER_FAMILY_REFERENCE_ONLY; not exact MS11HS5L410C-01; shaft/head pending actual dimensions')
    for o in motor.component.allOccurrences:
        for b in o.bRepBodies:
            if not b.isSolid:b.isLightBulbOn=False
    wet=[]
    for name,y in [('ENTRADA',-35),('SALIDA',35)]:
        group=hydraulics.occurrences.addNewComponent(I());group.component.name='JPT_'+name+' M10 5.5mm - CAD Blue Robotics'
        wet.append(install('JPT_OFICIAL',group.component,'WetLink JPT M10 5.5mm - STEP fabricante',transform((344.55,y,35)),
            'https://bluerobotics.com/store/cables-connectors/penetrators/wetlink-penetrator-jpt/','MANUFACTURER_X55_SHARED_CAD; downloaded LC geometry, HC seal not represented'))
        wet.append(install('TUERCA_JPT_OFICIAL',group.component,'Tuerca M10 WetLink - STEP fabricante',transform((377.55,y,35)),
            'https://cad.bluerobotics.com/WL-M10-NUT-R1.zip','MANUFACTURER_STEP; threads modeled'))
    # Old occurrences are removed from the browser after replacements exist.
    for o in old:assert root.features.removeFeatures.add(o)
    assert root.features.removeFeatures.add(stage)
    if d.snapshots.hasPendingSnapshot:d.snapshots.add()
    # Import operations already have their own groups; group only this placement stage.
    group=d.timeline.timelineGroups.add(start,d.timeline.count-1)
    group.name='CAD catalogo - Raspberry, Atlas, Pololu, motor y pasamuros'
    app.activeViewport.fit();app.activeViewport.refresh()
    report={'models':['Raspberry Pi 4 community','Atlas ISCCB Gen2 manufacturer','Pololu2814 manufacturer','MOONS MS11HS5P manufacturer family','WetLink JPT X55 manufacturer shared CAD','WetLink nut manufacturer'],
            'removed_approximate_occurrences':len(old),'staging_removed':True,
            'body_count':sum(o.bRepBodies.count for o in root.allOccurrences)}
    with open(BASE+'/cad/fusion_m2/MODELOS_STEP_COLOCACION_2026-11-03.json','w') as f:json.dump(report,f,indent=2)
    print(json.dumps(report))
