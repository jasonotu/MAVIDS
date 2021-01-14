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
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import tkinter as tk
from tkinter import filedialog
#from pymavlink import mavutil
from .models import Settings

from pymavlink import mavutil
from .pyulog_mod import ulog2csv

os.environ['MAVLINK20'] = "1"
mavutil.set_dialect("MAVIDS")

def read_file(mode='gpsonly', malicious=False):
    #_________________VARIABLES YOU CAN EDIT_______________________________
    setting = Settings.objects.first()
    attacks = {"GPS": setting.gps_enabled, "DOS": setting.dos_enabled}

    csv_list_all = ['actuator_controls', 'actuator_output', 'airspeed',
                'ekf2_innovations', 'estimator_status', 'multirotor_motor_limits',
                'rate_ctrl_status', 'sensor_combined', 'telemetry_status', 'angular_velocity',
                'vehicle_attitude_0', 'global_position_0', 'gps_position_0', 'local_position_0',
                'magnetometer', 'vehicle_rates_setpoint']
    csv_list_gps = ['vehicle_attitude_0', 'global_position_0', 'gps_position_0', 'local_position_0']
    csv_list_gpsekf = ['actuator_controls', 'actuator_output', 'airspeed',
                       'ekf2_innovations', 'estimator_status', 'angular_velocity',
                       'vehicle_attitude_0', 'global_position_0', 'gps_position_0', 'local_position_0']
    #_______________________VARIABLES______________________________________
    #setting = Settings.objects.first()
    final_df = pd.Dataframe()
    #______________________END______________________________________________

    # __________________PARSING OF TLOG_____________________________________

    if mode == 'gpsonly':
        csv_list = csv_list_gps
    elif mode == 'gpsekf':
        csv_list = csv_list_gpsekf
    else:
        csv_list = csv_list_all


    # existing_csv_list = os.listdir(folderdir)
    # search_list.append((existing_csv_list, folderdir))
    # if malicious:
    #     mal_csv_list = os.listdir(malfolderdir)
    #     search_list.append((mal_csv_list, malfolderdir))

    # for csv_class in search_list:

    #     for csv in csv_list:
    #         for exist_csv in csv_class[0]:
    #             if csv in exist_csv:

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()

    for tuple_pair in ulog2csv(file_path, csv_list):
        temp_df = pd.Dataframe(tuple_pair[0], columns=tuple_pair[1])
        # print(temp_df)
        if len(final_df.columns) == 0:
            final_df = temp_df
        else:
            final_df = final_df.merge(temp_df, how='outer', left_on='timestamp', right_on='timestamp')
        break

    final_df = final_df.sort_values('timestamp')
    final_df = final_df.set_index('timestamp')
    final_df = final_df.interpolate(axis=0, method='linear', limit_direction='both')

    for column in final_df.columns:
        if "timestamp" in column:
            if column == "timestamp":
                continue
            print(column)
            final_df = final_df.drop(columns=column)

    # Code to label data points. Don't need in production. Used for debug and testing
    # if malicious == True and csv_class == search_list[1]:
    #     target_column = []
    #     target_lon, target_lat = 0, 0
    #     for index, row, in final_df[['lat_x', 'lon_x']].iterrows():
    #         if len(target_column) == 0:
    #             print(index, row)
    #             target_lat = row['lat_x']
    #             target_lon = row['lon_x']

    #         if (row['lat_x'] > target_lat + 0.03 or row['lat_x'] < target_lat - 0.03) or (
    #                 row['lon_x'] > target_lon + 0.03 or row['lon_x'] < target_lon - 0.03):
    #             # print(row, target_lat, target_lon)
    #             target_column.append("malicious")
    #         else:
    #             target_column.append("benign")
    #     final_df['label'] = target_column
    # end of labelling
    final_df = final_df.replace([np.inf, -np.inf], np.nan).dropna(how='any', axis=1)

    return final_df

