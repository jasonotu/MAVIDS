import math
import time
import pickle
import sys
import pandas as pd
import numpy as np
import os
from sklearn import metrics
from sklearn import svm
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
#from pymavlink import mavutil
from .models import Settings

sys.path.append(os.path.join(os.path.dirname(__file__)) + "\..\..\libraries")
print(sys.path)
from pymavlink import mavutil

os.environ['MAVLINK20'] = "1"
mavutil.set_dialect("MAVIDS")

# optimization function modified from: https://github.com/spacesense-ai/spacesense/blob/master/spacesense/utils.py
def optimize_OneClassSVM(X, n):
    print('Searching for optimal hyperparameters...')
    nu = np.linspace(start=1e-5, stop=1e-2, num=n)
    gamma = np.linspace(start=1e-6, stop=1e-3, num=n)
    opt_diff = 1.0
    opt_nu = None
    opt_gamma = None
    for i in range(len(nu)):
        for j in range(len(gamma)):
            classifier = svm.OneClassSVM(kernel="rbf", nu=nu[i], gamma=gamma[j])
            classifier.fit(X)
            label = classifier.predict(X)
            p = 1 - float(sum(label == 1.0)) / len(label)
            diff = math.fabs(p - nu[i])
            if diff < opt_diff:
                opt_diff = diff
                opt_nu = nu[i]
                opt_gamma = gamma[j]
    print("Found: nu = %f, gamma = %f" % (opt_nu, opt_gamma))
    return opt_nu, opt_gamma

def train_OneClassSVM():
    output = ''
    # load CSVs
    df_benign_flight = pd.read_csv(r'C:\Users\Jason\PycharmProjects\mavids\mavids\gcsclient\NORMAL_DOS_V_FINAL.csv')
    df_malicious_flight = pd.read_csv(r'C:\Users\Jason\PycharmProjects\mavids\mavids\gcsclient\DOS_DATASET_V_FINAL.csv')

    df_benign_flight_train = df_benign_flight.drop(columns=['timestamp', 'label'])
    df_malicious_flight_pred = df_malicious_flight.drop(columns=['timestamp', 'label'])
    df_malicious_flight = df_malicious_flight.drop(columns=['timestamp'])

    # print the first 5 rows of each dataframe
    output += "Original Values:\n"
    output += "df_benign_flight_train: \n%s\n" % df_benign_flight_train[0:5].to_string()
    output += "df_malicious_flight_pred: \n%s\n" % df_malicious_flight_pred[0:5].to_string()
    output += "df_malicious_flight: \n%s\n" % df_malicious_flight[0:5].to_string()

    output += "Benign count: " + str(len(df_benign_flight_train)) + "\n"
    output += "Malicious count: " + str(len(df_malicious_flight.loc[df_malicious_flight['label'] == 'malicious'])) + "\n"

    nu_opt, gamma_opt = optimize_OneClassSVM(df_benign_flight_train, 10)

    model = svm.OneClassSVM(nu=nu_opt, kernel="rbf", gamma=gamma_opt)
    model.fit(df_benign_flight_train)

    pickle.dump(model, open('finalized_model.sav', 'wb'))

    y_pred = model.predict(df_malicious_flight_pred)
    y_true = df_malicious_flight[['label']]

    y_true = y_true.replace({'benign': 1})
    y_true = y_true.replace('malicious', -1)

    #output += str(model.score_samples(df_malicious_flight_pred)) # get raw scores

    output += str(metrics.classification_report(y_true, y_pred, digits=4))
    output += str(metrics.confusion_matrix(y_true, y_pred))

    return output

