"""Full active-assembly interference review, preserving catalog provenance.
Fusion interference results may return native bodies: classify by native
component attributes, never by entityToken string equality.
"""
import adsk.core, adsk.fusion, json, collections
BASE='/Users/alex/Nube /repos/Cruz_prototipe'
def run(_context):
    app=adsk.core.Application.get();d=adsk.fusion.Design.cast(app.activeProduct)
    objects=adsk.core.ObjectCollection.create();nonsolids=0;omitted=[]
    for o in d.rootComponent.allOccurrences:
        for b in o.bRepBodies:
            if not b.isSolid:nonsolids+=1;continue
            if o.component.name.startswith('EL_PI_PLUG_SPACE '):
                omitted.append(o.component.name);continue
            objects.add(b)
    inp=d.createInterferenceInput(objects);inp.areCoincidentFacesIncluded=False
    results=d.analyzeInterference(inp)
    def desc(b):
        c=b.parentComponent;a=c.attributes.itemByName('cad_provenance','owner')
        return {'component':c.name,'body':b.name,'owner':a.value if a else None}
    rows=[]
    for hit in results:
        if hit.interferenceBody.volume<.000001:continue
        a=desc(hit.entityOne);b=desc(hit.entityTwo)
        owners={a['owner'],b['owner']};names=[a['component'],b['component']]
        cls='UNEXPLAINED_EXTERNAL'
        if a['owner'] and a['owner']==b['owner']:
            cls='INTERNAL_CATALOG_GEOMETRY'
        elif owners=={'WETLINK_JPT','WETLINK_NUT'}:
            cls='CATALOG_MATING_THREADS'
        elif any(n.startswith('R') and 'M8 A4 threaded' in n for n in names) and any(n.startswith('N') and 'M8 closed' in n for n in names):
            cls='SIMPLIFIED_M8_THREADS'
        elif 'MOONS_MS11HS5_FAMILY' in owners and any(n.startswith('H_PUMP_HEAD ') for n in names):
            cls='PROVISIONAL_MOTOR_HEAD_COUPLING'
        elif 'WETLINK_JPT' in owners and any(n.startswith('H_EXTERNAL_') for n in names):
            cls='CATALOG_BORE_CLOSED_VS_CONTINUOUS_TUBE'
        bb=hit.interferenceBody.boundingBox
        rows.append({'a':a,'b':b,'volume_cm3':hit.interferenceBody.volume,'classification':cls,'bbox_mm':[v*10 for v in [*bb.minPoint.asArray(),*bb.maxPoint.asArray()]]})
    counts=dict(collections.Counter(r['classification'] for r in rows))
    report={'date':'2026-11-03','document':app.activeDocument.name,
        'scope':'Modeled solids only, not physical fit or pressure validation. Exact camera/head, carrier revision and custom motor dimensions remain unverified.',
        'solid_bodies_checked':objects.count,'nonphysical_clearance_omitted':omitted,'nonsolid_bodies_omitted':nonsolids,
        'classification_counts':counts,'unexplained_external_count':counts.get('UNEXPLAINED_EXTERNAL',0),
        'notes':['Catalog CAD includes pins embedded in PCBs and overlapping package details.',
                 'Two WetLink public catalog bodies have a closed internal bore where the continuous 5mm-OD tube is represented. Original CAD retained; this is not clearance approval.',
                 'MOONS family shaft/pilot overlaps the unverified pump-head reserve. Coupling dimensions must be measured.',
                 'No pressure, optical, electrical, hose bending-radius, thermal or tolerance validation is implied.'],
        'intersections':rows}
    with open(BASE+'/cad/fusion_m2/COMPROBACION_MODELOS_CATALOGO_2026-11-03.json','w') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k!='intersections'}))
    for r in rows:
        if r['classification']=='UNEXPLAINED_EXTERNAL':print(json.dumps(r))
