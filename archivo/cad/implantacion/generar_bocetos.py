"""ARCHIVO D45: bocetos verticales anteriores. No son el diseño vigente."""
from pathlib import Path
from html import escape
from math import sqrt
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/drawings'
C={'ink':'#172b3a','muted':'#5e7180','line':'#b9c9d3','blue':'#237dba','water':'#1396b8','pump':'#bb7333','green':'#41896a','purple':'#775aa5','red':'#d75a62','amber':'#eaa33d'}
class SVG:
 def __init__(self,w,h,title,sub):
  self.w=w;self.h=h;self.s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"><title>{escape(title)}</title><defs>']
  for k in ['water','red','amber','blue','ink']:
   self.s.append(f'<marker id="a-{k}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto-start-reverse"><path d="M0,1 L7,4 L0,7" fill="none" stroke="{C[k]}" stroke-width="1.5"/></marker>')
  self.s+=['<linearGradient id="rainbow" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#995cde"/><stop offset=".25" stop-color="#4493df"/><stop offset=".5" stop-color="#60b97d"/><stop offset=".75" stop-color="#f8d85d"/><stop offset="1" stop-color="#eb7063"/></linearGradient></defs>',f'<rect width="{w}" height="{h}" fill="white"/>','<g font-family="Arial, Helvetica, sans-serif" stroke-linecap="round" stroke-linejoin="round">']
  self.text(65,65,title,39,bold=True);self.text(65,105,sub,23,C['muted'])
 def add(self,s):self.s.append(s)
 def text(self,x,y,t,size=23,color=None,bold=False,anchor='start'):
  self.add(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color or C["ink"]}" font-weight="{700 if bold else 400}" text-anchor="{anchor}">{escape(t)}</text>')
 def rect(self,x,y,w,h,fill='white',stroke=None,rx=5,dash=None):
  self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke or C["line"]}" stroke-width="2"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
 def circle(self,x,y,r,fill='none',stroke=None,dash=None):
  self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke or C["line"]}" stroke-width="2"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
 def path(self,pts,color='ink',width=3,arrow=False,dash=None):
  self.add(f'<polyline points="'+ ' '.join(f'{x},{y}' for x,y in pts)+f'" fill="none" stroke="{C.get(color,color)}" stroke-width="{width}"'+(f' marker-end="url(#a-{color})"' if arrow else '')+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
 def dim(self,x1,y1,x2,y2,label,tx,ty):
  self.add(f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{C["muted"]}" stroke-width="1.7" marker-start="url(#a-ink)" marker-end="url(#a-ink)"/>');self.text(tx,ty,label,22,C['muted'])
 def finish(self,name):
  self.add('</g></svg>');(OUT/name).write_text('\n'.join(self.s))

# LÁMINA 1: corte longitudinal y dos secciones funcionales.
a=SVG(1700,1580,'ARCHIVO · distribución vertical','Sustituida por PVC horizontal · revisión D45 · 21 oct 2026')
a.text(65,163,'A · Equipo vertical',28,bold=True)
a.text(65,199,'Corte esquemático; los bloques son reservas de espacio.',21,C['muted'])
sc=2.5; cx=400; zb=1190
Y=lambda z:zb-z*sc
# top/bottom, walls, guide columns
for x in [175,625]:a.rect(x,Y(330)-25,8,890,'#acb9c2','#667786',0)
a.rect(cx-187.5,Y(330),375,825,'#f5fbfd',C['water'],0)
a.rect(cx-175,Y(330),350,825,'#fbfdfe',C['line'],0)
for z in [0,330]:a.rect(150,Y(z)-(25 if z==330 else 0),500,25,'#e8e1f3',C['purple'],0)
for z in [15,80,90,165,170,255,260,315]:a.path([(cx-170,Y(z)),(cx+170,Y(z))],C['line'],1.2,dash='6 8')
# Side rails on removable chassis
for x in [cx-143,cx+143]:a.rect(x,Y(315),9,750,'#dbe4e9','#a1b1bb',1)
# Battery envelope height 65, not fictitious real dimensions
by=Y(80);a.rect(300,by+6,200,150,'#edf3e2','#82a251')
a.text(400,by+61,'BATERÍA',23,bold=True,anchor='middle');a.text(400,by+95,'+ fusible',22,anchor='middle');a.text(400,by+126,'base elevada',20,C['muted'],anchor='middle')
# optics zone 90–165
oy=Y(165);a.rect(282,oy+5,240,177,'#eaf1f4','#7c8c97',3)
# El rótulo óptico queda fuera para mantener visibles los conductos.
a.rect(366,Y(153),34,145,'#def3f7',C['water'],1)
a.path([(383,Y(108)),(383,Y(148))],'water',3,True)
a.rect(291,Y(128),65,38,'#fae4c4',C['amber']);a.rect(425,Y(128),85,38,'#d5dfe6','#60798d')
a.path([(351,Y(120)),(430,Y(120))],'amber',3)
# Resguardo opaco indicado en la llamada exterior.
# Electronics + auxiliary camera shared at same height, opposite sides, see section C
py=Y(255);a.rect(318,py+7,170,202,'#e5f1e9',C['green'])
a.text(401,py+48,'Pi + control',23,bold=True,anchor='middle');a.text(401,py+82,'DC/DC',22,anchor='middle');a.text(401,py+112,'y drivers',22,anchor='middle')
a.rect(492,Y(240),46,78,'#d9e9f5',C['blue']);a.circle(532,Y(225),9,'#567e9c',C['blue'])
a.path([(541,Y(225)),(572,Y(225)+18),(572,Y(225)-18),(541,Y(225))],'blue',2)
a.text(401,py+187,'ver sección C',20,C['muted'],anchor='middle')
# Pump reservation 55mm explicitly not model dimensions
a.rect(355,Y(315)+4,174,127,'#fbebdc',C['pump'],5,dash='7 5')
a.circle(406,Y(289),38,'#fff9f3',C['pump']);a.text(406,Y(289)+8,'P',27,C['pump'],True,anchor='middle');a.text(490,Y(289)+8,'motor',18,C['pump'],anchor='middle')
# top ports intake at -120 and outlet at+120 in elevation offset to left of camera
a.rect(262,Y(330)-60,22,60,'#dcf0f6',C['water'],2);a.rect(506,Y(330)-60,22,60,'#dcf0f6',C['water'],2)
a.text(245,Y(330)-75,'IN',22,C['water'],True);a.text(493,Y(330)-75,'OUT',22,C['water'],True)
a.path([(273,Y(330)-10),(273,Y(98)),(383,Y(98)),(383,Y(106))],'water',5,True)
a.path([(383,Y(151)),(383,Y(163)),(548,Y(163)),(548,Y(289)),(445,Y(289))],'water',5,True)
a.path([(445,Y(302)),(517,Y(302)),(517,Y(330)-49)],'water',5,True)
# leak sensor beneath raised battery, drain gutter indicative
# note no bulkheads implied
for x in [278,548]:a.path([(x,Y(90)),(x,Y(10))],C['line'],1.8,dash='5 6')
a.rect(373,Y(12),55,18,'#f5d7db',C['red'],2);a.text(400,Y(12)+16,'fuga',14,C['red'],anchor='middle')
# Labels positioned to right of assembly
for z,title,subtitle,col in [(323,'Puertos de servicio','Agua ×2 · datos/carga · vent',C['purple']),(285,'Bomba arriba','Reserva axial: 55 mm*',C['pump']),(215,'Electrónica + cámara USB','Miran a caras opuestas (C)',C['green']),(128,'Cubeta vertical + cruz','Flujo ascendente · resguardo opaco',C['water']),(48,'Batería abajo','Separada del canal hidráulico','#6e8e3c'),(7,'Testigo de fuga','Batería sobre bandeja elevada',C['red'])]:
 yy=Y(z);a.path([(585,yy),(670,yy)],C['line'],1.7);a.text(685,yy-4,title,21,col,True);a.text(685,yy+24,subtitle,18,C['muted'])
a.dim(105,Y(330),105,Y(0),'330',55,790)
a.dim(225,1255,575,1255,'Ø140 interior',303,1290)
a.text(65,1334,'*Reserva provisional: medir bomba completa, racores y curvas de tubo.',21,C['muted'])
# panel separation
a.path([(1020,155),(1020,1355)],C['line'],1.5)
# Optical section x mapping scale3.3
a.text(1070,164,'B · Cruz vista desde arriba',27,bold=True)
a.text(1070,198,'Nivel óptico · z ≈ 128 mm',21,C['muted'])
ox,oy,ss=1350,475,3.3
P=lambda x,y:(ox+x*ss,oy-y*ss)
a.circle(ox,oy,75*ss,'#eef8fb',C['water']);a.circle(ox,oy,70*ss,'#fff',C['water'])
def boxxy(x,y,w,h,fill,stroke):
 px,py=P(x-w/2,y+h/2);a.rect(px,py,w*ss,h*ss,fill,stroke,2)
# compact unverified envelopes
boxxy(-54,0,20,19,'#fae4c4',C['amber']);boxxy(-22,0,12.5,12.5,'#dff3f8',C['water'])
boxxy(-22,35,22,14,'#dcece4',C['green']);boxxy(-22,-35,18,16,'#e5e8fc',C['blue'])
# beam BEFORE grating only
start,end=P(-43,0),P(50,0);a.path([start,end],'amber',3)
sl=P(-10,0);a.path([(sl[0],sl[1]-30),(sl[0],sl[1]+30)],'ink',6)
# camera reserve and rainbow located at grating/lens, not across free path
boxxy(58,0,20,23,'#dfe6eb','#60788b')
gx,gy=P(50,0);a.rect(gx-4,gy-28,8,56,'url(#rainbow)','#697d8b',0)
a.path([P(-22,-27),P(-22,-6.5)],'blue',4,True)
a.path([P(-22,6.5),P(-22,27)],'red',4,True)
# Identificar los componentes sin simular la envolvente definitiva.
a.text(*P(-54,-1.5),'Halógena',13,C['pump'],True,anchor='middle')
a.text(1390,287,'Red/lente + OV9281',20,C['muted'],True)
a.path([(1538,300),P(58,12)],C['line'],2)
a.text(sl[0]+12,oy+46,'0,5 mm',17,C['muted'])
# leaders all labels outside circle
a.text(1070,248,'AS7265x · receptor',21,C['green'],True);a.path([(1240,255),P(-22,42)],C['line'],2)
a.text(1070,730,'LED 430 nm → muestra',21,C['blue'],True);a.path([(1245,710),P(-22,-43)],C['line'],2)
a.text(1070,770,'Rojo: emisión de la muestra hacia el sensor.',19,C['red'])
a.text(1070,806,'Ámbar: transmisión hasta la red/lente.',19,C['amber'])
a.dim(sl[0],oy+66,gx,oy+66,'60 mm de referencia',sl[0]+5,oy+96)
a.text(1070,850,'Se conservan 36° y gran angular del MonoSpectro.',19,C['muted'])
a.text(1070,880,'Envolventes compactas por medir; sin colimador.',19,C['muted'])
# section C electronics
a.text(1070,951,'C · Cámara y placas, mismo nivel',26,bold=True)
ex,ey,t=1350,1160,2.3
a.circle(ex,ey,75*t,'#eef8fb',C['water']);a.circle(ex,ey,70*t,'white',C['water'])
# Pi edge view: plane vertical, board width56 radialx, thickness reserve25
# all section reserves explicitly
xx=ex-28*t;yy=ey-52*t;a.rect(xx,yy,56*t,28*t,'#e0efe5',C['green'],3)
a.text(ex,yy+40,'Pi + cables',18,C['green'],True,anchor='middle')
a.rect(ex-60*t,ey-15*t,22*t,30*t,'#edf2e5','#819959',2);a.rect(ex+38*t,ey-15*t,22*t,30*t,'#edf2e5','#819959',2)
a.text(ex,ey+8,'espacio libre',19,C['muted'],anchor='middle')
a.rect(ex-20*t,ey+23*t,40*t,25*t,'#dceaf6',C['blue'],3);a.circle(ex,ey+50*t,12,'#638baa',C['blue'])
a.path([(ex,ey+52*t),(ex-34,ey+71*t),(ex+34,ey+71*t),(ex,ey+52*t)],'blue',2)
a.text(1070,1382,'Cámara auxiliar → exterior por pared transparente.',20,C['blue'])
a.text(1070,1414,'Soportes, placas y cableado: reservas por ajustar.',19,C['muted'])
a.path([(65,1450),(1635,1450)],C['line'],1.5)
a.text(65,1490,'RECORRIDO: toma → cubeta → bomba → descarga. Transmisión primero; fluorescencia después.',23,bold=True)
a.text(65,1530,'Implantación propuesta · no demuestra encaje · espesores, juntas y taladros siguen pendientes.',21,C['muted'])
a.finish('implantacion-interior-v1.svg')

# LÁMINA 2: tapa de servicio, posiciones provisionales
b=SVG(1600,1360,'ARCHIVO · tapa del cuerpo acrílico','Referencia anterior · Ø200 y posiciones no aplicables automáticamente a PVC')
b.text(65,163,'A · Todos los servicios en una tapa',28,bold=True)
ccx,ccy,k=500,590,3.2
R=lambda r:r*k
b.circle(ccx,ccy,R(100),'#f1edf8',C['purple'])
b.circle(ccx,ccy,R(75),'#e1f3f8',C['water']);b.circle(ccx,ccy,R(70),'#fff',C['water'])
b.circle(ccx,ccy,R(72.5),'none',C['amber'])
b.path([(ccx-345,ccy),(ccx+345,ccy)],C['line'],1,dash='8 8');b.path([(ccx,ccy-345),(ccx,ccy+345)],C['line'],1,dash='8 8')
# Tie rod slots are not final holes
for sx in [-1,1]:
 for sy in [-1,1]:
  px=ccx+sx*87/sqrt(2)*k;py=ccy+sy*87/sqrt(2)*k
  b.circle(px,py,24,'#dce3e8','#738594',dash='5 4');b.circle(px,py,7,'#738594','#738594')
ports=[('H1',-30,25,12,C['water'],'Entrada de agua'),('H2',30,25,12,C['water'],'Salida desde bomba'),('V1',-30,-25,10,C['pump'],'Vent o PRV'),('E1',20,-25,18,C['green'],'Datos + carga')]
for code,x,y,r,col,label in ports:
 px=ccx+x*k;py=ccy-y*k;b.circle(px,py,R(r),'#f8fbfd',col,dash='6 5')
 b.text(px,py+6,code,22,col,True,anchor='middle')
 # distinct short titles in central free space near ports
 b.text(px,py+R(r)+27,label,18,col,anchor='middle')
b.text(500,975,'Ø200 mm: reserva de contorno de tapa',23,C['purple'],True,anchor='middle')
b.text(500,1008,'Ø150 / Ø140: tubo · naranja: posición provisional del sello',20,C['muted'],anchor='middle')
b.text(500,1040,'Gris: cuatro tirantes exteriores al tubo',20,C['muted'],anchor='middle')
b.rect(905,183,630,272,'#f5f9fb',C['line'],10)
b.text(935,225,'Cuatro puertos funcionales',27,bold=True)
for i,(code,_,_,_,col,label) in enumerate(ports):b.text(935,273+i*46,f'{code}   {label}',24,col,True)
b.text(935,501,'Los círculos discontinuos reservan sitio',23,bold=True)
b.text(935,534,'para tuercas, juntas y herramienta.',23,bold=True)
b.text(935,571,'Su diámetro NO es el diámetro del taladro.',22,C['red'])
b.text(935,627,'Antes de perforar',27,bold=True)
for i,line in enumerate(['Elegir cada componente de panel.','Comprobar tuerca, arandela y tapón.','Fijar espesor de tapa y ranura.','Verificar giro y radios de manguera.','Calcular ligamentos y apriete.']):b.text(935,673+i*39,'• '+line,22,C['muted'])
b.rect(905,915,630,158,'#f4f1f8',C['purple'],8)
b.text(935,955,'Tapa inferior: ciega y desmontable',25,C['purple'],True)
b.text(935,993,'Salida del bastidor por abajo, con conexiones',21,C['muted'])
b.text(935,1025,'de servicio accesibles y desconectables.',21,C['muted'])
b.path([(65,1110),(1535,1110)],C['line'],1.5)
b.text(65,1154,'H1 → entrada inferior de cubeta → salida superior → bomba → H2',27,C['water'],True)
b.text(65,1197,'La toma exterior se prolonga lejos de la descarga para evitar recircular la misma agua.',23,C['muted'])
b.text(65,1250,'Ø200, posiciones y reservas de puertos son propuestas; espesor y taladros no están definidos.',22,C['red'])
b.text(65,1292,'No perforar la pared curva. No imprimir ni mecanizar a partir de esta lámina.',22,C['muted'])
b.finish('tapa-servicios-v1.svg')
print('SVG de implantación y tapa generados.')
