import pandas as pd
import string
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

# Messages:
# SYS_STATUS, VIBRATION, SERVO_OUTPUT_RAW, HIGHRES_IMU, ATTITUDE, ATTITUDE_QUATERNION
# ESTIMATOR_STATUS, VFR_HUD, LOCAL_POS_NED

# Make sure to change bucket, org, url and token


# MAVLink message input data
print ("SYS_STATUS")
SYS_STATUS = pd.read_csv("../../Drone IDS/DOS/SYS_STATUS.csv")
print (SYS_STATUS.iloc[0,:])

print ("VIBRATION")
VIBRATION = pd.read_csv("../../Drone IDS/DOS/VIBRATION.csv")
print (VIBRATION.iloc[0,:])

print ("SERVO_OUTPUT_RAW")
SERVO_OUTPUT_RAW = pd.read_csv("../../Drone IDS/DOS/SERVO_OUTPUT_RAW.csv")
print (SERVO_OUTPUT_RAW.iloc[0,:])

print ("HIGHRES_IMU")
HIGHRES_IMU = pd.read_csv("../../Drone IDS/DOS/HIGHRES_IMU.csv")
print (HIGHRES_IMU.iloc[0,:])

print ("ATTITUDE")
ATTITUDE = pd.read_csv("../../Drone IDS/DOS/ATTITUDE.csv")
print (ATTITUDE.iloc[0,:])

print ("ATTITUDE_QUATERNION")
ATTITUDE_QUATERNION = pd.read_csv("../../Drone IDS/DOS/ATTITUDE_QUATERNION.csv")
print (ATTITUDE_QUATERNION.iloc[0,:])

print ("ESTIMATOR_STATUS")
ESTIMATOR_STATUS = pd.read_csv("../../Drone IDS/GPS/ESTIMATOR_STATUS.csv")
print (ESTIMATOR_STATUS.iloc[0,:])

print ("VFR_HUD")
VFR_HUD = pd.read_csv("../../Drone IDS/GPS/VFR_HUD.csv")
print (VFR_HUD.iloc[0,:])

print ("LOCAL_POSITION_NED")
LOCAL_POSITION_NED = pd.read_csv("../../Drone IDS/GPS/LOCAL_POSITION_NED.csv")
print (LOCAL_POSITION_NED.iloc[0,:])

# Omar's local influx
# bucket = "edf58ae3ffbc46dd"
# org = "565ddff2e29c416a"
# token = "Ad_35XsfmrHT-1mevYf5iuMkWum8NGyCPh2hC3SxvlQdU0wXteCKumFkm5NTrL2dD3bg3JpniiQjW2iBC1kYXw=="
#
# client =InfluxDBClient(
#     url="http://localhost:9999",
#     token="Ad_35XsfmrHT-1mevYf5iuMkWum8NGyCPh2hC3SxvlQdU0wXteCKumFkm5NTrL2dD3bg3JpniiQjW2iBC1kYXw==",
#     org="565ddff2e29c416a"
# )

# Cloud Influx | Test bucket
bucket = "a4aff0ec5f602f9a"
org = "2bf2125883ed70f6"
token = "PUT TOKEN"

client =InfluxDBClient(
    url="https://us-west-2-1.aws.cloud2.influxdata.com",
    token="PUT TOKEN",
    org="2bf2125883ed70f6"
)

write_api = client.write_api(write_options=SYNCHRONOUS)



def record_creator(point, tags, fields, row):
    records = []

    for feature in fields:
        records.append(Point(point).tag(tags[0], tags[1]).field(feature, row[feature]))

    return records


# SYS STATUS
sys_status_features = ['load',
                        'onboard_control_sensors_enabled',
                        'drop_rate_comm', 'errors_count3',
                        'errors_count1', 'errors_comm',
                        'errors_count2',
                        'onboard_control_sensors_present',
                        'voltage_battery',
                        'battery_remaining',
                        'errors_count4',
                        'onboard_control_sensors_health',
                        'current_battery']
for index, row in SYS_STATUS.iterrows():
    records = record_creator('my_measurement', ['MAV_message', 'SYS_STATUS'], sys_status_features, row)
    write_api.write(bucket=bucket, org=org, record=records)

print ("sys status")


