from time import sleep, time
from datetime import datetime
import matplotlib.pyplot as plt
import random
import carla
import csv
import sys
import os

from carla import Vector3D

def read_data(file_path):
    data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data

def plot_gnss(gnss_data, experiment_dir):
    timestamps = [float(row[0]) for row in gnss_data[1:]]
    latitudes = [float(row[1]) for row in gnss_data[1:]]
    longitudes = [float(row[2]) for row in gnss_data[1:]]
    altitudes = [float(row[3]) for row in gnss_data[1:]]

    plt.figure(figsize=(10, 6))

    plt.subplot(3, 1, 1)
    plt.plot(timestamps, latitudes, label='Latitude')
    plt.xlabel('Timestamp (s)')
    plt.ylabel('Latitude (degrees)')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(timestamps, longitudes, label='Longitude')
    plt.xlabel('Timestamp (s)')
    plt.ylabel('Longitude (degrees)')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(timestamps, altitudes, label='Altitude')
    plt.xlabel('Timestamp (s)')
    plt.ylabel('Altitude (m)')
    plt.legend()

    plt.tight_layout()
    plt.savefig(f'{experiment_dir}/gnss_plot.png')

def plot_imu(imu_data, experiment_dir):
    timestamps = [float(row[0]) for row in imu_data[1:]]
    accelerometers = [eval(row[1]) for row in imu_data[1:]]
    gyroscopes = [eval(row[2]) for row in imu_data[1:]]
    compasses = [float(row[3]) for row in imu_data[1:]]

    accel_x = [accel.x for accel in accelerometers]
    accel_y = [accel.y for accel in accelerometers]
    accel_z = [accel.z for accel in accelerometers]

    gyro_x = [gyro.x for gyro in gyroscopes]
    gyro_y = [gyro.y for gyro in gyroscopes]
    gyro_z = [gyro.z for gyro in gyroscopes]

    # Plot Accelerometer Data
    plt.figure(figsize=(10, 12))

    plt.suptitle('Acceletometer Data')

    plt.subplot(3, 1, 1)
    plt.plot(timestamps, accel_x, label='Acceleration (m/s²)')
    plt.xlabel('Timestamp (s)')
    plt.ylabel('Acceleration X (m/s²)')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(timestamps, accel_y, label='Acceleration (m/s²)', color='orange')
    plt.xlabel('Timestamp (s)')
    plt.ylabel('Acceleration Y (m/s²)')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(timestamps, accel_z, label='Acceleration (m/s²)', color='green')
    plt.xlabel('Timestamp (s)')
    plt.ylabel('Acceleration Z (m/s²)')
    plt.legend()

    plt.tight_layout()
    plt.savefig(f'{experiment_dir}/accel_plot.png')

    # Plot Gyroscope Data
    plt.figure(figsize=(10, 12))

    plt.subplot(3, 1, 1)
    plt.plot(timestamps, gyro_x, label='Eixo X (rad/s)')
    plt.xlabel('Timestamp (s)')
    plt.ylabel('Gyroscope X (rad/s)')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(timestamps, gyro_y, label='Eixo Y (rad/s)', color='orange')
    plt.xlabel('Timestamp (s)')
    plt.ylabel('Gyroscope Y (rad/s)')
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(timestamps, gyro_z, label='Eixo Z (rad/s)', color='green')
    plt.xlabel('Timestamp (s)')
    plt.ylabel('Gyroscope Z (rad/s)')
    plt.legend()

    plt.tight_layout()
    plt.savefig(f'{experiment_dir}/gyro_plot.png')

    # Plot Compass Data
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, compasses, label='Compass')
    plt.xlabel('Timestamp (s)')
    plt.ylabel('Compass (degrees)')
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{experiment_dir}/compass_plot.png')

