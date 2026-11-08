"""Replace the long wet EC enclosure by tip-only insertion.
Official Atlas STEP is a legacy generation: dry-envelope fit still needs checking
against the purchased probe. Dimensions in mm; no Fusion document save.
"""
import adsk.core, adsk.fusion

def run(_context):
    app=adsk.core.Application.get();d=adsk.fusion.Design.cast(app.activeProduct);d.activateRootComponent()
    tmp=adsk.fusion.TemporaryBRepManager.get();B=adsk.fusion.BooleanTypes
    P=lambda x,y,z:adsk.core.Point3D.create(x/10,y/10,z/10);V=adsk.core.Vector3D.create
    def oc(p):return next(o for o in d.rootComponent.allOccurrences if o.component.name.startswith(p))
    def box(c,s):return tmp.createBox(adsk.core.OrientedBoundingBox3D.create(P(*c),V(1,0,0),V(0,1,0),s[0]/10,s[1]/10,s[2]/10))
    def cy(a,b,r):return tmp.createCylinderOrCone(P(*a),r/10,P(*b),r/10)
    def op(a,b,k):assert tmp.booleanOperation(a,b,k);return a
    def cut(a,b):return op(a,b,B.DifferenceBooleanType)
    def un(a,b):return op(a,b,B.UnionBooleanType)
    def put(c,b):
        f=c.features.baseFeatures.item(0);assert f.startEdit();assert f.updateBody(f.bodies.item(0),b);assert f.finishEdit()
    parent=oc('06_AGUA_Y_SENSORES').component
    group=parent.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    group.component.name='03_CONDUCTIVIDAD_SOLO_PUNTA_HUMEDA'
    def add(name,b,color,status):
        o=group.component.occurrences.addNewComponent(adsk.core.Matrix3D.create());c=o.component;c.name=name
        f=c.features.baseFeatures.add();f.name='EC punta humeda - editable source script'
        assert f.startEdit();c.bRepBodies.add(b,f);assert f.finishEdit()
        c.bRepBodies.item(0).appearance=d.appearances.itemByName(color)
        c.attributes.add('ec_tip_only','status',status)
        return o
    # Use the actual electrode apertures from the manufacturer's model.
    official=oc('ENV-40-EC-K=1').component.bRepBodies.item(0)
    probe=tmp.copy(official)
    op(probe,box((0,-35,0),(40,150,40)),B.IntersectionBooleanType) # trim display cable only, not the physical probe
    m=adsk.core.Matrix3D.create()
    m.setWithArray([0,1,0,29.6,1,0,0,0,0,0,-1,-6,0,0,0,1])
    assert tmp.transform(probe,m)
    p=add('EC4_SONDA Atlas K1 oficial - punta mojada y cuerpo seco',probe,'M2 Optical black','Manufacturer legacy STEP, 2021; confirm generation. Tip X186; active-zone envelope X186..201.5')
    p.component.attributes.add('ec_tip_only','source','https://files.atlas-scientific.com/ENV-40-EC-K-1.0.zip')
    # Short machined flow block: the rest of the probe is in dry air.
    body=cy((175,0,-60),(203,0,-60),12.5)
    un(body,cy((203,0,-60),(212,0,-60),14))
    cut(body,cy((178,0,-60),(206,0,-60),10))
    cut(body,cy((206,0,-60),(213,0,-60),10.8))
    cut(body,cy((164,0,-51.5),(179,0,-51.5),1.5))
    cut(body,cy((205.5,-2,-60),(205.5,25,-60),1.5))
    add('EC4_BLOQUE_FLUJO Corto 37 mm - solo zona activa',body,'Glass (Clear)','Machined flow block proposal; thread, fitting and seals to validate before manufacture')
    outlet=cy((165,0,-51.5),(175,0,-51.5),3)
    cut(outlet,cy((164,0,-51.5),(179,0,-51.5),1.5))
    add('EC4_SALIDA_SUPERIOR Hacia cubeta - purga del punto alto',outlet,'Steel - Satin','Flow proposal: high outlet at cavity roof; no full-length wet housing')
    inlet=cy((205.5,14,-60),(205.5,24,-60),3)
    cut(inlet,cy((205.5,-2,-60),(205.5,25,-60),1.5))
    add('EC4_ENTRADA_LATERAL Desde temperatura',inlet,'Steel - Satin','3 mm bore, 5 mm hose interface to verify')
    # Reserve for a commercial 12 mm probe compression fitting. Do not print a seal.
    gland=cy((206.2,0,-60),(220,0,-60),10.5)
    un(gland,cy((212.2,0,-60),(238,0,-60),15))
    cut(gland,cy((205,0,-60),(239,0,-60),6.25))
    add('EC4_RACOR_12mm Sellado del vastago - reserva dimensional',gland,'M2 Optical black','Commercial probe compression fitting required; 1/2 NPT Atlas candidate; OD/length are space reserves, not certified drawing')
    # Two soft saddles hold the small chamber and dry probe head.
    for station,radius in [(181,12.5),(300,8.15)]:
        foam=cy((station-3,0,-60),(station+3,0,-60),radius+2)
        cut(foam,cy((station-4,0,-60),(station+4,0,-60),radius))
        op(foam,box((station,0,-72),(8,40,24)),B.IntersectionBooleanType)
        add('EC4_ESPUMA_%d Apoyo seco - cortar, NO imprimir'%station,foam,'M2 Silicone grey','2 mm closed-cell foam; retain with ties, no strain on probe seal')
    # Integrate both saddles into the existing printed chassis.
    for prefix,station,radius in [('P_CHASSIS_FRONT ',181,14.5),('P_CHASSIS_REAR ',300,10.15)]:
        c=oc(prefix).component;carrier=tmp.copy(c.bRepBodies.item(0))
        saddle=box((station,0,-73),(8,36,18))
        op(saddle,cy((station-5,0,0),(station+5,0,0),84),B.IntersectionBooleanType)
        un(carrier,saddle)
        cut(carrier,cy((station-5,0,-60),(station+5,0,-60),radius))
        for y in [-18,18]:cut(carrier,box((station,y,-71),(10,3,3)))
        put(c,carrier)
    # Keep the old assembly hidden as a reference, including its obsolete seals/rods.
    old=oc('03_SENSOR_CONDUCTIVIDAD_Y_CELDA')
    old.component.name='90_EC_CAMARA_LARGA_DESCARTADA_NO_USAR';old.isLightBulbOn=False
    for prefix in ['H_TUBE_EC_CELL ','H3_TUBE_TEMP_EC ']:
        o=oc(prefix);o.isLightBulbOn=False
        o.component.attributes.add('ec_tip_only','superseded','tip-only EC layout')
    d.activateRootComponent()
    print('Wet area: tip only, X186..201.5 inside short cavity X178..206')
    print('Dry probe extends to X331.6; commercial 12 mm compression fitting space reserved')
