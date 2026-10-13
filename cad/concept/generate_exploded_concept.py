#!/usr/bin/env python3
"""Vector A3 assembly concept for Cruz; geometry is schematic and not to scale."""
from pathlib import Path
from math import atan2, cos, sin, pi
from reportlab.lib import colors
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

OUT = Path(__file__).resolve().parents[2] / 'docs/drawings/CRUZ-CON-001_exploded_concept.pdf'
W, H = landscape(A3)
K = colors.HexColor('#1D2933')
G = colors.HexColor('#8796A1')
F = colors.HexColor('#E9EEF1')
B = colors.HexColor('#087B94')   # water
T = colors.HexColor('#A46B19')   # transmission
V = colors.HexColor('#684887')   # fluorescence
R = colors.HexColor('#A23F39')
P = colors.HexColor('#3D7759')


def X(v): return v * mm

def Y(v): return H - v * mm

def text(c, x, y, s, size=7, bold=False, color=K, align='left'):
    c.setFillColor(color); c.setFont('Helvetica-Bold' if bold else 'Helvetica', size)
    if align == 'right': c.drawRightString(X(x), Y(y), s)
    elif align == 'center': c.drawCentredString(X(x), Y(y), s)
    else: c.drawString(X(x), Y(y), s)

def line(c, x1, y1, x2, y2, color=K, weight=.25, dash=None):
    c.setStrokeColor(color); c.setLineWidth(X(weight)); c.setDash(dash or [])
    c.line(X(x1), Y(y1), X(x2), Y(y2)); c.setDash([])

def rect(c, x, y, w, h, fill=None, stroke=K, weight=.3):
    c.setFillColor(fill or colors.white); c.setStrokeColor(stroke); c.setLineWidth(X(weight))
    c.rect(X(x), Y(y+h), X(w), X(h), stroke=1, fill=bool(fill))

def circ(c, x, y, radius, fill=None, stroke=K, weight=.3):
    c.setFillColor(fill or colors.white); c.setStrokeColor(stroke); c.setLineWidth(X(weight))
    c.circle(X(x), Y(y), X(radius), stroke=1, fill=bool(fill))

def poly(c, pts, fill=None, stroke=K, weight=.3):
    p=c.beginPath(); p.moveTo(X(pts[0][0]),Y(pts[0][1]))
    for x,y in pts[1:]: p.lineTo(X(x),Y(y))
    p.close(); c.setFillColor(fill or colors.white); c.setStrokeColor(stroke); c.setLineWidth(X(weight))
    c.drawPath(p,fill=bool(fill),stroke=1)

def arrow(c,x1,y1,x2,y2,color=K,weight=.45):
    line(c,x1,y1,x2,y2,color,weight); a=atan2(y2-y1,x2-x1)
    for off in (pi-.48,pi+.48):
        line(c,x2,y2,x2+2.7*cos(a+off),y2+2.7*sin(a+off),color,weight)

def balloon(c,n,x,y,tx,ty):
    line(c,x,y,tx,ty,G,.18); circ(c,x,y,3.5,colors.white,K,.35)
    text(c,x,y+1.45,f'{n:02d}',6.4,True,K,'center')

def frame(c,num,title,subtitle):
    rect(c,9,9,402,279,stroke=K,weight=.5); rect(c,13,13,394,271,stroke=G,weight=.15)
    text(c,17,22,'CRUZ',17,True); line(c,48,16,48,32,K,.28)
    text(c,52,21,title,12,True); text(c,52,28,subtitle,7,color=G)
    rect(c,328,16,79,16,stroke=R,weight=.5)
    text(c,367.5,22.2,'CONCEPTO / NO FABRICAR',8,True,R,'center')
    text(c,367.5,28,'Cotas no verificadas: TBD',6,color=R,align='center')
    for i,x in enumerate((38,88,138,188,238,288,338,388),1):
        text(c,x,11.8,str(i),5,color=G,align='center');text(c,x,287,str(i),5,color=G,align='center')
    for a,y in zip('ABCD',(48,109,177,258)):
        text(c,11,y,a,5,color=G,align='center');text(c,409,y,a,5,color=G,align='center')
    titleblock(c,num,title)

