"""Elastic study of a Fusion STEP ring using mm, N and MPa."""

import json, math, pathlib, sys
import gmsh
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import splu

path = pathlib.Path(sys.argv[1])
step = float(sys.argv[2])
width = float(sys.argv[3]) if len(sys.argv)>3 else 20.
output = pathlib.Path(sys.argv[4])
mode = sys.argv[5] if len(sys.argv)>5 else 'fijo'
field_path = pathlib.Path(sys.argv[6]) if len(sys.argv)>6 else None
assert mode in ('fijo', 'topes', 'topes_d')
assert field_path is None or mode == 'topes_d'
gmsh.initialize()
gmsh.option.setNumber('General.Terminal',0)
gmsh.model.occ.importShapes(str(path))
gmsh.model.occ.synchronize()
assert len(gmsh.model.getEntities(3)) == 1
rod_surfaces = {}
eye = None
rim = None
for _,tag in gmsh.model.getEntities(2):
    x,y,z = gmsh.model.occ.getCenterOfMass(2,tag)
    kind = gmsh.model.getType(2,tag)
    if kind=='Cylinder' and abs(abs(x)-101/math.sqrt(2)) < .04 and abs(abs(y)-101/math.sqrt(2)) < .04:
        rod_surfaces[tag] = (x,y)
    if kind=='Cylinder' and abs(x-103)<.02 and abs(y)<.02:
        eye = tag
    if kind=='Torus' and abs(x-103)<.02 and abs(y)<.02 and z>width*.9:
        rim = tag
assert len(rod_surfaces)==4 and eye and rim,(rod_surfaces,eye,rim)
gmsh.option.setNumber('Mesh.MeshSizeMin',step*.44)
gmsh.option.setNumber('Mesh.MeshSizeMax',step)
gmsh.option.setNumber('Mesh.MeshSizeFromCurvature',22)
gmsh.option.setNumber('Mesh.Algorithm3D',1)
gmsh.model.mesh.generate(3)
labels,coords,_ = gmsh.model.mesh.getNodes()
xyz = np.asarray(coords).reshape(-1,3)
index = np.full(int(max(labels))+1,-1,dtype=np.int64)
index[labels]=np.arange(len(labels))
t = index[gmsh.model.mesh.getElementsByType(4)[1]].reshape(-1,4)
assert np.all(t>=0) and len(t)>1000
def surface(tag):
    types, _, nodes = gmsh.model.mesh.getElements(2,tag)
    assert len(types)==1 and types[0]==2
    return index[nodes[0]].reshape(-1,3)
rod_nodes = {tag:np.unique(surface(tag)) for tag in rod_surfaces}
eyes = surface(eye)
rims = surface(rim)
gmsh.finalize()

elems_xyz = xyz[t]
deltas = elems_xyz[:,1:] - elems_xyz[:,:1]
vol = abs(np.linalg.det(deltas))/6
assert min(vol)>0
derivatives = np.linalg.inv(deltas).transpose((0,2,1))
derivatives = np.concatenate((-derivatives.sum(axis=1,keepdims=True),derivatives),axis=1)
B = np.zeros((len(t),6,12))
for i in range(4):
    gx,gy,gz=derivatives[:,i,:].T
    B[:,0,3*i]=gx
    B[:,1,3*i+1]=gy
    B[:,2,3*i+2]=gz
    B[:,3,3*i]=gy
    B[:,3,3*i+1]=gx
    B[:,4,3*i+1]=gz
    B[:,4,3*i+2]=gy
    B[:,5,3*i]=gz
    B[:,5,3*i+2]=gx
# Verify shape gradients and engineering-shear convention using a uniform strain field.
uniform = elems_xyz.copy()*0
uniform[:,:,0]=elems_xyz[:,:,0]*.001
assert np.max(abs((B @ uniform.reshape(-1,12,1)).squeeze()-np.array([.001,0,0,0,0,0])))<1e-10
E=1200.
poisson=.36
lam=E*poisson/((1+poisson)*(1-2*poisson))
mu=E/(2*(1+poisson))
D=np.zeros((6,6))
D[:3,:3]=lam+np.eye(3)*2*mu
D[3:,3:]=mu*np.eye(3)
ke = B.transpose((0,2,1)) @ D @ B * vol[:,None,None]
gdof=np.repeat(t*3,3,axis=1)+np.tile([0,1,2],4)
n=3*len(xyz)
K=coo_matrix((ke.ravel(),(np.repeat(gdof,12,axis=1).ravel(),np.tile(gdof,(1,12)).ravel())),shape=(n,n)).tocsr()
del ke

