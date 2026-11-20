"""Revised hose layout after the pump displacement; all dimensions in mm."""
import adsk.core, adsk.fusion, math, json

def run(_context):
    d=adsk.fusion.Design.cast(adsk.core.Application.get().activeProduct)
    root=d.rootComponent
    parent=next(o for o in root.allOccurrences if o.component.name=='02_MANGUERAS_INTERNAS').component
    groups={'06':parent}
    I=adsk.core.Matrix3D.create
    P=lambda x,y,z: adsk.core.Point3D.create(x/10,y/10,z/10)
    p={'tube_hose':{'od':5,'id':3}}
    colors={'glass':d.appearances.itemByName('Glass (Clear)')}
    manifest=[]
    routes=[
      ('H3_TUBE_IN','Entrada a temperatura - canal en travesano','X',[(374,-35,35),(321,-35,35),(321,25,35),(321,25,-14)]),
      ('H3_TUBE_TEMP_EC','Temperatura a conductividad - circuito completo','Z',[(321,25,-46),(321,25,-72),(365,-9,-72),(365,-9,-46),(345,-9,-46)]),
      
      ('H3_TUBE_OUT','Bomba a descarga - canal en travesano','Z',[(280,32,19),(280,32,35),(310,35,35),(374,35,35)])]
    for code,name,axis,points in routes:
        occ = groups['06'].occurrences.addNewComponent(I())
        c = occ.component; c.name = code+' '+name
        sketch = c.sketches.add(c.xYConstructionPlane)
        sketch.name = '3D hydraulic centerline with tangent circular bends'
        def minus(a,b): return [a[i]-b[i] for i in range(3)]
        def norm(a): return math.sqrt(sum(v*v for v in a))
        def unit(a): return [v/norm(a) for v in a]
        corners = []
        for i in range(1,len(points)-1):
            u = unit(minus(points[i-1],points[i]))
            v = unit(minus(points[i+1],points[i]))
            angle = math.acos(max(-1,min(1,sum(a*b for a,b in zip(u,v)))))
            corners.append({'u':u,'v':v,'angle':angle,'d':15/math.tan(angle/2)})
        for i in range(len(points)-1):
            left = corners[i-1]['d'] if i else 0
            right = corners[i]['d'] if i<len(corners) else 0
            available = .95*norm(minus(points[i+1],points[i]))
            if left+right > available:
                factor = available/(left+right)
                if i: corners[i-1]['d'] *= factor
                if i<len(corners): corners[i]['d'] *= factor
        curves = adsk.core.ObjectCollection.create()
        previous = points[0]
        radii = []
        for i,corner in enumerate(corners,1):
            u,v,angle,dist = corner['u'],corner['v'],corner['angle'],corner['d']
            first = [points[i][j]+u[j]*dist for j in range(3)]
            last = [points[i][j]+v[j]*dist for j in range(3)]
            bisector = unit([u[j]+v[j] for j in range(3)])
            radius = dist*math.tan(angle/2)
            assert radius > p['tube_hose']['od']/2+0.5, (code,'Bend too tight',radius)
            radii.append(round(radius,3))
            center = [points[i][j]+bisector[j]*dist/math.cos(angle/2) for j in range(3)]
            middle = [center[j]-bisector[j]*radius for j in range(3)]
            if norm(minus(first,previous)) > .001:
                curves.add(sketch.sketchCurves.sketchLines.addByTwoPoints(P(*previous),P(*first)))
            curves.add(sketch.sketchCurves.sketchArcs.addByThreePoints(P(*first),P(*middle),P(*last)))
            previous = last
        curves.add(sketch.sketchCurves.sketchLines.addByTwoPoints(P(*previous),P(*points[-1])))
        path = c.features.createPath(curves, False)
        plane_input = c.constructionPlanes.createInput()
        basis = c.yZConstructionPlane if axis=='X' else c.xYConstructionPlane
        value = points[0][0] if axis=='X' else points[0][2]
        assert plane_input.setByOffset(basis,adsk.core.ValueInput.createByReal(value/10))
        plane = c.constructionPlanes.add(plane_input)
        section = c.sketches.add(plane)
        center = section.modelToSketchSpace(P(*points[0]))
        for radius in (p['tube_hose']['od']/20,p['tube_hose']['id']/20):
            section.sketchCurves.sketchCircles.addByCenterRadius(center,radius)
        profile = next(pr for pr in section.profiles if pr.profileLoops.count==2)
        sweep = c.features.sweepFeatures.add(c.features.sweepFeatures.createInput(profile,path,adsk.fusion.FeatureOperations.NewBodyFeatureOperation))
        body = sweep.bodies.item(0); body.name = c.name
        body.appearance = colors['glass']; body.opacity=.65
        sketch.isLightBulbOn = False; section.isLightBulbOn = False; plane.isLightBulbOn = False
        bb = body.boundingBox
        manifest.append({'code':code,'name':name,'group':'06','status':'ROUTE_PROPOSAL_BEND_RADIUS_UNVERIFIED','printed':False,'bbox_mm':[round(10*(getattr(bb.maxPoint,k)-getattr(bb.minPoint,k)),3) for k in 'xyz'],'volume_cm3':round(body.volume,4),'centerline_points_mm':points,'bend_radii_mm':radii})
        c.attributes.add('cruz_m2','status','ROUTE_PROPOSAL_BEND_RADIUS_UNVERIFIED')

    for prefix in ['H2_TUBE_IN ','H2_TUBE_TEMP_EC ','H2_TUBE_OUT ']:
        old=next(o for o in root.allOccurrences if o.component.name.startswith(prefix))
        old.isLightBulbOn=False
        old.component.attributes.add('assembly_adjustment','superseded','H2 hose route')
    for entry in manifest: print(entry['code'],entry['bend_radii_mm'])
    with open('/Users/alex/Nube /repos/Cruz_prototipe/archivo/cad/fusion_m2/RECORRIDOS_MANGUERAS_V3.json','w') as f:json.dump(manifest,f,indent=2)
