from sexpdata import loads,dumps,Symbol as S
from pathlib import Path
from uuid import uuid4
import math
root=Path('/Users/alex/Nube /repos/Cruz_prototipe/electronica')
v7=root/'cross_v7_raspberry'
s=loads((v7/'cross_v7_draft.kicad_sch').read_text()); netlist=loads((v7/'cross_v7_draft.net').read_text())
def children(x,k):return [z for z in x if isinstance(z,list) and str(z[0])==k]
def one(x,k):return next(iter(children(x,k)),None)
def elem(x):return str(x[0]) if isinstance(x,list) and x else ''
nets={}
for n in children(one(netlist,'nets'),'net'):
 name=one(n,'name')[1]
 if str(name).startswith('N$'):continue
 for node in children(n,'node'):nets[(one(node,'ref')[1],one(node,'pin')[1])]=name
libs={x[1]:x for x in children(one(s,'lib_symbols'),'symbol')}
for sub in children(libs['4xxx:4013'],'symbol'):
 parts=sub[1].rsplit('_',2);sub[1]='_'.join(parts[:-1]+['1'])
instances=[x for x in children(s,'symbol') if one(x,'lib_id')[1]!='power:GND']
# 80 mm columns, 85 mm rows, 9x9 grid; A0 landscape.
new=[];uu=lambda:S(str(uuid4()))
for idx,ins in enumerate(instances):
 libid=one(ins,'lib_id')[1];unit=int(one(ins,'unit')[1]);props=children(ins,'property');ref=next(x[2] for x in props if x[1]=='Reference')
 col=idx%9;row=idx//9;cx=55.88+col*119.38;cy=60.96+row*88.9
 
 if ref=='U8':
  for p in props:
   if p[1]=='Value':p[2]='CD4013_LATCH_PROVISIONAL'
   if p[1]=='Footprint':p[2]='Package_DIP:DIP-14_W7.62mm'
 at=one(ins,'at');at[1:]=[cx,cy,0]
 for p in props:
  a=one(p,'at');a[1:]=[cx,cy+(-12 if p[1]=='Reference' else -9 if p[1]=='Value' else 0),0]
 ins[:]=[x for x in ins if elem(x)!='mirror']
 one(one(ins,'instances'),'project')[1]='cross_v8_draft'
 lib=libs[libid]
 for sub in children(lib,'symbol'):
  name=sub[1]; piece=name.rsplit('_',2)
  if len(piece)<3 or int(piece[-2]) not in (0,unit):continue
  for pin in children(sub,'pin'):
   pn=one(pin,'number')[1];a=one(pin,'at');px=round(cx+float(a[1]),4);py=round(cy-float(a[2]),4);ang=int(float(a[3]))%360
   key=(ref,pn)
   if key not in nets:
    new.append([S('no_connect'),[S('at'),px,py],[S('uuid'),uu()] ]);continue
   # Locate wire outwards from the component pin.
   dx,dy={0:(-2.54,0),90:(0,2.54),180:(2.54,0),270:(0,-2.54)}[ang]
   ex,ey=round(px+dx,4),round(py+dy,4)
   new.append([S('wire'),[S('pts'),[S('xy'),px,py],[S('xy'),ex,ey]],[S('stroke'),[S('width'),0],[S('type'),S('default')]],[S('uuid'),uu()]])
   la={0:0,180:0,90:90,270:90}[ang]
   new.append([S('label'),str(nets[key]),[S('at'),ex,ey,la],[S('effects'),[S('font'),[S('size'),0.85,0.85]],[S('justify'),S('left'),S('bottom')]],[S('uuid'),uu()]])
# remove every existing graphical connection, leave symbols in isolation.
s[:]=[x for x in s if elem(x) not in ('wire','label','global_label','junction','no_connect') and not (elem(x)=='symbol' and one(x,'lib_id')[1]=='power:GND')]
s.extend(new)
out=Path('/tmp/cruz_v8/cross_v8_draft.kicad_sch');out.write_text(dumps(s))
print('symbols',len(instances),'wire-label-nc',len(new),'known pins',len(nets))
