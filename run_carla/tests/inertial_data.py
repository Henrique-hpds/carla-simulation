import carla
import random
import sys
import os
from time import sleep


try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)

    world = client.load_world('Town01')
    blueprint_library = world.get_blueprint_library()

    vehicle_blueprints = blueprint_library.filter('vehicle.ford.mustang')
    spawn_points = world.get_map().get_spawn_points()
    ego_vehicle = world.spawn_actor(random.choice(vehicle_blueprints), random.choice(spawn_points))
    ego_vehicle.set_autopilot(True)

    print('created %s' % ego_vehicle.type_id)

    actor_list = [ego_vehicle]

    # --------------
    # Add GNSS sensor to ego vehicle. 
    # --------------

    gnss_bp = blueprint_library.find('sensor.other.gnss')
    gnss_location = carla.Location(0,0,0)
    gnss_rotation = carla.Rotation(0,0,0)
    gnss_transform = carla.Transform(gnss_location,gnss_rotation)
    gnss_bp.set_attribute("sensor_tick",str(3.0))
    ego_gnss = world.spawn_actor(gnss_bp,gnss_transform,attach_to=ego_vehicle, attachment_type=carla.AttachmentType.Rigid)
    actor_list.append(ego_gnss)
    print('created %s' % ego_gnss.type_id)

    def gnss_callback(gnss):
        print("GNSS measure:\n"+str(gnss)+'\n')
    ego_gnss.listen(lambda gnss: gnss_callback(gnss))

    # --------------
    # Add IMU sensor to ego vehicle. 
    # --------------

    imu_bp = blueprint_library.find('sensor.other.imu')
    imu_location = carla.Location(0,0,0)
    imu_rotation = carla.Rotation(0,0,0)
    imu_transform = carla.Transform(imu_location,imu_rotation)
    imu_bp.set_attribute("sensor_tick",str(3.0))
    ego_imu = world.spawn_actor(imu_bp,imu_transform,attach_to=ego_vehicle, attachment_type=carla.AttachmentType.Rigid)
    actor_list.append(ego_imu)
    print('created %s' % ego_imu.type_id)

    def imu_callback(imu):
        print("IMU measure:\n"+str(imu)+'\n')
    ego_imu.listen(lambda imu: imu_callback(imu))

    while True:
        sleep(1)

except KeyboardInterrupt:
    pass
finally:
    client.apply_batch([carla.command.DestroyActor(x) for x in actor_list])