# VIBRATION 6
vibration_features = ['clipping_2',
                        'vibration_x',
                        'clipping_0',
                        'vibration_z',
                        'clipping_1',
                        'vibration_y']
for index, row in VIBRATION.iterrows():
    records = record_creator('my_measurement', ['MAV_message', 'VIBRATION'], vibration_features, row)
    write_api.write(bucket=bucket, org=org, record=records)

print ("vibration done")

# SERVO_OUTPUT_RAW 9
servo_output_raw_vibration_features = ["servo3_raw",
                                        "servo6_raw",
                                        "servo4_raw",
                                        "servo1_raw",
                                        "servo2_raw",
                                        "servo7_raw",
                                        "port",
                                        "servo5_raw",
                                        "servo8_raw"]
for index, row in SERVO_OUTPUT_RAW.iterrows():
    records = record_creator('my_measurement', ['MAV_message', 'SERVO_OUTPUT_RAW'], servo_output_raw_vibration_features, row)
    write_api.write(bucket=bucket, org=org, record=records)

print ("SERVO_OUTPUT_RAW done")


# HIGHRES_IMU 14
highres_imu_features = ['zacc',
                        'xmag',
                        'diff_pressure',
                        'ymag',
                        'xacc',
                        'pressure_alt',
                        'abs_pressure',
                        'fields_updated',
                        'temperature',
                        'zmag',
                        'ygyro',
                        'xgyro',
                        'yacc',
                        'zgyro']
for index, row in HIGHRES_IMU.iterrows():
    records = record_creator('my_measurement', ['MAV_message', 'HIGHRES_IMU'], highres_imu_features, row)
    write_api.write(bucket=bucket, org=org, record=records)

print ("HIGHRES_IMU done")

# ATTITUDE 7
attitude_features = ['time_boot_ms',
                    'pitch',
                    'yawspeed',
                    'pitchspeed',
                    'yaw',
                    'rollspeed',
                    'roll']
for index, row in ATTITUDE.iterrows():
    records = record_creator('my_measurement', ['MAV_message', 'ATTITUDE'], attitude_features, row)
    write_api.write(bucket=bucket, org=org, record=records)

print ("ATTITUDE done")


attitude_quaternion_features = ['time_boot_ms',
                                'pitchspeed',
                                'yawspeed',
                                'q2',
                                'q1',
                                'q4',
                                'rollspeed',
                                'q3']
# ATTITUDE_QUATERNION 8
for index, row in ATTITUDE_QUATERNION.iterrows():
    records = record_creator('my_measurement', ['MAV_message', 'ATTITUDE_QUATERNION'], attitude_quaternion_features, row)
    write_api.write(bucket=bucket, org=org, record=records)

print ("ATTITUDE_QUATERNION done")

estimator_status_features = ['pos_vert_accuracy',
                            'mag_ratio',
                            'hagl_ratio',
                            'pos_horiz_ratio',
                            'pos_vert_ratio',
                            'time_usec',
                            'vel_ratio',
                            'flags',
                            'tas_ratio',
                            'pos_horiz_accuracy']
# ESTIMATOR_STATUS 10
for index, row in ESTIMATOR_STATUS.iterrows():
    records = record_creator('my_measurement', ['MAV_message', 'ESTIMATOR_STATUS'], estimator_status_features, row)
    write_api.write(bucket=bucket, org=org, record=records)
print ("ESTIMATOR_STATUS done")


vfr_hud_features = ['climb',
                    'throttle',
                    'groundspeed',
                    'alt',
                    'airspeed',
                    'heading']
# VFR_HUD 6
for index, row in VFR_HUD.iterrows():
    records = record_creator('my_measurement', ['MAV_message', 'VFR_HUD'], vfr_hud_features, row)
    write_api.write(bucket=bucket, org=org, record=records)
print ("VFR_HUD done")


local_position_ned_features = ['z',
                                'time_boot_ms',
                                'vy',
                                'vz',
                                'x',
                                'vx',
                                'y']
# LOCAL_POSITION_NED 7
for index, row in LOCAL_POSITION_NED.iterrows():
    records = record_creator('my_measurement', ['MAV_message', 'LOCAL_POSITION_NED'], local_position_ned_features, row)
    write_api.write(bucket=bucket, org=org, record=records)


print ("LOCAL_POSITION_NED done")
