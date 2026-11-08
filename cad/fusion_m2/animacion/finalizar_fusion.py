"""Verify restored assembly poses and export the proposed revision. No cloud save."""
import adsk.core,adsk.fusion,json
from pathlib import Path
H=Path('/Users/alex/Nube /repos/Cruz_prototipe/cad/fusion_m2/animacion')
def run(_context):
 a=adsk.core.Application.get();d=adsk.fusion.Design.cast(a.activeDocument.products.itemByProductType('DesignProductType'));s=json.loads((H/'ESTADO_ANTES_ANIMACION.json').read_text(encoding='utf-8'));os={o.fullPathName:o for o in d.rootComponent.allOccurrences};errors=[]
 for r in s['motion']:
  o=os[r['path']];err=max(abs(x-y) for x,y in zip(r['matrix'],o.transform2.asArray()))
  if err>1e-7 or o.isLightBulbOn!=r['visible'] or o.isGroundToParent!=r['grounded']:errors.append(r['path'])
 assert not errors,errors
 count=sum(o.bRepBodies.count for o in os.values());assert count==s['initial_body_count']==335
 for r in s['motion']:
  if r['group'] in ['base','chassis']:assert abs(os[r['path']].component.opacity-1)<1e-6
 assert d.activateRootComponent()
 vp=a.activeViewport;c=vp.camera;c.cameraType=adsk.core.CameraTypes.OrthographicCameraType;c.isSmoothTransition=False;c.isFitView=False
 c.eye=adsk.core.Point3D.create(-12,-35,30);c.target=adsk.core.Point3D.create(19,0,0);c.upVector=adsk.core.Vector3D.create(0,0,1);c.viewExtents=39;vp.camera=c;vp.refresh();adsk.doEvents()
 archive=H.parent/'CROSS_MONTAJE_ACCESIBLE_2026-11-03.f3d';assert d.exportManager.execute(d.exportManager.createFusionArchiveExportOptions(str(archive)))
 warnings=[];visited=[]
 def inspect(t):
  if t.isGroup:
   group=adsk.fusion.TimelineGroup.cast(t)
   for j in range(group.count):inspect(group.item(j))
  else:
   visited.append(t.name)
   if t.healthState in [adsk.fusion.FeatureHealthStates.WarningFeatureHealthState,adsk.fusion.FeatureHealthStates.ErrorFeatureHealthState]:warnings.append({'name':t.name,'message':t.errorOrWarningMessage})
 for i in range(d.timeline.count):inspect(d.timeline.item(i))

 report={'document':a.activeDocument.name,'verified_occurrence_poses':len(s['motion']),'bodies':count,'camera':'assembled isometric','cloud_saved':False,'archive':str(archive),'timeline_feature_count':len(visited),'timeline_issues':warnings}
 (H/'ESTADO_FINAL_VERIFICADO.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))