def train_LocalOutlierFactor():
    output = ''
    # load CSVs
    df_benign_flight = pd.read_csv(r'C:\Users\Jason\PycharmProjects\mavids\mavids\gcsclient\NORMAL_DOS_V_FINAL.csv')
    df_malicious_flight = pd.read_csv(r'C:\Users\Jason\PycharmProjects\mavids\mavids\gcsclient\DOS_DATASET_V_FINAL.csv')

    df_benign_flight_train = df_benign_flight.drop(columns=['timestamp', 'label'])
    df_malicious_flight_pred = df_malicious_flight.drop(columns=['timestamp', 'label'])
    df_malicious_flight = df_malicious_flight.drop(columns=['timestamp'])

    df_benign_flight_train = df_benign_flight[
        ['load', 'vibration_x', 'vibration_y', 'servo1_raw', 'servo3_raw', 'servo5_raw', 'servo6_raw', 'q3', 'xgyro',
         'pitch', 'rollspeed', 'yacc']]
    df_malicious_flight_pred = df_malicious_flight_pred[
        ['load', 'vibration_x', 'vibration_y', 'servo1_raw', 'servo3_raw', 'servo5_raw', 'servo6_raw', 'q3', 'xgyro',
         'pitch', 'rollspeed', 'yacc']]
    df_malicious_flight = df_malicious_flight[
        ['label', 'load', 'vibration_x', 'vibration_y', 'servo1_raw', 'servo3_raw', 'servo5_raw', 'servo6_raw', 'q3',
         'xgyro', 'pitch', 'rollspeed', 'yacc']]
    # df_malicious_flight_train = df_malicious_flight.drop(columns=['timestamp', 'label'])

    # print the first 5 rows of each dataframe
    output += "Original Values:\n"
    output += "df_benign_flight_train: \n%s\n" % df_benign_flight_train[0:5].to_string()
    output += "df_malicious_flight_pred: \n%s\n" % df_malicious_flight_pred[0:5].to_string()
    output += "df_malicious_flight: \n%s\n" % df_malicious_flight[0:5].to_string()

    """*   Run classifier and print predictions
    *   We are using the entire malicious flight for training. We don't *have* to, but we do to properly score the performance. Otherwise the predictions and truths aren't lined up/accurate
    """

    output += "Benign count: " + str(len(df_benign_flight_train)) + "\n"
    output += "Malicious count: " + str(len(df_malicious_flight.loc[df_malicious_flight['label'] == 'malicious'])) + "\n"

    # neighbours at 61 gives lower false positive rate than n=30
    model = LocalOutlierFactor(n_neighbors=61, novelty=True, contamination=0.1)
    model.fit(df_benign_flight_train)

    pickle.dump(model, open('finalized_model.sav', 'wb'))

    y_pred = model.predict(df_malicious_flight_pred)
    y_true = df_malicious_flight[['label']]

    y_true = y_true.replace({'benign': 1})
    y_true = y_true.replace('malicious', -1)

    output += str(metrics.classification_report(y_true, y_pred, digits=5))
    output += str(metrics.confusion_matrix(y_true, y_pred))

    return output