def inertial_data(tick = 0.05, sim_time = 300, town='Town01', vehicle='vehicle.ford.mustang', save_data=True, plot_data=True):

    gnss_data_list = []
    imu_data_list = []
    actor_list = []
    
    try:
        # conectar ao serverside do CARLA
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)

        world = client.load_world(town)
        blueprint_library = world.get_blueprint_library()

        # spawnar veículo
        vehicle_blueprints = blueprint_library.filter(vehicle)
        spawn_points = world.get_map().get_spawn_points()
        ego_vehicle = world.spawn_actor(random.choice(vehicle_blueprints), random.choice(spawn_points))
        ego_vehicle.set_autopilot(True)

        print('created %s' % ego_vehicle.type_id)

        # cria lista de atores
        # importante para destruir os atores ao final do script,
        # evitando que eles continuem ativos no simulador
        actor_list.append(ego_vehicle)

        # --------------
        # Add GNSS sensor to ego vehicle. 
        # --------------

        gnss_bp = blueprint_library.find('sensor.other.gnss')
        gnss_location = carla.Location(0,0,0)
        gnss_rotation = carla.Rotation(0,0,0)
        gnss_transform = carla.Transform(gnss_location,gnss_rotation)
        gnss_bp.set_attribute("sensor_tick",str(tick))
        ego_gnss = world.spawn_actor(gnss_bp,gnss_transform,attach_to=ego_vehicle, attachment_type=carla.AttachmentType.Rigid)
        actor_list.append(ego_gnss)
        print('created %s' % ego_gnss.type_id)

        def gnss_callback(gnss):
            gnss_data_list.append([gnss.timestamp, gnss.latitude, gnss.longitude, gnss.altitude])
            print("GNSS measure:\n"+str(gnss)+'\n')
        ego_gnss.listen(lambda gnss: gnss_callback(gnss))

        # --------------
        # Add IMU sensor to ego vehicle. 
        # --------------

        imu_bp = blueprint_library.find('sensor.other.imu')
        imu_location = carla.Location(0,0,0)
        imu_rotation = carla.Rotation(0,0,0)
        imu_transform = carla.Transform(imu_location,imu_rotation)
        imu_bp.set_attribute("sensor_tick",str(tick))
        ego_imu = world.spawn_actor(imu_bp,imu_transform,attach_to=ego_vehicle, attachment_type=carla.AttachmentType.Rigid)
        actor_list.append(ego_imu)
        print('created %s' % ego_imu.type_id)

        def imu_callback(imu):
            imu_data_list.append([imu.timestamp, imu.accelerometer, imu.gyroscope, imu.compass])
            print("IMU measure:\n"+str(imu)+'\n')
        ego_imu.listen(lambda imu: imu_callback(imu))

        timestamp = datetime.now().strftime('%d-%m-%Y_%Hh-%Mm-%Ss')
        experiment_dir = f'data/exp_{timestamp}'
        gnss_filename = experiment_dir + '/gnss_data.csv'
        imu_filename = experiment_dir + '/imu_data.csv'

        if save_data:
            os.makedirs(experiment_dir)
            with open(gnss_filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['timestamp', 'latitude', 'longitude', 'altitude'])
            with open(imu_filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['timestamp', 'accelerometer', 'gyroscope', 'compass'])
        
        count = 0
        while count <= sim_time:
            count += tick
            world.tick()  # Avança o simulador em um passo
            sleep(tick)
            if save_data:
                if gnss_data_list:
                    with open(gnss_filename, 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerows(gnss_data_list)
                        gnss_data_list.clear()
                if imu_data_list:
                    with open(imu_filename, 'a', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerows(imu_data_list)
                        imu_data_list.clear()
        

        if plot_data:
            gnss_data = read_data(gnss_filename)
            imu_data = read_data(imu_filename)
            plot_gnss(gnss_data, experiment_dir)
            plot_imu(imu_data, experiment_dir)

        print("Dados salvos em: ", experiment_dir)

    finally:
        for x in actor_list:
            if x is not None:
                x.destroy()

if __name__ == "__main__":
    inertial_data(sim_time=5)