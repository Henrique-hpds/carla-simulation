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

def plot_inercial_data(data, experiment_dir, save_plot_data=True):
    pass

def inertial_data(tick = 0.05, sim_time = 300, town='Town01', vehicle='vehicle.ford.mustang', save_data=True, plot_data=True):

    gnss_data_list = []
    imu_data_list = []
    
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
        actor_list = [ego_vehicle]

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
            timestamp = time()
            gnss_data_list.append([timestamp, 'GNSS', gnss.latitude, gnss.longitude, gnss.altitude])
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
            timestamp = time()
            imu_data_list.append([timestamp, 'IMU', imu.accelerometer, imu.gyroscope, imu.compass])
            print("IMU measure:\n"+str(imu)+'\n')
        ego_imu.listen(lambda imu: imu_callback(imu))

        timestamp = datetime.now().strftime('%d-%m-%Y_%Hh-%Mm-%Ss')
        experiment_dir = f'data/exp_{timestamp}'
        gnss_filename = experiment_dir + '/gnss_data.csv'
        imu_filename = experiment_dir + '/imu_data.csv'

        if save_data:
            os.makedirs(experiment_dir)

        count = 0
        while count < sim_time:
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
            plot_inercial_data(gnss_data, experiment_dir)
            plot_inercial_data(imu_data, experiment_dir)

    except KeyboardInterrupt:
        client.apply_batch([carla.command.DestroyActor(x) for x in actor_list])

if __name__ == "__main__":
    inertial_data(sim_time=5)