def titleblock(c,num,title):
    x,y=17,246; rect(c,x,y,390,38,stroke=K,weight=.4)
    line(c,261,y,261,y+38);line(c,325,y,325,y+38);line(c,x,y+16,407,y+16,G,.2)
    text(c,21,y+5.5,'PROYECTO',5.2,True,G);text(c,21,y+12.7,'CRUZ | Instrumento para agua natural',8,True)
    text(c,21,y+22,'TIPO DE DOCUMENTO',5.2,True,G);text(c,21,y+31,title.upper(),8,True)
    text(c,265,y+5.5,'PLANO',5.2,True,G);text(c,265,y+12.7,'CRUZ-CON-001',8,True)
    text(c,265,y+21.5,'FECHA',5.2,True,G);text(c,265,y+29.5,'2026-09-30',7.4,True)
    text(c,329,y+5.5,'ESCALA',5.2,True,G);text(c,329,y+12.7,'NTS',8,True)
    text(c,329,y+21.5,'REV.  B',5.2,True,G);text(c,329,y+29.5,f'HOJA  {num} / 2',7.4,True)

def panel(c,x,y,w,h,tag,title,sub=''):
    rect(c,x,y,w,h,stroke=G,weight=.25);rect(c,x,y,w,8.5,F,G,.2)
    text(c,x+4,y+5.9,tag+'  '+title,7.5,True)
    if sub:text(c,x+w-4,y+5.9,sub,6,color=G,align='right')

def exploded(c):
    frame(c,1,'CONJUNTO ÓPTICO EXPLOSIONADO','Vista superior de módulos desplazados sobre sus ejes de montaje')
    panel(c,17,39,269,199,'A','VISTA SUPERIOR EXPLOSIONADA','representación esquemática · NTS')
    cx,cy=146,140
    line(c,21,cy,281,cy,G,.14,[5,2,1,2]);line(c,cx,53,cx,232,G,.14,[5,2,1,2])
    text(c,24,58,'EJE T / TRANSMISIÓN',6.2,True,T)
    text(c,24,65,'EJE F / FLUORESCENCIA',6.2,True,V)
    text(c,278,58,'MUESTRA EN EL CRUCE',6.7,True,align='right')
    # Ghosted assembled seats and central 3D-printed carrier.
    poly(c,[(132,85),(160,85),(160,125),(205,125),(205,155),(160,155),
            (160,195),(132,195),(132,155),(87,155),(87,125),(132,125)],F,G,.25)
    rect(c,126,120,40,40,stroke=K,weight=.5)
    rect(c,136,130,20,20,stroke=B,weight=.3)
    for x,y,w,h in ((90,130,28,20),(174,130,28,20),(136,88,20,28),(136,164,20,28)):
        rect(c,x,y,w,h,stroke=G,weight=.2)
    balloon(c,1,105,181,128,155)
    text(c,25,182,'01  soporte óptico impreso',6.1,True)
    text(c,25,190,'Asientos finales y dimensiones: TBD',5.8,color=G)
    # Flow cell exploded above carrier; port stubs are symbolic.
    rect(c,176,70,20,20,colors.HexColor('#D9EFF2'),K,.45)
    rect(c,180,74,12,12,stroke=B,weight=.2)
    line(c,172,80,176,80,B,.7);line(c,196,80,200,80,B,.7)
    arrow(c,177,94,159,121,G,.25);balloon(c,2,209,72,196,80)
    text(c,193,102,'insertar celda',5.8,color=G,align='center')
    # Halogen source on the left. The sample precedes the slit.
    rect(c,24,126,30,28,stroke=K,weight=.5);circ(c,39,140,7.5,stroke=T,weight=.55)
    for yy in (131,135,145,149):line(c,24,yy,54,yy,G,.2)
    arrow(c,57,140,82,140,T,.6);balloon(c,3,29,113,31,126)
    text(c,39,161,'fuente visible',6.3,True,T,'center')
    # Slit, grating/lens, camera on the right.
    line(c,218,128,218,137,K,1.25);line(c,218,143,218,152,K,1.25)
    arrow(c,206,140,225,140,T,.6);balloon(c,4,220,113,218,129)
    circ(c,239,140,7,stroke=K,weight=.5);line(c,237,135,242,145,G,.65)
    rect(c,253,126,25,28,stroke=K,weight=.5)
    rect(c,259,132,13,16,fill=F,stroke=K,weight=.25)
    line(c,260,145,270,135,T,.5);balloon(c,5,272,112,266,126)
    text(c,246,162,'rendija  →  red/lente  →  cámara',5.9,True,align='center')
    text(c,207,171,'0,5 mm / 60 mm heredados;',5.8,color=G)
    text(c,207,177,'referencias de cota: verificar',5.8,color=G)
    text(c,207,183,'36° heredados; confirmar montaje',5.8,color=G)
    # Fluorescence LED above, detector below.
    rect(c,134,48,24,16,stroke=K,weight=.5);circ(c,146,56,4,stroke=V,weight=.55)
    balloon(c,6,116,52,134,56);arrow(c,146,96,146,116,V,.6)
    text(c,146,106,'LED 430 nm',5.8,True,V,'center')
    rect(c,129,211,34,16,stroke=K,weight=.5)
    for xx in (136,146,156):circ(c,xx,219,2,stroke=G,weight=.2)
    arrow(c,146,163,146,207,V,.6);balloon(c,7,177,219,163,219)
    text(c,146,206,'AS7265x · 18 canales',5.9,True,V,'center')
    text(c,25,215,'T: fuente → celda → rendija → red/lente → cámara',6.1,True,T)
    text(c,25,224,'F: LED 430 nm → celda → AS7265x (645 nm principal)',6.1,True,V)
    text(c,278,232,'Sin colimador · sin filtro de emisión',5.8,color=G,align='right')
    parts(c)
    text(c,19,242,'Convenciones: ISO 128, ISO 5457 e ISO 7200. Referencias de cota y posición de la celda pendientes de medición.',5.8,color=G)