def train_Autoencoder():
    output = ''
    # load CSVs
    df_benign_flight = pd.read_csv(r'C:\Users\Jason\PycharmProjects\mavids\mavids\gcsclient\NORMAL_DOS_V_FINAL.csv')
    df_malicious_flight = pd.read_csv(r'C:\Users\Jason\PycharmProjects\mavids\mavids\gcsclient\DOS_DATASET_V_FINAL.csv')

    df_benign_flight = df_benign_flight[
        ['timestamp', 'label', 'load', 'vibration_x', 'vibration_y', 'servo1_raw', 'servo3_raw', 'servo5_raw',
         'servo6_raw', 'q3', 'xgyro', 'pitch', 'rollspeed', 'yacc']]
    df_malicious_flight = df_malicious_flight[
        ['timestamp', 'label', 'load', 'vibration_x', 'vibration_y', 'servo1_raw', 'servo3_raw', 'servo5_raw',
         'servo6_raw', 'q3', 'xgyro', 'pitch', 'rollspeed', 'yacc']]
    # split benign
    df_benign_flight_train, df_benign_flight_test = train_test_split(df_benign_flight, test_size=0.05, random_state=1)  # split x% of benign to test RMSE against

    # keep only features and label if applicable
    df_benign_flight_train = df_benign_flight_train.drop(columns=['timestamp', 'label'])
    df_benign_flight_test = df_benign_flight_test.drop(columns=['timestamp', 'label'])
    df_malicious_flight = df_malicious_flight.drop(columns=['timestamp'])
    df_malicious_flight_pred = df_malicious_flight.drop(columns=['label'])
    df_malicious_flight_test = df_malicious_flight_pred.loc[df_malicious_flight['label'] == 'malicious']

    # print the first 5 rows of each dataframe
    output += "Original Values:\n"
    output += "df_benign_flight_train:\n%s\n" % df_benign_flight_train[0:5].to_string()
    output += "df_benign_flight_test:\n%s\n" % df_benign_flight_test[0:5].to_string()
    output += "df_malicious_flight: \n%s\n" % df_malicious_flight[0:5].to_string()
    output += "df_malicious_flight_pred: \n%s\n" % df_malicious_flight_pred[0:5].to_string()

    output += "Benign count: " + str(len(df_benign_flight_train)) + "\n"
    output += "Malicious count: " + str(len(df_malicious_flight.loc[df_malicious_flight['label'] == 'malicious'])) + "\n"

    # This is the numeric feature vector, as it goes to the neural net
    x_benign_train = df_benign_flight_train.values
    x_benign_sample = df_benign_flight_test.values
    x_malicious_sample = df_malicious_flight_test.values

    model = Sequential()
    model.add(Dense(25, input_dim=x_benign_train.shape[1], activation='relu'))
    model.add(Dense(3, activation='relu'))
    model.add(Dense(25, activation='relu'))
    model.add(Dense(x_benign_train.shape[1]))  # Multiple output neurons
    model.compile(loss='mean_squared_error', optimizer='adam')
    monitor = EarlyStopping(monitor="loss", min_delta=1e-3, restore_best_weights=True)
    model.fit(x_benign_train, x_benign_train, verbose=1, epochs=100, callbacks=[monitor])

    #pickle.dump(model, open('finalized_model.sav', 'wb'))

    pred = model.predict(x_benign_train)
    score1 = metrics.mean_squared_error(pred, x_benign_train)
    pred = model.predict(x_benign_sample)
    score2 = metrics.mean_squared_error(pred, x_benign_sample)
    pred = model.predict(x_malicious_sample)
    score3 = metrics.mean_squared_error(pred, x_malicious_sample)
    output += f"Insample Benign Score (MSE): " + str(score1) + "\n"
    output += f"Out of Sample Benign Score (MSE): " + str(score2) + "\n"
    output += f"Malicious Score (MSE): " + str(score3) + "\n"

    threshold = 0.991
    y_pred = pd.DataFrame()
    predicted = model.predict(df_malicious_flight_pred)
    mse = np.mean(np.power(df_malicious_flight_pred - predicted, 2), axis=1)
    y_pred['MSE'] = mse
    mse_threshold = np.quantile(y_pred['MSE'], threshold)
    output += f'Selected threshold: {threshold * 100}%' + "\n"
    output += f'Calculated MSE threshold: {mse_threshold}' + "\n"
    y_pred['label'] = 1
    y_pred.loc[y_pred['MSE'] > mse_threshold, 'label'] = -1

    y_true = df_malicious_flight[['label']]
    y_true = y_true.replace({'benign': 1})
    y_true = y_true.replace('malicious', -1)

    output += f"Malicious count: {len(y_pred.loc[y_pred['label'] == -1])}" + "\n"
    output += str(classification_report(y_true, y_pred['label'], digits=4)) + "\n"
    output += str(confusion_matrix(y_true, y_pred['label'])) + "\n"

    return output

