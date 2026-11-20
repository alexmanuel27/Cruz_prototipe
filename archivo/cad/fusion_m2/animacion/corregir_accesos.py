"""Reversible assembly access revision; original F3D retained, no cloud save."""
import adsk.core,adsk.fusion,json,math
from pathlib import Path
HERE=Path('/Users/alex/Nube /repos/Cruz_prototipe/archivo/cad/fusion_m2/animacion')
def run(_context):
 app=adsk.core.Application.get();d=adsk.fusion.Design.cast(app.activeDocument.products.itemByProductType('DesignProductType'));root=d.rootComponent
 assert not any(o.component.name.startswith('P_TRAV216 ') for o in root.allOccurrences),'Revision already installed'
 tmp=adsk.fusion.TemporaryBRepManager.get();B=adsk.fusion.BooleanTypes
 def p(x,y,z):return adsk.core.Point3D.create(x/10,y/10,z/10)
 def box(x,y,z,w,h,t,angle=0):
  return tmp.createBox(adsk.core.OrientedBoundingBox3D.create(p(x,y,z),adsk.core.Vector3D.create(math.cos(angle),math.sin(angle),0),adsk.core.Vector3D.create(-math.sin(angle),math.cos(angle),0),w/10,h/10,t/10))
 def cyl(x,y,z0,z1,r0,r1=None):return tmp.createCylinderOrCone(p(x,y,z0),r0/10,p(x,y,z1),(r0 if r1 is None else r1)/10)
 def boolean(a,b,kind):assert tmp.booleanOperation(a,b,kind);return a
 def diff(a,b):return boolean(a,b,B.DifferenceBooleanType)
 def union(a,b):return boolean(a,b,B.UnionBooleanType)
 def comp(prefix):return next(o.component for o in root.allOccurrences if o.component.name.startswith(prefix))
 front=comp('P_CHASSIS_FRONT ');rear=comp('P_CHASSIS_REAR ')
 targets=[];report=[]
 channel=tmp.createCylinderOrCone(p(164,0,-60),1.53,p(381,0,-60),1.53)
 key=box(272.5,19,-60,217,10.6,6.6)
 beamBox=box(216,0,37,8,156,4)
 old=tmp.copy(rear.bRepBodies.item(0));beam=boolean(tmp.copy(old),tmp.copy(beamBox),B.IntersectionBooleanType)
 assert .5<beam.volume<6,beam.volume
 diff(beam,cyl(216,-70,34,40,1.7));diff(beam,cyl(216,70,34,40,1.7))
 for y in [-70,70]:diff(beam,cyl(216,y,37.7,39.1,1.7,3.1))
 for c in [front,rear]:
  body=tmp.copy(c.bRepBodies.item(0));v=body.volume
  diff(body,tmp.copy(channel));diff(body,tmp.copy(key))
  if c==rear:
   diff(body,tmp.copy(beamBox))
   for y in [-70,70]:
    diff(body,cyl(216,y,22,40,1.7));diff(body,box(215.75,y,27.3,8.1,6.4,2.6))
  targets.append((c,body));report.append({'component':c.name,'removed_cm3':v-body.volume})
 parent=next(o.component for o in root.allOccurrences if o.component.name=='01_3D_CHASIS_Y_AROS')
 def add(name,body,appearance):
  o=parent.occurrences.addNewComponent(adsk.core.Matrix3D.create());c=o.component;c.name=name
  f=c.features.baseFeatures.add();f.name='Acceso de montaje 2026-11-03';assert f.startEdit();b=c.bRepBodies.add(body,f);assert f.finishEdit();b.name=name;b.appearance=d.appearances.itemByName(appearance)
  return o
 # Compute all temporary geometry before modifying source solids.
 hardware=[]
 for y in [-70,70]:
  screw=union(cyl(216,y,23,37.7,1.5),cyl(216,y,37.7,39,1.5,2.8))
  # Cross recess is symbolic, screw and nut threads are not modeled.
  diff(screw,box(216,y,39.1,3.4,.7,1));diff(screw,box(216,y,39.1,.7,3.4,1))
  nut=cyl(216,y,26,28.4,3.18)
  for angle in [0,math.pi/3,2*math.pi/3]:boolean(nut,box(216,y,27.2,5.5,20,2.4,angle),B.IntersectionBooleanType)
  diff(nut,cyl(216,y,25.9,28.5,1.65));hardware.extend([('M3_BRIDGE_SCREW_%s Countersunk M3x16'%y,screw),('M3_BRIDGE_NUT_%s Captive M3'%y,nut)])
 start=d.timeline.count
 for c,body in targets:
  f=c.features.baseFeatures.item(0);assert f.startEdit();assert f.updateBody(f.bodies.item(0),body);assert f.finishEdit()
 add('P_TRAV216 Removable bridge; two countersunk M3x16',beam,'M2 Teal printed ASA')
 for name,body in hardware:add(name,body,'Cruz - Inox satinado')
 if d.timeline.count>start:
  g=d.timeline.timelineGroups.add(start,d.timeline.count-1);g.name='MONTAJE - Travesano desmontable y canal axial EC'
 (HERE/'REVISION_ACCESOS.json').write_text(json.dumps({'date':'2026-11-03','changes':report,'new_printed_part':'P_TRAV216','hardware':'2 x M3x16 countersunk + 2 x M3 nuts','original_backup':'CROSS_ANTES_ANIMACION.f3d','minimum_ideal_channel_floor_mm':8.7,'status':'Proposed; print tolerances and physical assembly untested'},indent=2))
 print(json.dumps({'changes':report,'beam_cm3':beam.volume,'bodies':sum(o.bRepBodies.count for o in root.allOccurrences)}))
