import random
import carla
import os
import time

from modules.Camera import Camera
from datetime import datetime

def main():

    camera_drone = None
    camera_media = None
    camera_carro = None

    sensores = [camera_drone, camera_media, camera_carro]
    agentes = []

    try:

        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)

        if not os.path.exists(xodr_path):
            print(f"Arquivo {xodr_path} não encontrado!")
            return

        with open(xodr_path, 'r') as od_file:
            xodr_data = od_file.read()

        vertex_distance = 2.0  # in meters
        max_road_length = 500.0 # in meters
        wall_height = 0.0      # in meters
        extra_width = 0.6      # in meters
        world = client.generate_opendrive_world(xodr_data, carla.OpendriveGenerationParameters(vertex_distance=vertex_distance, max_road_length=max_road_length, wall_height=wall_height, additional_width=extra_width, smooth_junctions=True, enable_mesh_visibility=True))

        # client.generate_opendrive_world(xodr_data)
        print(f"Mapa {xodr_path} personalizado carregado com sucesso!")

        # Conecta ao mundo
        world = client.get_world()

        # map = world.get_map()

        # print(map)

        settings = world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = tick_time

        world.apply_settings(settings)

        # Obtém a biblioteca de blueprints
        blueprint_library = world.get_blueprint_library()

        # Seleciona um veículo aleatório
        vehicle_bp = blueprint_library.filter('vehicle.*')

        # Define a posição inicial do veículo
        spawn_points = world.get_map().get_spawn_points()
        if not spawn_points:
            print("Nenhum ponto de spawn disponível no mapa!")
            return
        
        for _ in range(1):  # Adiciona 10/10 veículos NPC
            vehicle_2 = world.try_spawn_actor(random.choice(vehicle_bp), random.choice(spawn_points))
            if vehicle_2 is not None:
                agentes.append(vehicle_2)
                vehicle_2.set_autopilot(True)
        # Spawna o veículo
        vehicle = world.spawn_actor(random.choice(vehicle_bp), random.choice(spawn_points))

        if vehicle is not None:
            agentes.append(vehicle)
            print(f"Veículo {vehicle.type_id} spawnado com sucesso!")
        else:
            print("Falha ao spawnar o veículo!")
            return

        # Configura o controlador automático para o veículo
        vehicle.set_autopilot(True)


        timestamp = datetime.now().strftime('%d-%m-%Y_%Hh-%Mm-%Ss')
        experiment_dir = f'data/exp_{timestamp}'
        filename = experiment_dir + '/data.csv'

        if not os.path.exists(experiment_dir):
            os.makedirs(experiment_dir)

        camera_drone = Camera("drone", world, 0, 0, 1000, -90, vehicle)
        camera_media = Camera("media", world, 0, 0, 100, -90, vehicle)
        camera_carro = Camera("carro", world, 0, 0, 2, 0, vehicle)

        camera_drone.start(experiment_dir)
        camera_media.start(experiment_dir)
        camera_carro.start(experiment_dir)

        world_time = 0
        while world_time < sim_time:
            world_time += tick_time
            world.tick()
            time.sleep(tick_time)

        camera_drone.stop()
        camera_media.stop()
        camera_carro.stop()
        print("Captura de imagens finalizada.")

    finally:

        for sensor in sensores:
            if sensor is not None:
                sensor.destroy()
                print(f"Sensor {sensor} destruído.")
            else:
                print(f"Sensor {sensor} já destruído ou não inicializado.")

        for agent in agentes:
            if agent is not None:
                agent.destroy()
                print(f"Agente {agent} destruído.")
            else:
                print(f"Agente já destruído ou não inicializado.")

        print("Finalizado e atores destruídos.")

if __name__ == '__main__':
    xodr_path = 'map.xodr'
    sim_time = 100
    tick_time = 0.5 # taxa de amostragem
    main()