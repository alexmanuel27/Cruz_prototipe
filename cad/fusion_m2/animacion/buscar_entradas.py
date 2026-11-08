"""Bounded route search using cached world bounds, never repeated exact boundingBox calls."""
import adsk.core, adsk.fusion, json, time
from pathlib import Path
HERE=Path('/Users/alex/Nube /repos/Cruz_prototipe/cad/fusion_m2/animacion')
def run(_context):
 app=adsk.core.Application.get();d=adsk.fusion.Design.cast(app.activeDocument.products.itemByProductType('DesignProductType'))
 state=json.loads((HERE/'ESTADO_ANTES_ANIMACION.json').read_text(encoding='utf-8'));plan=json.loads((HERE/'PLAN_MONTAJE.json').read_text(encoding='utf-8'))
 bounds={(r['path'],r['name']):(r['min'],r['max']) for r in state['body_signature']};tmp=adsk.fusion.TemporaryBRepManager.get();groups={};all_o=list(d.rootComponent.allOccurrences)
 for r in state['motion']:
  lst=groups.setdefault(r['group'],[])
  for o in all_o:
   if o.fullPathName==r['path'] or o.fullPathName.startswith(r['path']+'+'):
    for b in o.bRepBodies:
     if b.isSolid:lst.append((o.component.name,b,bounds[(o.fullPathName,b.name)]))
 cases={'sensors':[[240,0,0],[-400,0,0],[0,0,105]],'optics':[[-300,0,0],[350,0,0],[0,0,100]],'hood_pi':[[-300,0,0],[350,0,0],[0,0,80]],'tray':[[260,0,0],[-400,0,0],[0,0,135]]}
 report=[];start=time.monotonic();tests=0
 for wanted,vectors in cases.items():
  done={'base'}
  for step in plan['steps']:
   if wanted in step['moves']:break
   done.update(step['moves'])
  for delta in vectors:
   hit=None;complete=True
   for f in [.1,.3,.5,.7,.9,.97]:
    shift=[v*(1-f)/10 for v in delta];m=adsk.core.Matrix3D.create();m.translation=adsk.core.Vector3D.create(*shift)
    for name,b,bb in groups[wanted]:
     lo=[a+c for a,c in zip(bb[0],shift)];hi=[a+c for a,c in zip(bb[1],shift)];moving=None
     for g in done:
      for other,static,sbb in groups[g]:
       if any(min(hi[i],sbb[1][i])-max(lo[i],sbb[0][i])<=1e-7 for i in range(3)):continue
       if time.monotonic()-start>150:complete=False;break
       if moving is None:moving=tmp.copy(b);assert tmp.transform(moving,m)
       intersection=tmp.copy(moving);assert tmp.booleanOperation(intersection,tmp.copy(static),adsk.fusion.BooleanTypes.IntersectionBooleanType);tests+=1
       if intersection.volume>1e-5:
        hit={'moving':name,'stationary':other,'fraction':f,'cm3':intersection.volume};break
      if hit or not complete:break
     if hit or not complete:break
    if hit or not complete:break
   report.append({'group':wanted,'delta_mm':delta,'complete':complete,'hit':hit})
   (HERE/'ENTRADAS_CANDIDATAS.json').write_text(json.dumps({'tests':tests,'results':report},indent=2))
   if not complete:print(json.dumps({'tests':tests,'results':report}));return
 print(json.dumps({'tests':tests,'results':report}))
