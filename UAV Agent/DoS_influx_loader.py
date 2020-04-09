import pandas as pd
import string
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

# Messages:
# SYS_STATUS, VIBRATION, SERVO_OUTPUT_RAW, HIGHRES_IMU, ATTITUDE, ATTITUDE_QUATERNION

# Make sure to change bucket, org, url and token


# convert sample data to line protocol (with nanosecond precision)
print ("SYS_STATUS")
SYS_STATUS = pd.read_csv("SYS_STATUS.csv")
print (SYS_STATUS.iloc[0,:])

print ("VIBRATION")
VIBRATION = pd.read_csv("VIBRATION.csv")
print (VIBRATION.iloc[0,:])

print ("SERVO_OUTPUT_RAW")
SERVO_OUTPUT_RAW = pd.read_csv("SERVO_OUTPUT_RAW.csv")
print (SERVO_OUTPUT_RAW.iloc[0,:])

print ("HIGHRES_IMU")
HIGHRES_IMU = pd.read_csv("HIGHRES_IMU.csv")
print (HIGHRES_IMU.iloc[0,:])


print ("ATTITUDE")
ATTITUDE = pd.read_csv("ATTITUDE.csv")
print (ATTITUDE.iloc[0,:])

print ("ATTITUDE_QUATERNION")
ATTITUDE_QUATERNION = pd.read_csv("ATTITUDE_QUATERNION.csv")
print (ATTITUDE_QUATERNION.iloc[0,:])


bucket = "edf58ae3ffbc46dd"
org = "565ddff2e29c416a"
token = "Ad_35XsfmrHT-1mevYf5iuMkWum8NGyCPh2hC3SxvlQdU0wXteCKumFkm5NTrL2dD3bg3JpniiQjW2iBC1kYXw=="

client =InfluxDBClient(
    url="http://localhost:9999",
    token="Ad_35XsfmrHT-1mevYf5iuMkWum8NGyCPh2hC3SxvlQdU0wXteCKumFkm5NTrL2dD3bg3JpniiQjW2iBC1kYXw==",
    org="565ddff2e29c416a"
)

write_api = client.write_api(write_options=SYNCHRONOUS)

# SYS STATUS
for index, row in SYS_STATUS.iterrows():
	load = Point("my_measurement").tag("MAV_message", "SYS_STATUS").field("load", row['load'])
	onboard_control_sensors_enabled = Point("my_measurement").tag("MAV_message", "SYS_STATUS").field("onboard_control_sensors_enabled", row['onboard_control_sensors_enabled'])
	drop_rate_comm = Point("my_measurement").tag("MAV_message", "SYS_STATUS").field("drop_rate_comm", row['drop_rate_comm'])
	errors_count3 = Point("my_measurement").tag("MAV_message", "SYS_STATUS").field("errors_count3", row['errors_count3'])
	errors_count1 = Point("my_measurement").tag("MAV_message", "SYS_STATUS").field("errors_count1", row['errors_count1'])
	errors_comm = Point("my_measurement").tag("MAV_message", "SYS_STATUS").field("errors_comm", row['errors_comm'])
	errors_count2 = Point("my_measurement").tag("MAV_message", "SYS_STATUS").field("errors_count2", row['errors_count2'])
	onboard_control_sensors_present = Point("my_measurement").tag("MAV_message", "SYS_STATUS").field("onboard_control_sensors_present", row['onboard_control_sensors_present'])
	voltage_battery = Point("my_measurement").tag("MAV_message", "SYS_STATUS").field("voltage_battery", row['voltage_battery'])
	battery_remaining = Point("my_measurement").tag("MAV_message", "SYS_STATUS").field("battery_remaining", row['battery_remaining'])
	errors_count4 = Point("my_measurement").tag("MAV_message", "SYS_STATUS").field("errors_count4", row['errors_count4'])
	onboard_control_sensors_health = Point("my_measurement").tag("MAV_message", "SYS_STATUS").field("onboard_control_sensors_health", row['onboard_control_sensors_health'])
	current_battery = Point("my_measurement").tag("MAV_message", "SYS_STATUS").field("current_battery", row['current_battery'])

	write_api.write(bucket=bucket, org=org, record=[load, onboard_control_sensors_enabled, drop_rate_comm, errors_count3, errors_count1, errors_comm, errors_count2, onboard_control_sensors_present, voltage_battery, battery_remaining, errors_count4, onboard_control_sensors_health, current_battery])

