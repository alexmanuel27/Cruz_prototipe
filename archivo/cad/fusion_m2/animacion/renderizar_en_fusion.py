"""Render actual Fusion viewport frames without mouse, keyboard or window activation.
Each batch restores the assembly and camera in a finally block. No cloud save.
"""
import adsk.core, adsk.fusion, json
from pathlib import Path
HERE=Path('/Users/alex/Nube /repos/Cruz_prototipe/archivo/cad/fusion_m2/animacion')
BATCH_START = 0
BATCH_END = 1

def run(_context):
    app=adsk.core.Application.get();d=adsk.fusion.Design.cast(app.activeDocument.products.itemByProductType('DesignProductType'))
    original=json.loads((HERE/'ESTADO_ANTES_ANIMACION.json').read_text(encoding='utf-8'))
    plan=json.loads((HERE/'PLAN_MONTAJE.json').read_text(encoding='utf-8'))
    assert app.activeDocument.name==original['document']
    by_path={o.fullPathName:o for o in d.rootComponent.allOccurrences}
    assert all(r['path'] in by_path for r in original['motion'])
    context=[by_path[r['path']].component for r in original['motion'] if r['group'] in ['base','chassis']]
    opacity=[(c,c.opacity) for c in context]
    P=adsk.core.Point3D.create;V=adsk.core.Vector3D.create;M=adsk.core.Matrix3D.create
    vp=app.activeViewport;frames=HERE/'frames';frames.mkdir(exist_ok=True)
    def matrix(values):
        m=M();assert m.setWithArray(values);return m
    def pose(r,delta,visible):
        o=by_path[r['path']]
        if o.isLightBulbOn!=visible:o.isLightBulbOn=visible
        if visible:
            if o.isGroundToParent:o.isGroundToParent=False
            m=matrix(r['matrix']);t=m.translation;t.x+=delta[0]/10;t.y+=delta[1]/10;t.z+=delta[2]/10;m.translation=t
            if max(abs(a-b) for a,b in zip(o.transform2.asArray(),m.asArray()))>1e-8:o.transform2=m
    def restore():
        for c,value in opacity:
            if c.opacity!=value:c.opacity=value
        for r in original['motion']:
            o=by_path[r['path']]
            if max(abs(a-b) for a,b in zip(o.transform2.asArray(),r['matrix']))>1e-8:
                if o.isGroundToParent:o.isGroundToParent=False
                o.transform2=matrix(r['matrix'])
            if o.isLightBulbOn!=r['visible']:o.isLightBulbOn=r['visible']
            if o.isGroundToParent!=r['grounded']:o.isGroundToParent=r['grounded']
        c=vp.camera;rec=original['camera'];c.isSmoothTransition=False;c.isFitView=False;c.cameraType=rec['type']
        c.eye=P(*rec['eye']);c.target=P(*rec['target']);c.upVector=V(*rec['up']);c.viewExtents=rec['extents'];vp.camera=c;vp.refresh();adsk.doEvents()
    def save(idx):
        vp.refresh();adsk.doEvents();vp.refresh()
        assert vp.saveAsImageFile(str(frames/('%04d.png'%idx)),1920,864)
    try:
        assert d.activateRootComponent()
        app.userInterface.activeSelections.clear()
        c=vp.camera;c.cameraType=adsk.core.CameraTypes.OrthographicCameraType;c.isSmoothTransition=False;c.isFitView=False
        c.eye=P(-12,-35,30);c.target=P(19,0,0);c.upVector=V(0,0,1);c.viewExtents=39
        vp.camera=c;vp.refresh();adsk.doEvents();vp.camera=c;vp.refresh();adsk.doEvents()
        for idx in range(BATCH_START,min(BATCH_END,plan['frame_count'])):
            if idx==0:
                for c,value in opacity:
                    if c.opacity!=value:c.opacity=value
                for r in original['motion']:pose(r,[0,0,0],r['visible'])
            else:
                step=next(s for s in plan['steps'] if s['first_frame']<=idx<s['first_frame']+s['render_count'])
                for c,value in opacity:
                    desired=.22 if step['number'] in [2,3] else value
                    if abs(c.opacity-desired)>1e-6:c.opacity=desired
                mounted={'base'}|{g for s in plan['steps'][:step['number']-1] for g in s['moves']}
                t=(idx-step['first_frame'])/max(1,step['render_count']-1);smooth=t*t*(3-2*t)
                for r in original['motion']:
                    g=r['group'];visible=g in mounted or g in step['moves']
                    delta=[v*(1-smooth) for v in step['moves'].get(g,[0,0,0])]
                    if g in step.get('waypoints',{}):
                        pts=step['waypoints'][g];u=smooth*(len(pts)-1);j=min(int(u),len(pts)-2);f=u-j
                        delta=[a*(1-f)+b*f for a,b in zip(pts[j],pts[j+1])]
                    # Flexible tubing appears in its routed shape: no fictitious rigid insertion.
                    if g in ['hoses','upper_hose'] and g in step['moves']:visible=t>=.25
                    pose(r,delta,visible)
            save(idx)
        print('Rendered frames',BATCH_START,'through',min(BATCH_END,plan['frame_count'])-1)
    finally:
        restore()
        print('Original occurrence positions, visibility and camera restored.')
