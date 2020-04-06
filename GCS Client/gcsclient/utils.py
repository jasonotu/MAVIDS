import math
import pickle
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn import preprocessing
from sklearn import svm

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
