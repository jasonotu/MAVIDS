import math
import pickle
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn import preprocessing
from sklearn import svm
from statistics import mean


# Takes data from influx and formats it with features. Also takes an average of
# all Messages
# params [dict] features: contains all the MAVLink messages (keys) and the
# name of their features (values). Example for DoS shown below.
# params [dict] message_data: contains data returned from influx db
# return [dict] ml_dict: formatted dictionary. Example below for DoS.
#
# Example of features param:
# features = {    "VIBRATION": ["vibration_x", "vibration_y"],
#                 "SYS_STATUS": ["load"],
#                 "SERVO_OUTPUT_RAW": ["servo1_raw", "servo3_raw", "servo5_raw", "servo6_raw"],
#                 "HIGHRES_IMU": ["xgyro", "yacc"],
#                 "ATTITUDE": ["pitch", "rollspeed"],
#                 "ATTITUDE_QUATERNION": ["q3"]
#
# Example of ml_dict return dict:
# ml_dict = {    'vibration_x': 3.179839902500703e-09,
#                'vibration_y': 8.991874201456085e-05,
#                'load': 417.2, 'servo1_raw': 0,
#                'servo3_raw': 0, 'servo5_raw': 0,
#                'servo6_raw': 0,
#                'xgyro': -0.001985228154808282,
#                'yacc': 0.01635252805426717,
#                'pitch': -0.0011402471456676722,
#                'rollspeed': 0.0038531175348907707,
#                'q3': -0.0006025685928761959
#            }
def df_formatter(features, message_data):
    ml_dict = {}

    for key, value in features.items():
        for feature in value:
            ml_dict[feature] = mean(message_data[key+'-'+feature])

    return ml_dict


# WIP
# Predicts if message is malicous or benign
# params [dict] features: contains all the MAVLink messages (keys) and the name of their features (values).
# params [dict] message_data: contains data returned from influx db
# params [string] model_file: full path to saved model
# return [string] output: model results
def make_prediction(features, message_data, model_file):
    # Make data frame with average of all values to pass into model

    ml_dict = df_formatter(features, message_data)


    ml_df = pd.DataFrame([ml_dict])

    # appending label for the test data DataFrame
    ml_dict['label'] = "benign"
    ml_label_df = pd.DataFrame([ml_dict])


    model = pickle.load(open(model_file, 'rb'))

    y_pred = model.predict(ml_df)

    output = ""

    #output+= "This is y pred", y_pred
    y_true = ml_label_df[['label']]

    y_true = y_true.replace({'benign': 1})
    y_true = y_true.replace('malicious', -1)

    #output += str(model.score_samples(df_malicious_flight_pred)) # get raw scores
    output += str(metrics.classification_report(y_true, y_pred, digits=4))
    output += str(metrics.confusion_matrix(y_true, y_pred))


    return output
