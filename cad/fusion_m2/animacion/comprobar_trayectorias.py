"""Check sampled assembly paths against previously installed modeled solids.
Catalog internal overlaps are outside this check: moving subassemblies stay intact.
"""
import adsk.core, adsk.fusion, json, hashlib
from pathlib import Path
HERE=Path('/Users/alex/Nube /repos/Cruz_prototipe/cad/fusion_m2/animacion')
def run(_context):
    app=adsk.core.Application.get();d=adsk.fusion.Design.cast(app.activeDocument.products.itemByProductType('DesignProductType'))
    state=json.loads((HERE/'ESTADO_ANTES_ANIMACION.json').read_text(encoding='utf-8'));plan=json.loads((HERE/'PLAN_MONTAJE.json').read_text(encoding='utf-8'))
    tmp=adsk.fusion.TemporaryBRepManager.get();all_occ=list(d.rootComponent.allOccurrences);groups={}
    # Cache recorded world bounds; repeated exact boundingBox evaluation dominates runtime.
    bounds={(r['path'],r['name']):(r['min'],r['max']) for r in state['body_signature']}
    for r in state['motion']:
        lst=groups.setdefault(r['group'],[])
        for o in all_occ:
            if o.fullPathName==r['path'] or o.fullPathName.startswith(r['path']+'+'):
                for b in o.bRepBodies:
                    if b.isSolid:lst.append((o.component.name,b,bounds[(o.fullPathName,b.name)]))
    completed={'base'};hits=[];tests=0
    for step in plan['steps']:
        for g,delta in step['moves'].items():
            if not any(delta):continue
            for fraction in [.15,.5,.85]:
                m=adsk.core.Matrix3D.create();m.translation=adsk.core.Vector3D.create(*(v*(1-fraction)/10 for v in delta))
                for name,body,bb in groups[g]:
                    shift=[v*(1-fraction)/10 for v in delta]
                    lo=[a+b for a,b in zip(bb[0],shift)];hi=[a+b for a,b in zip(bb[1],shift)]
                    moved=None
                    for prev in completed:
                        for other,stationary,sbb in groups[prev]:
                            if any(min(hi[i],sbb[1][i])-max(lo[i],sbb[0][i])<=1e-7 for i in range(3)):continue
                            if g=='tube' and max(abs(sbb[0][1]),abs(sbb[1][1]))**2+max(abs(sbb[0][2]),abs(sbb[1][2]))**2<8.5**2:continue
                            if moved is None:
                                moved=tmp.copy(body);assert tmp.transform(moved,m)
                            tests+=1;hit=tmp.copy(moved)
                            assert tmp.booleanOperation(hit,tmp.copy(stationary),adsk.fusion.BooleanTypes.IntersectionBooleanType)
                            if hit.volume>1e-5:hits.append({'step':step['number'],'fraction':fraction,'moving':name,'stationary':other,'cm3':hit.volume})
        completed.update(step['moves'])
        (HERE/'PROGRESO_COMPROBACION.json').write_text(json.dumps({'last_step':step['number'],'boolean_tests':tests,'hits':len(hits)}))
    report={'plan_sha256':hashlib.sha256((HERE/'PLAN_MONTAJE.json').read_bytes()).hexdigest(),'sampled_progress':[.15,.5,.85],'boolean_tests':tests,'hits':hits,'limit':'Discrete samples, modeled solids only. Flexible cables/tubes, tools, hand clearance, tolerances and continuous swept volumes are not validated.'}
    (HERE/'TRAYECTORIAS_MUESTREADAS.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report))
