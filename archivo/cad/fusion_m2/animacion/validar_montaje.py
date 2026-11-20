"""Bounded sampled assembly clearance verification with cached bounds."""
import adsk.core,adsk.fusion,json,time,math
from pathlib import Path
HERE=Path('/Users/alex/Nube /repos/Cruz_prototipe/archivo/cad/fusion_m2/animacion')
ONLY=[]
def run(_context):
 app=adsk.core.Application.get();d=adsk.fusion.Design.cast(app.activeDocument.products.itemByProductType('DesignProductType'))
 state=json.loads((HERE/'ESTADO_ANTES_ANIMACION.json').read_text(encoding='utf-8'));plan=json.loads((HERE/'PLAN_MONTAJE.json').read_text(encoding='utf-8'));tmp=adsk.fusion.TemporaryBRepManager.get()
 bounds={(r['path'],r['name']):(r['min'],r['max']) for r in state['body_signature']};groups={};all_o=list(d.rootComponent.allOccurrences)
 for r in state['motion']:
  lst=groups.setdefault(r['group'],[])
  for o in all_o:
   if o.fullPathName==r['path'] or o.fullPathName.startswith(r['path']+'+'):
    for b in o.bRepBodies:
     if b.isSolid:lst.append((o.component.name,b,bounds[(o.fullPathName,b.name)]))
 start=time.monotonic();tests=0;results=[];done={'base'}
 for step in plan['steps']:
  if ONLY and step['number'] not in ONLY:done.update(step['moves']);continue
  hits=[];complete=True
  for g,delta in step['moves'].items():
   if g in ['hoses','upper_hose']:continue
   for f in [.05,.2,.4,.6,.8,.95,1.0]:
    shift=[v*(1-f)/10 for v in delta]
    if g in step.get('waypoints',{}):
     pts=step['waypoints'][g];u=f*(len(pts)-1);j=min(int(u),len(pts)-2);v=u-j;shift=[(a*(1-v)+b*v)/10 for a,b in zip(pts[j],pts[j+1])]
    m=adsk.core.Matrix3D.create();m.translation=adsk.core.Vector3D.create(*shift)
    for name,b,bb in groups[g]:
     if b.name.startswith('EL_PI_PLUG_SPACE'):continue
     lo=[a+c for a,c in zip(bb[0],shift)];hi=[a+c for a,c in zip(bb[1],shift)];moving=None
     for staticgroup in sorted(done):
      for other,static,sbb in groups[staticgroup]:
       if any(min(hi[i],sbb[1][i])-max(lo[i],sbb[0][i])<=1e-7 for i in range(3)):continue
       # Tube is annular: solids strictly inside its bore cannot intersect it.
       if g=='tube' and max(abs(sbb[k][1]) for k in [0,1])**2+max(abs(sbb[k][2]) for k in [0,1])**2<8.499**2:continue
       if time.monotonic()-start>155:complete=False;break
       if moving is None:moving=tmp.copy(b);assert tmp.transform(moving,m)
       inter=tmp.copy(moving);assert tmp.booleanOperation(inter,tmp.copy(static),adsk.fusion.BooleanTypes.IntersectionBooleanType);tests+=1
       if inter.volume>1e-5:
        hits.append({'group':g,'moving':name,'stationary':other,'stationary_group':staticgroup,'fraction':f,'cm3':inter.volume});break
      if hits or not complete:break
     if hits or not complete:break
    if hits or not complete:break
   if hits or not complete:break
  results.append({'step':step['number'],'title':step['title'],'complete':complete,'hits':hits})
  (HERE/'VALIDACION_MONTAJE.json').write_text(json.dumps({'seconds':time.monotonic()-start,'tests':tests,'results':results},indent=2,ensure_ascii=True))
  if not complete:break
  done.update(step['moves'])
 print(json.dumps({'seconds':time.monotonic()-start,'tests':tests,'steps':len(results),'collisions':[r for r in results if r['hits']],'complete':complete},ensure_ascii=True))
