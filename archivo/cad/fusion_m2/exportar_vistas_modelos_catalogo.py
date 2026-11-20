"""Export the complete assembly and native viewport; never save the cloud document.
The two inspection closeups were captured separately with covers hidden.
"""
import adsk.core, adsk.fusion, json
BASE='/Users/alex/Nube /repos/Cruz_prototipe/archivo/cad/fusion_m2/'
def run(_context):
    app=adsk.core.Application.get();d=adsk.fusion.Design.cast(app.activeProduct)
    root=d.rootComponent;d.activateRootComponent();vp=app.activeViewport
    d.analyses.isLightBulbOn=False
    groups={o.component.name:o for o in root.occurrences.item(0).childOccurrences}
    for name in ['01_CARCASA_Y_TAPAS','02_VARILLAS_Y_CIERRES','07_LASTRE']:groups[name].isLightBulbOn=True
    for o in root.allOccurrences:
        if o.component.name.startswith(('P_TOP ','EL_BAT ','PCB_V8_ESTUDIO')):o.isLightBulbOn=True
    c=vp.camera;c.cameraType=adsk.core.CameraTypes.OrthographicCameraType
    c.eye=adsk.core.Point3D.create(-12,-35,30);c.target=adsk.core.Point3D.create(19,0,0);c.upVector=adsk.core.Vector3D.create(0,0,1)
    c.isFitView=False;c.isSmoothTransition=False;c.viewExtents=62
    vp.camera=c;vp.refresh();adsk.doEvents();vp.camera=c;vp.refresh();adsk.doEvents()
    assert vp.saveAsImageFile(BASE+'STEP_MONTAJE_CATALOGO_2026-11-03.png',1800,1100)
    filename=BASE+'CROSS_MODELOS_CATALOGO_2026-11-03.f3d'
    assert d.exportManager.execute(d.exportManager.createFusionArchiveExportOptions(filename))
    problems=[];states={};count=0
    def inspect(item):
        nonlocal count
        group=adsk.fusion.TimelineGroup.cast(item)
        if group:
            for j in range(group.count):inspect(group.item(j))
            return
        count+=1;state=int(item.healthState);states[state]=states.get(state,0)+1
        if item.healthState in [adsk.fusion.FeatureHealthStates.WarningFeatureHealthState,adsk.fusion.FeatureHealthStates.ErrorFeatureHealthState]:
            problems.append({'name':item.name,'message':item.errorOrWarningMessage,'state':state})
    for i in range(d.timeline.count):inspect(d.timeline.item(i))
    counts={'occurrences':root.allOccurrences.count,'brep_bodies':sum(o.bRepBodies.count for o in root.allOccurrences),
        'timeline_leaf_items_checked':count,'timeline_health_states':states,'timeline_warnings_or_errors':problems,
        'export':filename,'cloud_document_saved':False}
    with open(BASE+'EXPORTACION_MODELOS_CATALOGO_2026-11-03.json','w') as f:json.dump(counts,f,indent=2)
    print(json.dumps(counts))
