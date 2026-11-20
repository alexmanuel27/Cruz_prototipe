import adsk.core,adsk.fusion,json
from pathlib import Path
HERE=Path('/Users/alex/Nube /repos/Cruz_prototipe/archivo/cad/fusion_m2/animacion')
def run(_context):
 a=adsk.core.Application.get();d=adsk.fusion.Design.cast(a.activeDocument.products.itemByProductType('DesignProductType'));tmp=adsk.fusion.TemporaryBRepManager.get();B=adsk.fusion.BooleanTypes;report=[]
 def box(x,y,z,w,h,t):return tmp.createBox(adsk.core.OrientedBoundingBox3D.create(adsk.core.Point3D.create(x/10,y/10,z/10),adsk.core.Vector3D.create(1,0,0),adsk.core.Vector3D.create(0,1,0),w/10,h/10,t/10))
 changes=[('P_CHASSIS_REAR ',[(251.6,32,-5.5,5.8,17,91.6),(341.5,-79.8,-6.1,3.8,3.2,1.4),(349.5,25,-43,63,6.6,6.6)]),('P_TOP ',[(379,0,48,14.2,130,30)])]
 for prefix,cuts in changes:
  c=next(o.component for o in d.rootComponent.allOccurrences if o.component.name.startswith(prefix));b=tmp.copy(c.bRepBodies.item(0));old=b.volume
  for args in cuts:assert tmp.booleanOperation(b,box(*args),B.DifferenceBooleanType)
  f=c.features.baseFeatures.item(0);assert f.startEdit();assert f.updateBody(f.bodies.item(0),b);assert f.finishEdit();report.append({'part':c.name,'removed_cm3':old-b.volume})
 (HERE/'AFINADO_ACCESOS.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
