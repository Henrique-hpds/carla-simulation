- Off-screen mode: Unreal Engine is working as usual, rendering is computed but there is no display available. GPU based sensors return data.
    - aparentemente o dockerfile já faz isso
    - ./CarlaUE4.sh -RenderOffScreen
    - Funcionando

- Tentar pegar dados, plotar com matplotlib e exportar para csv

- Amostrar na taxa de Nyquist?
    - Pegar dados já coletados, aplicar fft, calcular ws =2wm e Ts = pi/wm 