def parts(c):
    x,y,w,h=290,39,117,199
    panel(c,x,y,w,h,'B','LISTA DE ELEMENTOS','cantidades y materiales: TBD')
    line(c,x+13,y+8.5,x+13,y+h,G,.15);line(c,x+91,y+8.5,x+91,y+h,G,.15)
    text(c,x+6.5,y+15,'ID',5.7,True,G,'center');text(c,x+17,y+15,'ELEMENTO / FUNCIÓN',5.7,True,G)
    text(c,x+104,y+15,'ESTADO',5.7,True,G,'center');line(c,x,y+18,x+w,y+18,G,.18)
    items=[('01','Soporte óptico en cruz','propuesta'),('02','Celda de flujo de cuarzo','comprada'),
       ('03','Fuente visible 10 W','heredada'),('04','Rendija 0,5 mm','heredada'),
       ('05','Red + gran angular + cámara','heredados'),('06','LED de excitación 430 nm','fijado'),
       ('07','AS7265x · 18 canales','heredado'),('08','Carcasa impresa, zona seca','diseñar'),
       ('09','Tapa y junta estática','diseñar'),('10','Interfaz óptica estanca','diseñar'),
       ('11','Toma, tubos y descarga','diseñar'),('12','Bomba peristáltica sumergida','fijada'),
       ('13','Portaelectrónica y energía','diseñar')]
    for i,(num,name,status) in enumerate(items):
        yy=y+18+i*12.8
        if i%2:rect(c,x+.2,yy+.2,w-.4,12.4,F,F,.01)
        line(c,x,yy+12.8,x+w,yy+12.8,G,.13)
        text(c,x+6.5,yy+7.8,num,6.2,True,align='center')
        text(c,x+16,yy+7.8,name,6.0)
        text(c,x+104,yy+7.8,status,5.2,False,P if status in ('comprada','heredada','heredados','fijado','fijada') else G,'center')
    text(c,x+4,y+h-5,'BOM comercial, tornillería y tolerancias en X1.3.',5.2,color=G)

