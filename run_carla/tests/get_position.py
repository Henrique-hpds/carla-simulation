import time
import carla
import random
import csv
import sys
import os
import matplotlib.pyplot as plt
from datetime import datetime
from pprint import pprint

def get_position(sample_rate = 0.5, sim_time = 300, save_data = True):
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)

    world = client.load_world('Town01')
    vehicle_blueprints = world.get_blueprint_library().filter('vehicle.ford.mustang')
    spawn_points = world.get_map().get_spawn_points()
    ego_vehicle = world.spawn_actor(random.choice(vehicle_blueprints), random.choice(spawn_points))
    ego_vehicle.set_autopilot(True)

    print('created %s' % ego_vehicle.type_id)

    actor_list = [ego_vehicle]
    pontos = []

    start_time = time.time()
    while time.time() - start_time < sim_time:
        current_time = time.time() - start_time
        location = ego_vehicle.get_location()
        pontos.append((current_time, location.x, location.y))
        print(f"time={current_time}, x={location.x}, y={location.y}")
        time.sleep(sample_rate)

    if save_data:
        # Create the new experiment directory with a timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        experiment_dir = f'position_data/exp_{timestamp}'
        os.makedirs(experiment_dir)

        # Plot the points and save the figure
        x_coords, y_coords = [p[1] for p in pontos], [p[2] for p in pontos]
        plt.figure()
        plt.plot(x_coords, y_coords, marker='o')
        plt.title('Actor Movement')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.grid(True)
        plt.savefig(experiment_dir + '/actor_movement.png')

        with open(experiment_dir + '/actor_positions.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Time', 'X Coordinate', 'Y Coordinate'])
            writer.writerows(pontos)

    for actor in actor_list:
        actor.destroy()

if __name__ == '__main__':
    get_position(sim_time=100)