def read_file(file_name, use_label=False, start_label=None, end_label=None):
    #_________________VARIABLES YOU CAN EDIT_______________________________
    setting = Settings.objects.first()
    msg_dict = {
        "DOS": ["SYS_STATUS", "VIBRATION", "HIGHRES_IMU", "ATTITUDE_QUATERNION",
                "SERVO_OUTPUT_RAW", "ATTITUDE"],
        "GPS": ["HIGHRES_IMU", "ATTITUDE_QUATERNION", "GPS_RAW_INT", "VFR_HUD"],
        "3": ['VIBRATION', 'ATTITUDE', 'ATTITUDE_QUATERNION', 'HIGHRES_IMU', 'VFR_HUD', 'ATTITUDE_TARGET',
              'ESTIMATOR_STATUS', 'LOCAL_POSITION_NED', 'SERVO_OUTPUT_RAW', 'GLOBAL_POSITION_INT']}
    field_dict = {
        "DOS": ['load', 'vibration_x', 'servo3_raw', 'servo1_raw', "vibration_y", 'q3', 'xgyro', 'pitch',
                'rollspeed'],
        "GPS": ["xgyro", "ygyro", "zgyro", "ymag", "xmag", "zmag", "q1", "q2", "q3", "q4", "cog", "heading"],
        "3": ['vibration_x', 'vibration_y', 'vibration_z', 'q1', 'q2', 'pitchspeed', 'q4', 'yawspeed', 'rollspeed',
              'q3', 'roll', 'pitch', 'yaw', 'zacc', 'pressure_alt', 'xgyro', 'zmag', 'ymag', 'abs_pressure', 'xacc',
              'ygyro', 'zgyro', 'yacc', 'xmag', 'climb', 'throttle', 'groundspeed', 'alt', 'airspeed', 'heading',
              'body_pitch_rate', 'body_yaw_rate', 'body_roll_rate', 'pos_vert_accuracy', 'mag_ratio', 'hagl_ratio',
              'pos_horiz_ratio', 'pos_vert_ratio', 'vel_ratio', 'flags', 'tas_ratio', 'pos_horiz_accuracy',
              'servo6_raw', 'servo3_raw', 'servo2_raw', 'servo1_raw', 'servo5_raw', 'servo8_raw', 'servo4_raw',
              'servo7_raw', 'z', 'vy', 'vz', 'x', 'vx', 'y', 'hdg', 'lat', 'lon']}
    location_list = {
        "SYS_STATUS": ["load"],
        "VIBRATION": ["vibration_x", "vibration_y"],
        "HIGHRES_IMU": ["xgyro"],
        "ATTITUDE_QUATERNION": ["q3"],
        "SERVO_OUTPUT_RAW": ["servo3_raw", "servo1_raw"],
        "ATTITUDE": ["rollspeed", "pitch"]
    }
    window_time = {"DOS": 1.05, "GPS": 0.25, "3": 0.25}
    attacks = {"GPS": setting.gps_enabled, "DOS": setting.dos_enabled}
    #_______________________VARIABLES______________________________________
    #setting = Settings.objects.first()
    dataframe_dict = dict()
    dataframes = dict()
    begin = False
    final_dataset = {}
    mean_dataframe_rows = {}
    storage_list = {}
    #______________________END______________________________________________

    # __________________PARSING OF TLOG_____________________________________
    try:
        print(file_name)
        starttime = time.time()

        if ".tlog" in file_name:
            filename = file_name
            mlog = mavutil.mavlink_connection(filename)
            ext = os.path.splitext(filename)[1]
            isbin = ext in ['.bin', '.BIN']
            islog = ext in ['.log', '.LOG', '.tlog', '.TLOG']

            while True:

                m = mlog.recv_match()

                if m is None:
                    # FIXME: Make sure to output the last CSV message before dropping out of this loop
                    break

                timestamp = getattr(m, '_timestamp', 0.0)

                if not begin:
                    start_time = float(timestamp)
                    begin = True

                end_time = float(timestamp)

                s = "%s.%02u: %s" % (
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp)), int(timestamp * 100.0) % 100, m)

                first_split, temp_dict = lineparser(s)
                message_name = first_split[2]
                temp_dict["timestamp"] = timestamp

                if message_name in dataframe_dict:
                    dataframe_dict[message_name].append(temp_dict)
                else:
                    #print("hello")
                    dataframe_dict[message_name] = []
                    dataframe_dict[message_name].append(temp_dict)

            for x in dataframe_dict.keys():
                dataframes[x] = pd.DataFrame(dataframe_dict[x])
                print(dataframes[x])
        else:
            readfile = open(file_name)

            for x in readfile:
                lineparser(x)
    except IOError as e:
        print("error!", e)
        return False, None
    except Exception:
        return False, None

    #ACTUAL PARSING OF DATAFRAME

    try:
        for key, value in attacks.items():
            if value:
                final_dataset[key] = pd.DataFrame()
                mean_dataframe_rows[key] = []

                while True:
                    for x in field_dict[key]:
                        storage_list[x] = []

                    for x in msg_dict[key]:
                        temp_df = dataframes[x][(start_time <= dataframes[x]['timestamp']) & (
                                    dataframes[x]['timestamp'] < start_time + window_time[key])]

                        for y in location_list[x]:
                            storage_list[y] = temp_df[y].values.tolist()

                    data_point_dict = {}

                    for key_two, value_two in storage_list.items():
                        temp_list = list(map(float, value_two))
                        if len(temp_list) != 0:
                            data_point_dict[key_two] = sum(temp_list) / len(temp_list)
                            data_point_dict["timestamp"] = start_time

                    if len(data_point_dict) == len(field_dict[key]) + 1:
                        #start time
                        strp_a = datetime.datetime.strptime(start_label, fmt).time()

                        # end time
                        strp_b = datetime.datetime.strptime(end_label, fmt).time()

                        if use_label and start_time >= strp_a and start_time <= strp_b:
                            data_point_dict['label'] = '1'
                        elif use_label:
                            data_point_dict['label'] = '0'

                        mean_dataframe_rows[key].append(data_point_dict)

                    start_time += window_time[key]

                    if start_time > end_time:
                        break

                final_dataset[key] = pd.DataFrame(mean_dataframe_rows[key])

        endtime = time.time()
        print("done!! It took {0}".format(endtime - starttime))

        return True, final_dataset
    except Exception:
        return False, None