def section(c):
    frame(c,2,'ENVOLVENTE E INTERFACES','Sección de arquitectura y esquema de servicio para el CAD y ensayo de estanqueidad')
    panel(c,17,39,254,132,'C','SECCIÓN FUNCIONAL EXPLOSIONADA','corte esquemático · NTS')
    line(c,144,48,144,168,G,.14,[5,2,1,2])
    rect(c,89,55,110,9,F,K,.5);balloon(c,9,71,58,89,59)
    text(c,206,61,'tapa impresa',6.2,True)
    line(c,91,73,197,73,P,.9);line(c,91,76,197,76,P,.9)
    balloon(c,9,71,75,91,74);text(c,205,77,'junta estática',6.0,True,P)
    arrow(c,144,79,144,88,G,.25)
    poly(c,[(84,91),(92,91),(92,145),(196,145),(196,91),(204,91),
            (204,156),(84,156)],F,K,.55)
    for yy in range(96,151,5):
        line(c,84,yy+2,92,yy-2,G,.15);line(c,196,yy+2,204,yy-2,G,.15)
    balloon(c,8,70,120,84,120);text(c,207,120,'carcasa / barrera de agua',5.8,True)
    rect(c,104,101,80,18,stroke=K,weight=.35)
    rect(c,110,104,25,12,stroke=G,weight=.25)
    rect(c,143,104,32,12,stroke=G,weight=.25)
    text(c,122,111,'batería',5.3,color=G,align='center');text(c,159,111,'control',5.3,color=G,align='center')
    balloon(c,13,74,104,104,104);text(c,144,126,'ZONA SECA',7.2,True,align='center')
    line(c,95,129,193,129,G,.17,[4,2])
    rect(c,132,136,24,31,colors.HexColor('#DDF0F3'),B,.55)
    rect(c,137,140,14,22,stroke=B,weight=.2)
    text(c,144,151,'agua',5.4,True,B,'center')
    balloon(c,2,116,161,132,154)
    line(c,128,138,128,164,K,1.0);line(c,160,138,160,164,K,1.0)
    balloon(c,10,216,155,160,150)
    text(c,210,164,'sello celda-zona seca: TBD',5.7,color=R)
    arrow(c,94,152,131,152,B,.6);arrow(c,157,152,194,152,B,.6)
    text(c,94,166,'toma',5.8,True,B);text(c,192,166,'hacia bomba',5.8,True,B,'right')
    text(c,20,165,'Sección simbólica: cierre y soporte definitivos se calculan en X1.3.',5.3,color=G)
    interfaces(c);hydraulics(c);gates(c)

def interfaces(c):
    x,y=275,39;panel(c,x,y,132,132,'D','REGISTRO DE INTERFACES','medir antes del CAD')
    items=[('I-01','Celda: modelo, cuerpo, caras y puertos'),
        ('I-02','Rendija-cámara: origen de los 60 mm'),
        ('I-03','LED y AS7265x: placas y distancias'),
        ('I-04','Unión óptica seca / celda húmeda'),
        ('I-05','Tapa: material, junta, ranura, apriete'),
        ('I-06','Tubos/racores: medidas y sujeción'),
        ('I-07','Bomba: tamaño, caudal, cable sellado'),
        ('I-08','Energía y calor: volumen/disipación')]
    for i,(num,name) in enumerate(items):
        yy=55+i*13.5;line(c,278,yy+8,404,yy+8,G,.14)
        text(c,279,yy+4.7,num,6,True);text(c,298,yy+4.7,name,5.6)
    text(c,279,164,'No asignar tolerancias sin medición.',5.8,True,R)

def hydraulics(c):
    panel(c,17,175,187,65,'E','CIRCUITO DE AGUA Y SECUENCIA','componentes sumergidos')
    items=[(22,30,'TOMA'),(66,38,'CELDA'),(119,38,'BOMBA'),(171,30,'SALIDA')]
    for x,w,name in items:
        rect(c,x,191,w,15,F,B,.35);text(c,x+w/2,200.5,name,6.3,True,B,'center')
    for x1,x2 in ((52,66),(104,119),(157,171)):arrow(c,x1+1,198,x2-1,198,B,.6)
    text(c,20,217,'La muestra se mide antes de la bomba; celda y tubos quedan llenos.',6.2)
    text(c,20,225,'Ciclo: purga → oscuro → transmisión → fluorescencia → datos.',6.2)
    text(c,20,233,'Sin caudalímetro a bordo; volumen de purga calibrado en banco.',6.0,color=G)

def gates(c):
    panel(c,208,175,199,65,'F','CONDICIONES DE AVANCE','estado: pendiente')
    for y,name,body,color in ((192,'ÓPTICA','OPT-01 a OPT-07 con la celda definitiva',T),
                              (201,'SELLOS','Juntas y pasamuros diseñados antes del 19 oct',P),
                              (210,'ENSAYO','30 oct: inmersión con lastre, sin electrónica',B)):
        text(c,212,y,name,6,True,color);text(c,244,y,body,6.1)
    line(c,212,217,403,217,G,.16)
    text(c,212,226,'Material, cotas, fijaciones y protección real: por validar.',6.1,color=G)
    text(c,212,234,'El boceto no habilita impresión ni mecanizado.',6.1,True,R)

def main():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    c=canvas.Canvas(str(OUT),pagesize=landscape(A3),pageCompression=1)
    c.setTitle('CRUZ-CON-001 | Plano conceptual explosionado')
    c.setAuthor('Cruz prototype engineering')
    exploded(c);c.showPage();section(c);c.showPage();c.save()
    print(OUT)

if __name__ == '__main__': main()