# VIBRATION 6
for index, row in VIBRATION.iterrows():
	vibration_x = Point("my_measurement").tag("MAV_message", "VIBRATION").field("vibration_x", row['vibration_x'])
	clipping_2 = Point("my_measurement").tag("MAV_message", "VIBRATION").field("clipping_2", row['clipping_2'])
	clipping_0 = Point("my_measurement").tag("MAV_message", "VIBRATION").field("clipping_0", row['clipping_0'])
	vibration_z = Point("my_measurement").tag("MAV_message", "VIBRATION").field("vibration_z", row['vibration_z'])
	clipping_1 = Point("my_measurement").tag("MAV_message", "VIBRATION").field("clipping_1", row['clipping_1'])
	vibration_y = Point("my_measurement").tag("MAV_message", "VIBRATION").field("vibration_y", row['vibration_y'])

	write_api.write(bucket=bucket, org=org, record=[vibration_x,
													clipping_2,
													clipping_0,
													vibration_z,
													clipping_1,
													vibration_y])

# SERVO_OUTPUT_RAW 9
for index, row in SERVO_OUTPUT_RAW.iterrows():
	servo3_raw = Point("my_measurement").tag("MAV_message", "SERVO_OUTPUT_RAW").field("servo3_raw", row['servo3_raw'])
	servo6_raw = Point("my_measurement").tag("MAV_message", "SERVO_OUTPUT_RAW").field("servo6_raw", row['servo6_raw'])
	servo4_raw = Point("my_measurement").tag("MAV_message", "SERVO_OUTPUT_RAW").field("servo4_raw", row['servo4_raw'])
	servo1_raw = Point("my_measurement").tag("MAV_message", "SERVO_OUTPUT_RAW").field("servo1_raw", row['servo1_raw'])
	servo2_raw = Point("my_measurement").tag("MAV_message", "SERVO_OUTPUT_RAW").field("servo2_raw", row['servo2_raw'])
	servo7_raw = Point("my_measurement").tag("MAV_message", "SERVO_OUTPUT_RAW").field("servo7_raw", row['servo7_raw'])
	port = Point("my_measurement").tag("MAV_message", "SERVO_OUTPUT_RAW").field("port", row['port'])
	servo5_raw = Point("my_measurement").tag("MAV_message", "SERVO_OUTPUT_RAW").field("servo5_raw", row['servo5_raw'])
	servo8_raw = Point("my_measurement").tag("MAV_message", "SERVO_OUTPUT_RAW").field("servo8_raw", row['servo8_raw'])

	write_api.write(bucket=bucket, org=org, record=[servo3_raw,
													servo6_raw,
													servo4_raw,
													servo1_raw,
													servo2_raw,
													servo7_raw,
													port,
													servo5_raw,
													servo8_raw])

# HIGHRES_IMU 14
for index, row in HIGHRES_IMU.iterrows():
	zacc = Point("my_measurement").tag("MAV_message", "HIGHRES_IMU").field("zacc", row['zacc'])
	xmag = Point("my_measurement").tag("MAV_message", "HIGHRES_IMU").field("xmag", row['xmag'])
	diff_pressure = Point("my_measurement").tag("MAV_message", "HIGHRES_IMU").field("diff_pressure", row['diff_pressure'])
	ymag = Point("my_measurement").tag("MAV_message", "HIGHRES_IMU").field("ymag", row['ymag'])
	xacc = Point("my_measurement").tag("MAV_message", "HIGHRES_IMU").field("xacc", row['xacc'])
	pressure_alt = Point("my_measurement").tag("MAV_message", "HIGHRES_IMU").field("pressure_alt", row['pressure_alt'])
	abs_pressure = Point("my_measurement").tag("MAV_message", "HIGHRES_IMU").field("abs_pressure", row['abs_pressure'])
	fields_updated = Point("my_measurement").tag("MAV_message", "HIGHRES_IMU").field("fields_updated", row['fields_updated'])
	temperature = Point("my_measurement").tag("MAV_message", "HIGHRES_IMU").field("temperature", row['temperature'])
	zmag = Point("my_measurement").tag("MAV_message", "HIGHRES_IMU").field("zmag", row['zmag'])
	ygyro = Point("my_measurement").tag("MAV_message", "HIGHRES_IMU").field("ygyro", row['ygyro'])
	xgyro = Point("my_measurement").tag("MAV_message", "HIGHRES_IMU").field("xgyro", row['xgyro'])
	yacc = Point("my_measurement").tag("MAV_message", "HIGHRES_IMU").field("yacc", row['yacc'])
	zgyro = Point("my_measurement").tag("MAV_message", "HIGHRES_IMU").field("zgyro", row['zgyro'])

	write_api.write(bucket=bucket, org=org, record=[zacc,
													xmag,
													diff_pressure,
													ymag,
													xacc,
													pressure_alt,
													abs_pressure,
													fields_updated,
													temperature,
													zmag,
													ygyro,
													xgyro,
													yacc,
													zgyro])

