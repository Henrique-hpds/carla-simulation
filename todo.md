- Off-screen mode: Unreal Engine is working as usual, rendering is computed but there is no display available. GPU based sensors return data.
    - aparentemente o dockerfile já faz isso
    - ./CarlaUE4.sh -RenderOffScreen
    - Funcionando

- Tentar pegar dados, plotar com matplotlib e exportar para csv

- Amostrar na taxa de Nyquist?
    - Pegar dados já coletados, aplicar fft, calcular ws =2wm e Ts = pi/wm 

- Dados espúrios - Tratado

- Carro para no sinal vermelho
    - Melhorar plot usando gradiente

- Perguntas
    - Como validar os dados obtidos
    - Como definir uma métrica para avaliar a qualidade dos dados sintéticos?
    - É necessário tratar no dominio da frequência? (Dados espúrios)

