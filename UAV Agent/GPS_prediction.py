# Prediction for GPS messages. Be sure to change model_file to correct full path

from influx_reader import *
from prediction import *

# DoS
# range = "1050ms"

# GPS
# range = "-250ms"

# Testing
range = "-30d"

# Define all MAVLink messages and their features that you would like to load
# These are all the features for DoS
features = {    "ESTIMATOR_STATUS": ["pos_horiz_ratio", "flags"],
                "VIBRATION": ["vibration_z"],
                "ATTITUDE_QUATERNION": ["q1", "q4"],
                "HIGHRES_IMU": ["xmag"],
                "ATTITUDE": ["yaw"],
                "VFR_HUD": ["heading"],
                "LOCAL_POSITION_NED" : ["vx"]
                }

# Full path to saved model file using pickle
model_file = "/Users/omarm/OneDrive/Threat Intelligence/MAVIDS/GCS Client/gcsclient/finalized_model.sav"

# Pull MAVLink message data from InfluxDB
MAVLink_messages = influx_reader(features, range)

# Determine if MAVLink message is malicous or benign
make_prediction(features, MAVLink_messages, model_file)
