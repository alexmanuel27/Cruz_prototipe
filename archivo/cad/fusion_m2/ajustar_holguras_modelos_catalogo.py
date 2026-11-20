"""Fit catalog parts without moving the optical camera or changing cap seals.
Run once on the assembly after instalar_modelos_catalogo.py.
"""
import adsk.core, adsk.fusion, json
BASE='/Users/alex/Nube /repos/Cruz_prototipe'
def run(_context):
    app=adsk.core.Application.get();d=adsk.fusion.Design.cast(app.activeProduct)
    root=d.rootComponent;d.activateRootComponent()
    tmp=adsk.fusion.TemporaryBRepManager.get()
    P=lambda x,y,z:adsk.core.Point3D.create(x/10,y/10,z/10)
    V=adsk.core.Vector3D.create
    def occ(prefix):return next(o for o in root.allOccurrences if o.component.name.startswith(prefix))
    start=d.timeline.count
    for prefix,bounds,reason in [
        ('P_CHASSIS_REAR ',(248.75,255,23,41,-56,-45.5),'Clearance for catalog MOONS connector and wires; motor variant provisional'),
        ('P_TOP ',(196,198.6,30,35,40,61),'Remove obsolete detached tray finger interfering with Pi display connector')]:
        c=occ(prefix).component
        assert not c.attributes.itemByName('catalog_fit','relief'), 'Already adjusted'
        x0,x1,y0,y1,z0,z1=bounds
        cutter=tmp.createBox(adsk.core.OrientedBoundingBox3D.create(P((x0+x1)/2,(y0+y1)/2,(z0+z1)/2),V(1,0,0),V(0,1,0),(x1-x0)/10,(y1-y0)/10,(z1-z0)/10))
        assert c.bRepBodies.count==1
        body=tmp.copy(c.bRepBodies.item(0));old=body.volume
        assert tmp.booleanOperation(body,cutter,adsk.fusion.BooleanTypes.DifferenceBooleanType)
        assert body.volume<old
        f=c.features.baseFeatures.item(0)
        assert f.startEdit();assert f.updateBody(f.bodies.item(0),body);assert f.finishEdit()
        c.attributes.add('catalog_fit','relief',reason)
        print(prefix, 'removed cm3',old-body.volume)
    led=occ('EL_LED_B ');assert not led.component.attributes.itemByName('catalog_fit','shift')
    c=led.component;body=tmp.copy(c.bRepBodies.item(0))
    m=adsk.core.Matrix3D.create();m.translation=V(.35,0,0);assert tmp.transform(body,m)
    f=c.features.baseFeatures.item(0)
    assert f.startEdit();assert f.updateBody(f.bodies.item(0),body);assert f.finishEdit()
    c.attributes.add('catalog_fit','source_shift','3.5mm X on base body; snapshot-independent reserve relocation')
    led.component.attributes.add('catalog_fit','shift','+3.5mm X; 1.05mm Pi connector clearance; 1mm RTC reserve clearance')
    # No dimensional claims are made from reseller product photographs.
    cam=occ('O04 ').component
    cam.attributes.add('cad_provenance','source','https://www.fruugo.be/industriele-4k-usb-webcam-met-8mp-autofocus-en-imx179-sensor/p-478437047-992136824')
    cam.attributes.add('cad_provenance','status','PHOTO_IDENTIFIED_UNBRANDED; no published mechanical dimensions or verified STEP; existing envelope retained')
    pump=occ('H_PUMP_HEAD ').component
    pump.attributes.add('cad_provenance','source','https://www.fruugo.be/small-peristaltic-dosing-water-pump-with-stepper-motor-12v24v-3-rotors-silicone-for-lawn-irrigation/p-550072799-1112187245')
    pump.attributes.add('cad_provenance','status','PHOTO_KAS-SF-B063_24V20W; no exact STEP or dimensional drawing verified; 50x15mm reserve retained; ports provisional')
    amber=d.appearances.addByCopy(d.appearances.itemByName('M2 Optical black'),'Pump amber - photo reference, geometry provisional')
    for name in ['opaque_albedo','surface_albedo']:
        p=adsk.core.ColorProperty.cast(amber.appearanceProperties.itemById(name))
        if p:p.value=adsk.core.Color.create(184,123,38,255)
    for b in pump.bRepBodies:b.appearance=amber
    if d.snapshots.hasPendingSnapshot:d.snapshots.add()
    if d.timeline.count>start:
        g=d.timeline.timelineGroups.add(start,d.timeline.count-1);g.name='Holguras para CAD de catalogo; referencias fotograficas'
    app.activeViewport.refresh()
    print('Catalog fit updates complete; optical alignment and cap seals preserved.')