def preprocessor(loaded_dfs):
    df_benign_flight = loaded_df
    dataframes_processed = dict()
    df_benign_flight_train = df_benign_flight.drop(columns=['timestamp', 'label'], errors='ignore')
    x = df_benign_flight_train.values
    x = StandardScaler().fit_transform(x)  # normalizing the features
    train_pca_gps = PCA(.85)
    train_pc_data = train_pca_gps.fit_transform(x)
    df_benign_flight_train = pd.DataFrame(data=train_pc_data)

    print('Explained variation per principal component: {}'.format(train_pca_gps.explained_variance_ratio_))
    print(sum(train_pca_gps.explained_variance_ratio_))

    dataframes_processed['benign'] = df_benign_flight
    dataframes_processed['benign_train'] = df_benign_flight_train

    # if len(loaded_dfs) > 1:
    #     df_malicious_flight = loaded_dfs[1]

    #     target_column = df_malicious_flight[['label']]
    #     df_malicious_flight_pred = df_malicious_flight.drop(columns=['timestamp', 'label'])
    #     x = df_malicious_flight_pred.values
    #     x = StandardScaler().fit_transform(x)  # normalizing the features
    #     test_malicious_nolabel = train_pca_gps.transform(x)
    #     df_malicious_flight_pred = pd.DataFrame(data=test_malicious_nolabel)
    #     df_malicious_flight = pd.DataFrame(data=test_malicious_nolabel)
    #     df_malicious_flight['label'] = target_column

    #     dataframes_processed['malicious'] = df_malicious_flight
    #     dataframes_processed['malicious_pred'] = df_malicious_flight_pred

    #     df_malicious_flight_test = df_malicious_flight_pred.loc[df_malicious_flight['label'] == 'malicious']
    #     dataframes_processed['malicious_auto_test'] = df_malicious_flight_test

    df_benign_flight_train, df_benign_flight_test = train_test_split(df_benign_flight, test_size=0.05, random_state=1)

    dataframes_processed['benign_auto_test'] = df_benign_flight_test
    dataframes_processed['benign_auto_train'] = df_benign_flight_train

    return dataframes_processed


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

def train_OneClassSVM(dataframes_processed):
    output = ''
    # load CSVs

    df_benign_flight_train = dataframes_processed['benign_auto_train']
    # df_malicious_flight = dataframes_processed['malicious']
    # df_malicious_flight_pred = dataframes_processed['malicious_pred']


    # print the first 5 rows of each dataframe
    output += "Original Values:\n"
    output += "df_benign_flight_train: \n%s\n" % df_benign_flight_train[0:5].to_string()
    # output += "df_malicious_flight_pred: \n%s\n" % df_malicious_flight_pred[0:5].to_string()
    # output += "df_malicious_flight: \n%s\n" % df_malicious_flight[0:5].to_string()

    output += "Benign count: " + str(len(df_benign_flight_train)) + "\n"
    #output += "Malicious count: " + str(len(df_malicious_flight.loc[df_malicious_flight['label'] == 'malicious'])) + "\n"

    #nu_opt, gamma_opt = optimize_OneClassSVM(df_benign_flight_train, 10)
    #model = svm.OneClassSVM(nu=nu_opt, kernel="rbf", gamma=gamma_opt)
    model = svm.OneClassSVM(nu=0.0211, kernel="rbf", gamma=0.0003)
    model.fit(df_benign_flight_train)

    pickle.dump(model, open('finalized_model.sav', 'wb'))

    # y_pred = model.predict(df_malicious_flight_pred)
    # y_true = df_malicious_flight[['label']]

    # y_true = y_true.replace({'benign': 1})
    # y_true = y_true.replace('malicious', -1)

    # #output += str(model.score_samples(df_malicious_flight_pred)) # get raw scores

    # output += str(metrics.classification_report(y_true, y_pred, digits=4))
    # output += str(metrics.confusion_matrix(y_true, y_pred))

    return None

