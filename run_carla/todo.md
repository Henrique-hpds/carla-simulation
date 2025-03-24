- Off-screen mode: Unreal Engine is working as usual, rendering is computed but there is no display available. GPU based sensors return data.
    - aparentemente o dockerfile já faz isso
    - ./CarlaUE4.sh -RenderOffScreen
    - Funcionando

- Tentar pegar dados, plotar com matplotlib e exportar para csv

- Amostrar na taxa de Nyquist?
    - Pegar dados já coletados, aplicar fft, calcular ws =2wm e Ts = pi/wm 

- Erros inertial data

WARNING: sensor object went out of the scope but the sensor is still alive in the simulation: Actor 198 (sensor.other.gnss) 
WARNING: sensor object went out of the scope but the sensor is still alive in the simulation: Actor 199 (sensor.other.imu) 
terminate called without an active exception
terminate called recursively
Abortado (imagem do núcleo gravada)

- Arrumar csv e plotar gráficos