"""Read the current Fusion assembly and preserve its state before viewport animation.
No application activation, document opening, cloud save, mouse or keyboard use.
"""
import adsk.core, adsk.fusion, json, re
from pathlib import Path
HERE=Path('/Users/alex/Nube /repos/Cruz_prototipe/cad/fusion_m2/animacion')
WRAPPERS=('EL_PI Raspberry','EL_EZO Atlas','EL_GATE Pololu','EL_PUMP_MOTOR MOONS','PCB_V8_ESTUDIO','WetLink JPT','Tuerca M10 WetLink')
def group(name,path):
    if name.startswith('P_CHASSIS_FRONT '):return 'base'
    if name.startswith('P_CHASSIS_REAR '):return 'chassis'
    if name.startswith(('P_OPT_A ','P_OPT_B ')):return 'opt_support'
    if name.startswith(('O01 ','O03 ')):return 'optics'
    if name.startswith('O02 '):return 'optics'
    if name.startswith('O06 '):return 'optics'
    if name.startswith('O07 '):return 'optics'
    if name.startswith(('O05 ','H_CELL_')):return 'cell'
    if name.startswith('O04 '):return 'webcam'
    if name.startswith(('EL_PUMP_MOTOR','H_PUMP_')):return 'pump'
    if '03_CONDUCTIVIDAD_SOLO_PUNTA_HUMEDA:' in path:return 'ec'
    if '04_SENSOR_TEMPERATURA_Y_TEE:' in path:return 'temp'
    if name.startswith('P_TRAV216 '):return 'bridge'
    if name.startswith('M3_BRIDGE_NUT_'):return 'bridge_nuts'
    if name.startswith('M3_BRIDGE_SCREW_'):return 'bridge_screws'
    if name.startswith(('EL_EZO Atlas','P_EZO_V2 ')):return 'atlas'
    if name.startswith(('E03 ','EL_EN3 ','WetLink JPT','Tuerca M10 WetLink')):return 'rear_cap'
    if name.startswith('E05 '):return 'rear_gasket'
    if name.startswith('H2_TUBE_CELL_PUMP '):return 'upper_hose'
    if '02_MANGUERAS_INTERNAS:' in path or name.startswith('H_EXTERNAL_'):return 'hoses'
    if name.startswith('P_HOOD_UPPER '):return 'hood'
    if name.startswith('EL_PI Raspberry'):return 'pi'
    if name.startswith('EL_BAT '):return 'battery'
    if name.startswith(('P_TOP ','P_T')):return 'bare_tray'
    if name.startswith(('PCB_V8_ESTUDIO','EL_RTC ','EL_RS485 ','EL_LED_B ','EL_GATE Pololu')):return 'pcb_modules'
    if name.startswith('P_PCB_CLIP_'):return 'clips_l' if '_L ' in name else 'clips_r'
    if name.startswith('E01 '):return 'tube'
    if re.match(r'R[1-4] ',name) or re.match(r'W[1-4]RO ',name) or re.match(r'N[1-4]R ',name):return 'rods_rear_hardware'
    if re.match(r'W[1-4]RI ',name):return 'rear_inner_washers'
    if re.match(r'S[1-4] ',name):return 'limiters'
    if re.match(r'W[1-4]FI ',name):return 'front_inner_washers'
    if name.startswith('E02 '):return 'front_cap'
    if name.startswith('E04 '):return 'front_gasket'
    if re.match(r'W[1-4]FO ',name) or re.match(r'N[1-4]F ',name):return 'front_hardware'
    if '07_LASTRE:' in path:return 'ballast_front' if name.startswith(('P_C40_','B52 ')) else 'ballast_rear'
    raise RuntimeError('Unassigned component: '+path)
def run(_context):
    app=adsk.core.Application.get();d=adsk.fusion.Design.cast(app.activeDocument.products.itemByProductType('DesignProductType'))
    assert app.activeDocument.name.startswith('Cross_M2_horizontal_design')
    root=d.rootComponent;all_occ=list(root.allOccurrences)
    rows=[];all_state=[]
    for o in all_occ:
        all_state.append({'path':o.fullPathName,'matrix':list(o.transform2.asArray()),'visible':o.isLightBulbOn,'grounded':o.isGroundToParent})
        if o.component.name.startswith('EL_PI_PLUG_SPACE '):continue
        segments=o.fullPathName.split('+')
        if any(any(seg.startswith(p) for p in WRAPPERS) for seg in segments[:-1]):continue
        wrapper=o.component.name.startswith(WRAPPERS)
        if not wrapper and not any(b.isSolid for b in o.bRepBodies):continue
        key=group(o.component.name,o.fullPathName)
        rows.append({'path':o.fullPathName,'name':o.component.name,'group':key,'matrix':list(o.transform2.asArray()),'visible':o.isLightBulbOn,'grounded':o.isGroundToParent})
    camera=app.activeViewport.camera
    state={'document':app.activeDocument.name,'occurrences':all_state,'motion':rows,
           'camera':{'eye':list(camera.eye.asArray()),'target':list(camera.target.asArray()),'up':list(camera.upVector.asArray()),'extents':camera.viewExtents,'type':int(camera.cameraType)},
           'body_signature':[{'path':o.fullPathName,'name':b.name,'volume':b.volume,'min':list(b.boundingBox.minPoint.asArray()),'max':list(b.boundingBox.maxPoint.asArray())} for o in all_occ for b in o.bRepBodies if b.isSolid],
           'initial_body_count':sum(o.bRepBodies.count for o in all_occ)}
    (HERE/'ESTADO_ANTES_ANIMACION.json').write_text(json.dumps(state,indent=2))
    assert d.exportManager.execute(d.exportManager.createFusionArchiveExportOptions(str(HERE.parent/'CROSS_MONTAJE_ACCESIBLE_2026-11-03.f3d')))
    print(json.dumps({'moving_occurrences':len(rows),'groups':sorted(set(r['group'] for r in rows)),'bodies':state['initial_body_count']}))
