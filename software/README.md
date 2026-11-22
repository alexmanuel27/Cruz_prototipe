# Monitor local de Cruz

Monitor para Python 3.11 o posterior en macOS o Raspberry Pi OS. Programa los ciclos aunque se cierre el navegador y guarda cada ciclo con sus ajustes en SQLite. El panel en inglés se actualiza cada dos segundos y se adapta a pantallas de escritorio y móvil.

- **Monitor** muestra temperatura, conductividad y el espectro del último ciclo. Desde aquí se configura el intervalo, se pausa la adquisición automática o se solicita una medición.
- **Optical settings** reúne los ajustes de cámara y fluorómetro.
- **History** muestra las mediciones recientes, con el historial en CSV y los datos originales de cada ciclo en JSON.

## Probar en el Mac

Desde el repo:

```sh
python3 software/cruz.py --simulate
```

Abre [el panel local](http://127.0.0.1:8080). Arranca a 900 segundos por muestra. Para ver varias seguidas, baja el intervalo a **3 segundos** desde el panel. Todo dato de este modo es sintético, incluidas la transmisión por píxel y las 18 bandas del AS7265x. El modo simulado no requiere dependencias externas ni accede a GPIO, I²C o cámaras.

```sh
python3 -m unittest discover -s software/tests
python3 software/cruz.py --simulate --cycles 24 --config software/config/operation.example.json --output /tmp/cruz-demostracion
```

`--cycles` ejecuta una serie inmediata sin navegador ni espera y solo admite simulación. `--config` establece el ajuste inicial de una carpeta nueva. Los cambios del panel pasan a ser la configuración persistente.

## Primera prueba en la Pi 5

Con el Mac en la red Cruz, desde el repo copia el software y abre un túnel:

```sh
ssh alex@10.42.0.1 'mkdir -p ~/cruz-monitor'
scp -r software alex@10.42.0.1:cruz-monitor/
ssh -L 8080:127.0.0.1:8080 alex@10.42.0.1
```

En esa sesión SSH:

```sh
python3 ~/cruz-monitor/software/cruz.py --sensors
```

Abre en el Mac [el mismo panel local](http://127.0.0.1:8080). El modo de banco lee un DS18B20 por 1-Wire y el Atlas EC-OEM K0.1 en I²C 1, dirección 0x64. Requiere `i2ctransfer` del paquete `i2c-tools` y acceso de `alex` a `/dev/i2c-1`. Si falta permiso, comprueba el grupo `i2c` antes de arrancar el servicio. Usa este modo con el banco cableado como en las pruebas individuales. Si uno de los sensores falla, el otro puede guardar su lectura y el ciclo queda marcado como parcial. El Atlas conserva K y calibración. Se guarda la compensación térmica que el propio módulo reporta.

Una vez verificada la captura en la Pi, se puede iniciar automáticamente con el servicio de usuario incluido. Desde la Pi, con el monitor manual detenido:

```sh
mkdir -p ~/.config/systemd/user
cp ~/cruz-monitor/software/systemd/cruz.service ~/.config/systemd/user/
systemctl --user daemon-reload
sudo loginctl enable-linger "$USER"
systemctl --user enable --now cruz.service
```

Para entrar al panel más tarde basta volver a abrir el túnel. Para consultar el servicio, usa `systemctl --user status cruz.service`. Para detenerlo, usa `systemctl --user stop cruz.service`.

## Revisión de MonoSpectro y fluorómetro

- MonoSpectro configura la OV9281 en modo manual con exposición inicial de 50 ms, ganancia 11 y ROI de (100, 300) a (1100, 420). Prefiere RAW10 y guarda los metadatos de captura. Sus blancos, oscuros y calibraciones dependen del ROI, la exposición y la ganancia.
- El fluorómetro usa 10 lecturas por medición y conserva referencias oscuras y blancas de 18 canales. Su refrigeración programada es de 60 s después de tres mediciones iluminadas. No configura explícitamente ganancia ni integración en el firmware revisado.
- Estos valores describen los instrumentos anteriores. En Cruz siguen pendientes las capturas reales, el ajuste óptico, las referencias, la secuencia de iluminación y la evaluación de los tiempos. No se copian calibraciones ni fórmulas de concentración como si fueran válidas para la nueva geometría.
- El panel muestra los 18 canales simulados y descarga el espectro del último ciclo simulado en CSV. El archivo identifica el modo y conserva oscuro y luz azul por canal. Las lecturas reales del AS7265x aún no están integradas.

## Ajustes ópticos en el panel

El panel permite guardar exposición, ganancia, formato y ROI de cámara, además de réplicas, enfriamiento, ganancia e integración del AS7265x. Los valores iniciales de cámara y enfriamiento proceden de los instrumentos anteriores. Cada ciclo guarda una copia de los ajustes seleccionados. Estos controles son preparatorios y aún no modifican capturas ni las curvas simuladas.

La gráfica única permite elegir transmisión o fluorómetro. En fluorómetro aparece la selección de fuente azul, naranja o infrarroja. La simulación solo contiene lecturas para azul y lo indica para las otras fuentes. El intervalo de visualización se elige en píxeles para transmisión y en nm para fluorescencia. El CSV conserva todos los canales y los datos originales. Los controles de captura de oscuro, blanco y calibración aparecen deshabilitados hasta integrar la captura real.

## Qué queda registrado

- Las carpetas por defecto son `~/.local/share/cruz/simulado` y `~/.local/share/cruz/ambiental`. Cada una contiene `cruz.sqlite3`. `--output` permite usar otra carpeta. Una carpeta abierta en un modo rechaza el otro.
- Cada ciclo conserva identificador, inicio y fin UTC, duración monotónica, configuración, datos originales disponibles y fallos. Un ciclo que queda abierto tras una interrupción aparece como interrumpido en el siguiente arranque.
- Solo hay un ciclo a la vez. El botón manual reinicia la cuenta hasta el siguiente ciclo automático. El ajuste ordinario entra en el siguiente ciclo y se conserva tras reiniciar. El arranque mide de inmediato si la opción automática está activa.
- El tiempo proviene del reloj del sistema y se marca como no verificado. La cadencia usa un reloj monotónico. La sincronización, el despertar por RTC, y el corte de alimentación quedan pendientes.
- El modo de banco actual mide temperatura y conductividad. La secuencia óptica, luces y bomba todavía no se integran en el modo real. Las lecturas del banco actual sirven para comprobar comunicación y comportamiento, con calibración por patrón pendiente.
