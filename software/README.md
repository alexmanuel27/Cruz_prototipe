# Monitor local de Cruz

Primera versión para Python 3.11 o posterior en macOS o Raspberry Pi OS. El monitor programa los ciclos aunque se cierre el navegador. Guarda cada ciclo y los ajustes usados en SQLite. El panel permite configurar el intervalo, pausar la adquisición automática, pedir una medición y consultar el historial. Se actualiza cada dos segundos y ofrece un CSV del historial y los datos originales en JSON por ciclo.

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

## Qué queda registrado

- Las carpetas por defecto son `~/.local/share/cruz/simulado` y `~/.local/share/cruz/ambiental`. Cada una contiene `cruz.sqlite3`. `--output` permite usar otra carpeta. Una carpeta abierta en un modo rechaza el otro.
- Cada ciclo conserva identificador, inicio y fin UTC, duración monotónica, configuración, datos originales disponibles y fallos. Un ciclo que queda abierto tras una interrupción aparece como interrumpido en el siguiente arranque.
- Solo hay un ciclo a la vez. El botón manual reinicia la cuenta hasta el siguiente ciclo automático. El ajuste ordinario entra en el siguiente ciclo y se conserva tras reiniciar. El arranque mide de inmediato si la opción automática está activa.
- El tiempo proviene del reloj del sistema y se marca como no verificado. La cadencia usa un reloj monotónico. La sincronización, el despertar por RTC, y el corte de alimentación quedan pendientes.
- El modo de banco actual mide temperatura y conductividad. La secuencia óptica, luces y bomba todavía no se integran en el modo real. Las lecturas del banco actual sirven para comprobar comunicación y comportamiento, con calibración por patrón pendiente.
