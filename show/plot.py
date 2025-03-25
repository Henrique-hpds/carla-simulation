from matplotlib import pyplot as plt
from carla import Vector3D
import csv

def plot_gnss(filename: str):

    time = []
    latitudes = []
    longitudes = []
    altitudes = []

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            time.append(float(row['time']))
            latitudes.append(float(row['latitude']))
            longitudes.append(float(row['longitude']))
            altitudes.append(float(row['altitude']))

    plt.figure(figsize=(15, 10))

    plt.plot(time, latitudes, label='Latitude', color='blue')
    plt.plot(time, longitudes, label='Longitude', color='orange')
    plt.plot(time, altitudes, label='Altitude', color='green')

    plt.xlabel('Time (s)')
    plt.ylabel('Coordinates (m)')
    plt.legend()
    plt.title('Latitude, Longitude, and Altitude over Time')

    plt.tight_layout()
    plt.savefig('plots/gnss.png')

def plot_accel(filename: str):
    time = []
    accel_x = []
    accel_y = []
    accel_z = []

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            time.append(float(row['time']))
            accel_x.append(float(row['accel_x']))
            accel_y.append(float(row['accel_y']))
            accel_z.append(float(row['accel_z']))

    plt.figure(figsize=(15, 10))

    plt.plot(time, accel_x, label='Accel X', color='red')
    plt.plot(time, accel_y, label='Accel Y', color='green')
    plt.plot(time, accel_z, label='Accel Z', color='blue')

    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s²)')
    plt.legend()
    plt.title('Acceleration over Time')

    plt.tight_layout()
    plt.savefig('plots/accel.png')

def plot_gyro(filename: str):
    time = []
    gyro_x = []
    gyro_y = []
    gyro_z = []

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            time.append(float(row['time']))
            gyro_x.append(float(row['gyro_x']))
            gyro_y.append(float(row['gyro_y']))
            gyro_z.append(float(row['gyro_z']))

    plt.figure(figsize=(15, 10))

    plt.plot(time, gyro_x, label='Gyro X', color='red')
    plt.plot(time, gyro_y, label='Gyro Y', color='green')
    plt.plot(time, gyro_z, label='Gyro Z', color='blue')

    plt.xlabel('Time (s)')
    plt.ylabel('Angular Velocity (rad/s)')
    plt.legend()
    plt.title('Gyroscope Data over Time')

    plt.tight_layout()
    plt.savefig('plots/gyro.png')

def plot_gps(filename: str):
    time = []
    gps_x = []
    gps_y = []
    gps_z = []

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            time.append(float(row['time']))
            gps_x.append(float(row['gps_x']))
            gps_y.append(float(row['gps_y']))
            gps_z.append(float(row['gps_z']))

    plt.figure(figsize=(15, 10))

    plt.plot(time, gps_x, label='GPS X', color='red')
    plt.plot(time, gps_y, label='GPS Y', color='green')
    plt.plot(time, gps_z, label='GPS Z', color='blue')

    plt.xlabel('Time (s)')
    plt.ylabel('GPS Coordinates (m)')
    plt.legend()
    plt.title('GPS Data over Time')

    plt.tight_layout()
    plt.savefig('plots/gps.png')

def plot_compass(filename: str):
    time = []
    compass = []

    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            time.append(float(row['time']))
            compass.append(float(row['compass']))

    plt.figure(figsize=(15, 10))

    plt.plot(time, compass, label='Compass', color='purple')

    plt.xlabel('Time (s)')
    plt.ylabel('Compass (degrees)')
    plt.legend()
    plt.title('Compass Data over Time')

    plt.tight_layout()
    plt.savefig('plots/compass.png')