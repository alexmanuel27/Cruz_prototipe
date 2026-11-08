"""Fusion geometric checks against the current approximate component envelopes."""
import adsk.core
import adsk.fusion
import json
import os
import itertools

HERE = os.path.dirname(os.path.abspath(__file__))


def run(_context: str):
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)
    assert app.activeDocument.name.startswith('Cross_M2_horizontal_design')
    top = next(o.component for o in design.rootComponent.occurrences if o.component.name == 'M2_GENERATED')
    tmp = adsk.fusion.TemporaryBRepManager.get()
    objects = {o.component.name.split(' ')[0]:o.component.bRepBodies.item(0)
               for group in top.occurrences for o in group.component.occurrences
               if o.component.bRepBodies.count}
    manifest = json.load(open(os.path.join(HERE,'manifest.json')))
    printed = [part['code'] for part in manifest['parts'] if part['printed']]
    references = [k for k in objects if k.startswith(('O','EL_','H_'))]
    hits = []

    def overlap(a,b):
        if not a.boundingBox.intersects(b.boundingBox):
            return 0
        intersection = tmp.copy(a)
        assert tmp.booleanOperation(intersection,tmp.copy(b),adsk.fusion.BooleanTypes.IntersectionBooleanType)
        return intersection.volume

    for k in printed:
        for j in references:
            volume = overlap(objects[k],objects[j])
            if volume > .0001:
                hits.append([k,j,round(volume,6)])
    ref_hits = []
    intentional_contacts = []
    allowed = [set(['O01','O02']),set(['O01','O03']),set(['EL_PI','EL_PI_PORTS'])]
    for k,j in itertools.combinations(references,2):
        volume = overlap(objects[k],objects[j])
        if volume > .0001:
            if set([k,j]) in allowed:
                intentional_contacts.append([k,j,round(volume,6),'Original detector attachment or PCB under connector'])
            else:
                ref_hits.append([k,j,round(volume,6)])
    outside = []
    for group in top.occurrences:
        if group.component.name[:2] not in ['03','04','05','06']:
            continue
        for o in group.component.occurrences:
            if not o.component.bRepBodies.count:
                continue
            key = o.component.name.split(' ')[0]
            if key in ['EL_EN3','H_INTAKE','H_DISCHARGE']:
                continue
            body = tmp.copy(o.component.bRepBodies.item(0))
            internal = tmp.createCylinderOrCone(adsk.core.Point3D.create(-.255,0,0),7,
                                               adsk.core.Point3D.create(33.255,0,0),7)
            assert tmp.booleanOperation(body,internal,adsk.fusion.BooleanTypes.DifferenceBooleanType)
            if body.volume > .0001:
                outside.append([key,round(body.volume,6)])
    disconnected = [[key,objects[key].lumps.count] for key in printed if objects[key].lumps.count != 1]
    structural_hits = []
    structural = [key for key in objects if key not in references]
    for k,j in itertools.combinations(structural,2):
        if (k.startswith('R') and j.startswith('N')) or (j.startswith('R') and k.startswith('N')):
            continue  # Rod major diameter overlaps the simplified nut minor diameter.
        volume = overlap(objects[k],objects[j])
        if volume > .0001:
            structural_hits.append([k,j,round(volume,6)])
    rods = [k for k in objects if k in ['R1','R2','R3','R4']]
    nuts = [k for k in objects if k in ['N%d%s'%(i,s) for i in range(1,5) for s in ['F','R']]]
    assert len(rods)==4 and len(nuts)==8
    assert all(body.isSolid for body in objects.values())
    report = {'document':app.activeDocument.name,'scope':'Approximate CAD envelopes only. No physical fit, electrical, optical or pressure validation.',
              'parts_checked':len(objects),'printed_parts':len(printed),'rod_count':len(rods),'closed_dome_nut_count':len(nuts),
              'printed_vs_component_intersections_cm3':hits,'component_intersections_cm3':ref_hits,
              'intentional_reference_contacts_cm3':intentional_contacts,
              'parts_outside_internal_envelope_cm3':outside,'disconnected_printed_bodies':disconnected,
              'structural_intersections_cm3':structural_hits,
              'geometric_checks_pass':not(hits or ref_hits or outside or disconnected or structural_hits)}
    with open(os.path.join(HERE,'checks.json'),'w') as output:
        json.dump(report,output,indent=2)
    print(json.dumps(report))