# VIBRATION 6
for index, row in VIBRATION.iterrows():
	vibration_x = Point("my_measurement").tag("MAV_message", "VIBRATION").field("vibration_x", row['vibration_x'])
	clipping_2 = Point("my_measurement").tag("MAV_message", "VIBRATION").field("clipping_2", row['clipping_2'])
	clipping_0 = Point("my_measurement").tag("MAV_message", "VIBRATION").field("clipping_0", row['clipping_0'])
	vibration_z = Point("my_measurement").tag("MAV_message", "VIBRATION").field("vibration_z", row['vibration_z'])
	clipping_1 = Point("my_measurement").tag("MAV_message", "VIBRATION").field("clipping_1", row['clipping_1'])
	vibration_y = Point("my_measurement").tag("MAV_message", "VIBRATION").field("vibration_y", row['vibration_y'])

	write_api.write(bucket=bucket, org=org, record=[vibration_x,
													clipping_2,
													clipping_0,
													vibration_z,
													clipping_1,
													vibration_y])

# ATTITUDE 7
for index, row in ATTITUDE.iterrows():
	time_boot_ms = Point("my_measurement").tag("MAV_message", "ATTITUDE").field("time_boot_ms", row['time_boot_ms'])
	pitch = Point("my_measurement").tag("MAV_message", "ATTITUDE").field("pitch", row['pitch'])
	yawspeed = Point("my_measurement").tag("MAV_message", "ATTITUDE").field("yawspeed", row['yawspeed'])
	pitchspeed = Point("my_measurement").tag("MAV_message", "ATTITUDE").field("pitchspeed", row['pitchspeed'])
	yaw = Point("my_measurement").tag("MAV_message", "ATTITUDE").field("yaw", row['yaw'])
	rollspeed = Point("my_measurement").tag("MAV_message", "ATTITUDE").field("rollspeed", row['rollspeed'])
	roll = Point("my_measurement").tag("MAV_message", "ATTITUDE").field("roll", row['roll'])

	write_api.write(bucket=bucket, org=org, record=[time_boot_ms,
													pitch,
													yawspeed,
													pitchspeed,
													yaw,
													rollspeed,
													roll])

# ATTITUDE_QUATERNION 8
for index, row in ATTITUDE_QUATERNION.iterrows():
	time_boot_ms = Point("my_measurement").tag("MAV_message", "ATTITUDE_QUATERNION").field("time_boot_ms", row['time_boot_ms'])
	pitchspeed = Point("my_measurement").tag("MAV_message", "ATTITUDE_QUATERNION").field("pitchspeed", row['pitchspeed'])
	yawspeed = Point("my_measurement").tag("MAV_message", "ATTITUDE_QUATERNION").field("yawspeed", row['yawspeed'])
	q2 = Point("my_measurement").tag("MAV_message", "ATTITUDE_QUATERNION").field("q2", row['q2'])
	q1 = Point("my_measurement").tag("MAV_message", "ATTITUDE_QUATERNION").field("q1", row['q1'])
	q4 = Point("my_measurement").tag("MAV_message", "ATTITUDE_QUATERNION").field("q4", row['q4'])
	rollspeed = Point("my_measurement").tag("MAV_message", "ATTITUDE_QUATERNION").field("rollspeed", row['rollspeed'])
	q3 = Point("my_measurement").tag("MAV_message", "ATTITUDE_QUATERNION").field("q3", row['q3'])

	write_api.write(bucket=bucket, org=org, record=[time_boot_ms,
													pitchspeed,
													yawspeed,
													q2,
													q1,
													q4,
													rollspeed,
													q3])
