# Prediction for DoS messages. Be sure to change model_file to correct full path

from DoS_influx_reader import *
from prediction import *

# DoS
# range = "1050ms"

# GPS
# range = "-250ms"

# Testing
range = "-30d"

# Define all MAVLink messages and their features that you would like to load
# These are all the features for DoS
features = {    "VIBRATION": ["vibration_x", "vibration_y"],
                "SYS_STATUS": ["load"],
                "SERVO_OUTPUT_RAW": ["servo1_raw", "servo3_raw", "servo5_raw", "servo6_raw"],
                "HIGHRES_IMU": ["xgyro", "yacc"],
                "ATTITUDE": ["pitch", "rollspeed"],
                "ATTITUDE_QUATERNION": ["q3"]
                }

# Full path to saved model file using pickle
model_file = "/Users/omarm/OneDrive/Threat Intelligence/MAVIDS/GCS Client/gcsclient/finalized_model.sav"

# Pull MAVLink message data from InfluxDB
MAVLink_messages = influx_reader(features, range)

# Determine if MAVLink message is malicous or benign
make_prediction(features, MAVLink_messages, model_file)