def lineparser(linestr):
    global folder_out, pastload, pasttime

    first = linestr[:linestr.index("{") - 1]
    second = linestr[linestr.index("{"):len(linestr)]
    currentscope = False
    currentindex = 0
    scopeindexfirst, scopeindexlast = 0, 0
    temp_dict = dict()

    if "BAD_DATA" not in first:
        if "[" in second:
            scopeindexfirst = second.index("[")
            scopeindexlast = second.index("]")
            currentscope = True

        while True:
            if "," in second:
                spliceindex = second.index(",")
            else:
                keypair_dict = second.strip("{}, ").split(" : ")

                if len(keypair_dict) <= 1:
                    break

                temp_dict[keypair_dict[0]] = keypair_dict[1]
                break

            keypair = ""
            if spliceindex == -1:
                break
            elif spliceindex < scopeindexfirst and currentscope:
                keypair = second[1:spliceindex]
                second = second[spliceindex + 1:len(second)]
                scopeindexfirst -= spliceindex + 1
                scopeindexlast -= spliceindex + 1
            elif spliceindex > scopeindexfirst and currentscope:
                keypair = second[1:scopeindexlast + 1]
                keypair = keypair.replace(",", "|")
                second = second[scopeindexlast + 2: len(second)]

                if "[" in second:
                    scopeindexfirst = second.index("[")
                    scopeindexlast = second.index("]")
                else:
                    currentscope = False
            else:
                keypair = second[1:spliceindex]
                second = second[spliceindex + 1:len(second)]

            keypair_dict = keypair.split(" : ")
            temp_dict[keypair_dict[0]] = keypair_dict[1]
    else:
        temp_dict = {"data": second}

    first_split = first.split(" ")
    return first_split, temp_dict
