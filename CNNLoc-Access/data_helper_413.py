from sklearn.preprocessing import MinMaxScaler,RobustScaler
import pandas as pd
import numpy as np
import math
import  os

base_dir= os.getcwd()

WAP_SIZE = 520
LONGITUDE = 520
LATITUDE = 521
FLOOR = 522
BUILDINGID = 523

#input data separated before

class NormY(object):
    long_max=None
    long_min=None
    lati_max=None
    lati_min=None
    long_scale=None
    lati_scale=None

    def __init__(self):
        pass

    def fit(self,long,lati):
        self.long_max=max(long)
        self.long_min=min(long)
        self.lati_max=max(lati)
        self.lati_min=min(lati)
        self.long_scale=self.long_max-self.long_min
        self.lati_scale=self.lati_max-self.lati_min

    def normalizeY(self,longitude_arr, latitude_arr):

        longitude_arr = np.reshape(longitude_arr, [-1, 1])
        latitude_arr = np.reshape(latitude_arr, [-1, 1])
        long=(longitude_arr-self.long_min)/self.long_scale
        lati=(latitude_arr-self.lati_min)/self.lati_scale
        return long,lati

    def reverse_normalizeY(self,longitude_arr, latitude_arr):

        longitude_arr = np.reshape(longitude_arr, [-1, 1])
        latitude_arr = np.reshape(latitude_arr, [-1, 1])
        long=(longitude_arr*self.long_scale)+self.long_min
        lati=(latitude_arr*self.lati_scale)+self.lati_min
        return long,lati

def normalizeX(arr,b=2.8):
    # return normalizeX_powed_noise(arr,rate=noise_rate).reshape([-1,520])
    # return normalizeX_zero_to_one(arr).reshape([-1, 520])
    return normalizeX_powed(arr,b).reshape([-1, WAP_SIZE])

def normalizeX_powed(arr, b):
    res = np.copy(arr).astype(np.float)
    for i in range(np.shape(res)[0]):
        for j in range(np.shape(res)[1]):
            if (res[i][j] > 50) | (res[i][j] == None) | (res[i][j] < -95):
                res[i][j] = 0
            elif (res[i][j] >= 0):
                res[i][j] = 1

            else:
                res[i][j] = ((95 + res[i][j]) / 95.0) ** b
            # res[i][j] = (0.01 * (110 + res[i][j])) ** 2.71828
    return res



    # return normx.transform(arr).reshape([-1,520])
def load_data_perspective(file_name):
    data_frame = pd.read_csv(file_name)
    data_x = data_frame.get_values().T[:WAP_SIZE].T
    data_y = data_frame.get_values().T[[LONGITUDE, LATITUDE, FLOOR, BUILDINGID], :].T
    return data_x, data_y

def load_data_all(train,valid,test):
    return load_data_perspective(train),load_data_perspective(valid),load_data_perspective(test)
