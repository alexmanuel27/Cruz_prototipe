"""Physical assembly order; removable bridge and rear axial sensor access."""
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
steps=[]
def add(title,note,moves=None,hold=2.4,waypoints=None):
 s={'number':len(steps)+1,'title':title,'note':note,'moves':moves or {},'hold_seconds':hold}
 if waypoints:s['waypoints']=waypoints
 steps.append(s)
add('Unir las dos mitades del chasis','Colocar tuercas cautivas y fijar la unión M4. Dejar desmontado el travesaño de X216.',{'chassis':[80,0,0]})
add('Introducir la sonda de conductividad','Entrar desde atrás por el canal axial y fijar con apoyos blandos. Chasis transparente solo para mostrar este acceso.',{'ec':[240,0,0]},3)
add('Introducir la sonda de temperatura','Entrar desde atrás con el bloque de flujo premontado. Vista transparente para mostrar el acceso bajo el chasis.',{'temp':[110,0,0]})
add('Fijar los apoyos ópticos','Montar y comprobar los apoyos antes de colocar el cuarzo.',{'opt_support':[0,0,75]})
add('Instalar el módulo óptico premontado','En banco: montar PiCam, AS7265x y ambos LED en el portador. Después bajar el conjunto y fijarlo.',{'optics':[0,0,100]})
add('Instalar la cubeta de flujo','Apoyos blandos; no transmitir esfuerzos de las mangueras al cuarzo.',{'cell':[0,0,80]})

add('Montar la cámara auxiliar','Orientar la lente hacia la futura tapa transparente frontal.',{'webcam':[-100,0,0]})
add('Instalar la bomba completa','Motor y cabezal premontados. La muestra se mide antes de pasar por la bomba.',{'pump':[0,0,110]})
add('Fijar la interfaz Atlas en seco','Premontar placa lateral y carrier; dejar acceso a tornillos y bridas.',{'atlas':[0,-95,8]},waypoints={'atlas':[[0,-95,8],[0,0,8],[0,0,0]]})
add('Colocar la cubierta óptica','Conectar CSI a la PiCam y sacar su extremo libre. Pasar también la manguera superior, aún sin conectar.',{'hood':[0,0,80]},3.2)
add('Introducir las dos tuercas cautivas','Deslizar las M3 en los alojamientos laterales del chasis, antes de cerrar el travesaño.',{'bridge_nuts':[-18,0,0]})
add('Asentar el travesaño desmontable','Apoyar ambos extremos en las ménsulas del chasis; no cargar la cubierta óptica.',{'bridge':[0,0,65]})
add('Fijar el travesaño con dos M3','Tornillos avellanados M3 × 16; cabezas enrasadas y acceso libre antes de instalar la bandeja.',{'bridge_screws':[0,0,45]})
add('Sujetar la batería','Mantenerla desconectada y preparar el cableado antes de cubrir el compartimento.',{'battery':[0,0,110]})
add('Bajar la bandeja antes de la Raspberry','Bandeja vacía y separadores; extremo trasero recortado para que entre sin chocar con el aro.',{'bare_tray':[0,0,135]},3.4)
add('Montar la Raspberry junto a la PiCam','Conectar la cinta CSI sin tensarla y fijar la Pi sobre la cubierta. Mantener libres sus puertos.',{'pi':[0,0,65]},3)
add('Instalar PCB y módulos en la bandeja','V8 todavía de estudio. Colocar las placas con el equipo sin alimentación y sin forzar conectores.',{'pcb_modules':[0,0,100]},3)
add('Colocar los retenedores laterales','Entrar desde ambos lados, encajar las ranuras en el borde y fijar con M3.',{'clips_l':[0,-55,0],'clips_r':[0,55,0]})
add('Preparar y apoyar la tapa trasera','Premontar juntas, pasamuros y conector EN3 fuera del tubo; dejar la tapa accesible.',{'rear_cap':[100,0,0],'rear_gasket':[100,0,0]})
add('Conectar las mangueras inferiores','Con el tubo retirado, conectar sensores y pasamuros. Fijar rutas sin radios cerrados ni pellizcos.',{'hoses':[0,0,0]},3.2)
add('Conectar cubeta y bomba por arriba','Recuperar el extremo que se pasó por la cubierta y conectarlo a la bomba. Revisar ambos extremos.',{'upper_hose':[0,0,0]},3.2)
add('Revisar el conjunto todavía abierto','Comprobar fijaciones, CSI, cables y circuito hidráulico. Validar la electrónica antes de energizar.',hold=4.5)
add('Deslizar el tubo desde el frente','Guiarlo hasta la junta trasera sin rozar componentes; comprobar que ningún cable quede en el cierre.',{'tube':[-440,0,0]},3)
add('Introducir las cuatro varillas desde atrás','Tuercas y arandelas exteriores traseras premontadas; todavía sin comprimir las tapas.',{'rods_rear_hardware':[440,0,0]})
add('Colocar las arandelas interiores traseras','Deslizarlas desde los extremos delanteros libres; no atraviesan los taladros de la tapa.',{'rear_inner_washers':[-440,0,0]})
add('Colocar los limitadores de compresión','Deslizarlos sobre las varillas desde delante hasta las arandelas traseras.',{'limiters':[-440,0,0]})
add('Deslizar los dos conjuntos de lastre','Primero el collar trasero, después el delantero. Deslizar sobre tubo y limitadores antes de poner arandelas delanteras.',{'ballast_rear':[-440,0,0],'ballast_front':[-210,0,0]},3.4,{'ballast_rear':[[-440,0,0],[0,0,0],[0,0,0]],'ballast_front':[[-210,0,0],[-210,0,0],[0,0,0]]})
add('Colocar las arandelas interiores delanteras','Presentarlas contra los extremos de los limitadores.',{'front_inner_washers':[-70,0,0]})
add('Presentar junta y tapa frontal','Junta en la ranura de la tapa; limpiar, alinear y evitar retorcerla durante el cierre.',{'front_cap':[-100,0,0],'front_gasket':[-100,0,0]},3)
add('Cerrar alternando las diagonales','Colocar arandelas y tuercas exteriores; apretar por etapas y comprobar compresión uniforme.',{'front_hardware':[-75,0,0]},3.4)
add('Comprobar el montaje terminado','Revisar fijaciones, visión de cámara y lastre. El ensayo de estanqueidad se hace aparte, sin electrónica.',hold=5)
frame=1
for s in steps:
 s['first_frame']=frame;s['render_count']=48 if s.get('waypoints') else (32 if s['moves'] else 1);frame+=s['render_count']
state=json.loads((HERE/'ESTADO_ANTES_ANIMACION.json').read_text(encoding='utf-8'))
assigned={'base'}|{g for s in steps for g in s['moves']}
assert assigned=={r['group'] for r in state['motion']},assigned.symmetric_difference({r['group'] for r in state['motion']})
plan={'fps_render':24,'frame_count':frame,'steps':steps,'limits':['Secuencia comprobada en CAD por muestras discretas; pendiente de ensayo físico.', 'Travesaño X216 desmontable y canal axial EC: revisión propuesta, original conservado.', 'Cables, bridas, útiles y parte de la tornillería no están modelados; se indican en rótulos.', 'Mangueras mostradas por aparición; no se simula su flexión.', 'Juntas en geometría de trabajo, sin simulación elástica.', 'PCB V8 de estudio: no fabricar ni energizar sin terminar su validación.']}
(HERE/'PLAN_MONTAJE.json').write_text(json.dumps(plan,indent=2,ensure_ascii=True)+'\n')
print(len(steps),'steps,',frame,'native viewport frames')
