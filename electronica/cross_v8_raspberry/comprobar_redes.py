from sexpdata import loads
from collections import defaultdict
from pathlib import Path
def get(x,k):return next((z for z in x if isinstance(z,list) and str(z[0])==k),None)
def parse(f):
 s=loads(Path(f).read_text()); out={}
 for n in get(s,'nets')[1:]:
  name=get(n,'name')[1]; nodes={(get(x,'ref')[1],get(x,'pin')[1]) for x in n if isinstance(x,list) and str(x[0])=='node'}
  if len(nodes)>1:out[str(name)]=nodes
 return out
a=parse('/tmp/cruz_v7/cross_v7_draft.net');b=parse('/tmp/cruz_v8/export.net')
for k,v in a.items():
 if v not in b.values():print('MISMATCH',k,len(v), 'matched subsets',[(n,len(s),len(v&s)) for n,s in b.items() if v&s])
print('intended',len(a),'actual',len(b),'same groups',sum(v in b.values() for v in a.values()))
