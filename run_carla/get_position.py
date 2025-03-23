import time
import carla
import random
import csv
import matplotlib.pyplot as plt

client = carla.Client('localhost', 2000)
client.set_timeout(2.0)

world = client.load_world('Town01')

vehicle_blueprints = world.get_blueprint_library().filter('*vehicle*')
spawn_points = world.get_map().get_spawn_points()
ego_vehicle = world.spawn_actor(random.choice(vehicle_blueprints), random.choice(spawn_points))
ego_vehicle.set_autopilot(True)

pontos = []

start_time = time.time()
while time.time() - start_time < 300: # n_pontos
    current_time = time.time() - start_time
    location = ego_vehicle.get_location()
    pontos.append((current_time, location.x, location.y))
    print(f"time={current_time}, x={location.x}, y={location.y}")
    time.sleep(1) # periodo de amostragem

# Plot the points and save the figure
x_coords, y_coords = [p[1] for p in pontos], [p[2] for p in pontos]
plt.figure()
plt.plot(x_coords, y_coords, marker='o')
plt.title('Actor Movement')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.grid(True)
plt.savefig('actor_movement.png')

with open('actor_positions.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time', 'X Coordinate', 'Y Coordinate'])
    writer.writerows(pontos)