def traction(triangles, desired):
    points=xyz[triangles]
    area=np.linalg.norm(np.cross(points[:,1]-points[:,0],points[:,2]-points[:,0]),axis=1)*.5
    p=points.mean(axis=1)
    planar=p[:,:2]-[103,0]
    norms=np.linalg.norm(planar,axis=1)
    radial=planar/norms[:,None]
    w=np.maximum(radial[:,0],0)*area
    if desired[2]>0:
        vectors=np.zeros_like(p)
        vectors[:,2]=w*(desired[2]/w.sum())
    else:
        vectors=np.column_stack((radial,np.zeros(len(p)))) * w[:,None]
        vectors*=desired[0]/vectors[:,0].sum()
    result=np.zeros((len(xyz),3))
    np.add.at(result,triangles.flatten(),np.repeat(vectors/3,3,axis=0))
    return result.ravel()

def percentile(values,q,mask):
    val,weights=values[mask],vol[mask]
    ii=val.argsort()
    return float(val[ii[np.searchsorted(np.cumsum(weights[ii]),q*weights.sum())]])

centroids=elems_xyz.mean(axis=1)
eye_region=(centroids[:,0]>96) & (abs(centroids[:,1])<20)
cases=[]
diagonal=[k for k,(x,y) in rod_surfaces.items() if x*y<0]
configurations=[('4 casquillos',list(rod_surfaces)),('2 casquillos en diagonal',diagonal)]
if mode == 'topes':
    configurations.append(('2 casquillos y topes axiales',diagonal))
if mode == 'topes_d':
    configurations=[('2 casquillos y topes axiales',diagonal)]
for support, keep in configurations:
    fixed=np.unique(np.concatenate([rod_nodes[k] for k in keep]))
    blocked=(fixed[:,None]*3+np.arange(3)).ravel()
    if support.endswith('topes axiales'):
        stop_nodes=[]
        for tag in keep:
            radius=np.linalg.norm(xyz[:,:2]-rod_surfaces[tag],axis=1)
            face=(radius>=8.4) & (radius<=12.6) & ((abs(xyz[:,2])<1e-5) | (abs(xyz[:,2]-width)<1e-5))
            if mode == 'topes_d':
                outward=np.array(rod_surfaces[tag])/101
                face &= ((xyz[:,:2]-rod_surfaces[tag]) @ outward >= -9.5)
            stop_nodes.extend(np.flatnonzero(face))
        assert len(set(stop_nodes))>=30,len(stop_nodes)
        blocked=np.concatenate(((fixed[:,None]*3+np.arange(2)).ravel(), np.array(stop_nodes)*3+2))
    dofs=np.setdiff1d(np.arange(n),blocked)
    factor=splu(K[dofs][:,dofs].tocsc())
    for angle in (0,30):
        load_angle=math.radians(angle)
        f=traction(eyes,[250*math.cos(load_angle),0,0])
        if angle:
            f+=traction(rims,[0,0,250*math.sin(load_angle)])
        total=f.reshape(-1,3).sum(axis=0)
        assert abs(np.linalg.norm(total)-250)<.02 and abs(total[1])<1.
        u=np.zeros(n)
        u[dofs]=factor.solve(f[dofs])
        reaction=(K@u-f).reshape(-1,3).sum(axis=0)
        assert np.linalg.norm(reaction+total)<1e-5
        stress = ((D @ B) @ u[gdof][...,None]).squeeze()
        sx,sy,sz,txy,tyz,txz=stress.T
        vm=np.sqrt(((sx-sy)**2+(sy-sz)**2+(sz-sx)**2)/2+3*(txy**2+tyz**2+txz**2))
        disp=np.linalg.norm(u.reshape(-1,3),axis=1)
        k=int(vm.argmax())
        case={'supports':support,'inclination_deg':angle,'force_n':total.tolist(),
              'max_vm_mpa':float(vm.max()),'vm_99_mpa':percentile(vm,.99,np.ones(len(t),dtype=bool)),
              'max_eye_mpa':float(vm[eye_region].max()),'eye_995_mpa':percentile(vm,.995,eye_region),
              'max_disp_mm':float(disp.max()),'peak_xyz_mm':centroids[k].tolist()}
        if field_path and angle == 30:
            np.savez_compressed(
                field_path,
                points_mm=xyz,
                tetra_indices=t,
                displacement_mm=u.reshape(-1,3),
                stress_voigt_mpa=stress,
                von_mises_mpa=vm,
                force_n=f.reshape(-1,3),
                blocked_dofs=blocked,
            )
        cases.append(case)
        print(json.dumps(case),flush=True)
    del factor
res={'step':str(path),'max_size_mm':step,'width_mm':width,'nodes':len(xyz),'tets':len(t),'volume_cm3':float(vol.sum()/1000),'cases':cases}
output.write_text(json.dumps(res,indent=2))
print(len(xyz),len(t),'volume',res['volume_cm3'])
