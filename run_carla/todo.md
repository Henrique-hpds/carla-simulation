- Off-screen mode: Unreal Engine is working as usual, rendering is computed but there is no display available. GPU based sensors return data.
    - aparentemente o dockerfile já faz isso
    - ./CarlaUE4.sh -RenderOffScreen
    - Funcionando

- Tentar pegar dados, plotar com matplotlib e exportar para csv