def train_LocalOutlierFactor(dataframes_processed):
    output = ''
    # load CSVs
    df_benign_flight_train = dataframes_processed['benign_auto_train']
    # df_malicious_flight = dataframes_processed['malicious']
    # df_malicious_flight_pred = dataframes_processed['malicious_pred']

    # output += "Original Values:\n"
    # output += "df_benign_flight_train: \n%s\n" % df_benign_flight_train[0:5].to_string()
    # output += "df_malicious_flight_pred: \n%s\n" % df_malicious_flight_pred[0:5].to_string()
    # output += "df_malicious_flight: \n%s\n" % df_malicious_flight[0:5].to_string()

    """*   Run classifier and print predictions
    *   We are using the entire malicious flight for training. We don't *have* to, but we do to properly score the performance. Otherwise the predictions and truths aren't lined up/accurate
    """

    output += "Benign count: " + str(len(df_benign_flight_train)) + "\n"
    #output += "Malicious count: " + str(len(df_malicious_flight.loc[df_malicious_flight['label'] == 'malicious'])) + "\n"

    # neighbours at 61 gives lower false positive rate than n=30
    model = LocalOutlierFactor(n_neighbors=3100, novelty=True, contamination=0.1, n_jobs=-1)
    model.fit(df_benign_flight_train)

    pickle.dump(model, open('lof.sav', 'wb'))

    # y_pred = model.predict(df_malicious_flight_pred)
    # y_true = df_malicious_flight[['label']]

    # y_true = y_true.replace({'benign': 1})
    # y_true = y_true.replace('malicious', -1)

    # output += str(metrics.classification_report(y_true, y_pred, digits=5))
    # output += str(metrics.confusion_matrix(y_true, y_pred))

    return None

def train_Autoencoder(dataframes_processed):
    output = ''
    df_benign_flight_train = dataframes_processed['benign_auto_train']
    df_benign_flight_test = dataframes_processed['benign_auto_test']
    # df_malicious_flight_test = dataframes_processed['malicious_auto_test']
    # df_malicious_flight = dataframes_processed['malicious']
    # df_malicious_flight_pred = dataframes_processed['malicious_pred']

    x_benign_train = df_benign_flight_train.values
    x_benign_sample = df_benign_flight_test.values
    #x_malicious_sample = df_malicious_flight_test.values

    model = Sequential()
    model.add(Dense(25, input_dim=x_benign_train.shape[1], activation='relu'))
    model.add(Dense(3, activation='relu'))
    model.add(Dense(25, activation='relu'))
    model.add(Dense(x_benign_train.shape[1]))  # Multiple output neurons
    model.compile(loss='mean_squared_error', optimizer='adam')
    monitor = EarlyStopping(monitor="loss", min_delta=1e-3, restore_best_weights=True)
    model.fit(x_benign_train, x_benign_train, verbose=1, epochs=100, callbacks=[monitor])

    pred = model.predict(x_benign_train)
    score1 = metrics.mean_squared_error(pred, x_benign_train)
    pred = model.predict(x_benign_sample)
    score2 = metrics.mean_squared_error(pred, x_benign_sample)
    # pred = model.predict(x_malicious_sample)
    # score3 = metrics.mean_squared_error(pred, x_malicious_sample)

    output += f"Insample Benign Score (MSE): " + str(score1) + "\n"
    output += f"Out of Sample Benign Score (MSE): " + str(score2) + "\n"
    # output += f"Malicious Score (MSE): " + str(score3) + "\n"

    model.save('autoencoder.h5')

    threshold = 0.96
    y_pred = pd.DataFrame()

    # predicted = model.predict(df_malicious_flight_pred)
    # mse = np.mean(np.power(df_malicious_flight_pred - predicted, 2), axis=1)
    # y_pred['MSE'] = mse
    # mse_threshold = np.quantile(y_pred['MSE'], threshold)

    # output += f'Selected threshold: {threshold*100}%' + "\n"
    # output += f'Calculated MSE threshold: {mse_threshold}' + "\n"

    # y_pred['label'] = 1
    # y_pred.loc[y_pred['MSE'] > mse_threshold, 'label'] = -1

    # y_true = df_malicious_flight[['label']]
    # y_true = y_true.replace({'benign': 1})
    # y_true = y_true.replace('malicious', -1)

    # output += f"Malicious count: {len(y_pred.loc[y_pred['label'] == -1])}" + "\n"
    # output += classification_report(y_true, y_pred['label'], digits=5)  + "\n"
    # conf_matrix = confusion_matrix(y_true, y_pred['label']) + "\n"
    # output += conf_matrix + "\n"

    # LABELS = ["Malicious", "Benign"]
    # plt.figure(figsize=(12, 12))
    # plt.tick_params(axis="x", labelsize=30)
    # plt.tick_params(axis="y", labelsize=30)
    # sns.heatmap(conf_matrix, xticklabels=LABELS, yticklabels=LABELS, annot=True, annot_kws={"size": 50}, fmt="d",
    #             cmap="Blues", linewidths=1, linecolor='black');
    # plt.ylabel('True class', fontsize=28)
    # plt.xlabel('Predicted class', fontsize=28)
    # plt.show()

    return None


