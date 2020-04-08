import pandas as pd
import string
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

# Messages:
# SYS_STATUS, VIBRATION, SERVO_OUTPUT_RAW, HIGHRES_IMU, ATTITUDE, ATTITUDE_QUATERNION
# https://www.influxdata.com/blog/getting-started-with-python-and-influxdb-v2-0/
# Make sure to change bucket, org, url and token

bucket = "edf58ae3ffbc46dd"
org = "565ddff2e29c416a"
token = "Ad_35XsfmrHT-1mevYf5iuMkWum8NGyCPh2hC3SxvlQdU0wXteCKumFkm5NTrL2dD3bg3JpniiQjW2iBC1kYXw=="

client =InfluxDBClient(
    url="http://localhost:9999",
    token="Ad_35XsfmrHT-1mevYf5iuMkWum8NGyCPh2hC3SxvlQdU0wXteCKumFkm5NTrL2dD3bg3JpniiQjW2iBC1kYXw==",
    org="565ddff2e29c416a"
)

query_api = client.query_api()

# DoS
# range = "1050ms"

# GPS
# range = "-250ms"

# Testing
range = "-30d"

# Define all MAVLink messages and their features that you would like to load
feautres = {    "VIBRATION": ["vibration_x", "vibration_y"],
                "SYS_STATUS": ["load"],
                "SERVO_OUTPUT_RAW": ["servo1_raw", "servo3_raw", "servo5_raw", "servo6_raw"],
                "HIGHRES_IMU": ["xgyro", "yacc"],
                "ATTITUDE": ["pitch", "rollspeed"],
                "ATTITUDE_QUATERNION": ["q3"]
                }


final = {}

# Will append value to dictionary
for key, value in feautres.items():
    for feature in value:
        query = 'from(bucket: "mav")\
          |> range(start: '+ range + ' )\
          |> filter(fn: (r) => r.MAV_message == "'+ key +'")\
          |> filter(fn: (r) => r._field == "'+  feature +'")\
          |> filter(fn: (r) => r._measurement == "my_measurement")'

        result = client.query_api().query(org=org, query=query)
        for table in result:
            results = []
            for record in table.records:
                results.append(record.get_value())
                break
            final[key+"-"+feature] = results

# Outputs values
for key, value in final.items():
    print (key, value)
    print ("\n\n")
