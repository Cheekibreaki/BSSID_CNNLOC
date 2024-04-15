from encoder_model import EncoderDNN
import numpy as np
import data_helper
import time
import keras
import csv
#import matplotlib.pyplot as plt
import os
import tensorflow as tf
from keras.optimizers import Adam,Adagrad,Adadelta,Nadam,Adamax,SGD,RMSprop
from keras.losses import MSE,MAE,MAPE,MSLE,KLD,squared_hinge,hinge,categorical_hinge,categorical_crossentropy,sparse_categorical_crossentropy,kullback_leibler_divergence,poisson

os.environ["CUDA_VISIBLE_DEVICES"]='0'
from keras.backend.tensorflow_backend import set_session
config=tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction=0.9
set_session(tf.Session(config=config))

# OPT=[Adam,Adagrad,Nadam,Adamax,RMSprop]
OPT=[RMSprop,Adamax]

LOSS=[MSE]
LR_34=[0.005,0.001,0.0005,0.0001]
# LR_23=[0.05,0.01,0.005,0.001]
LR_23=[0.001,0.001,0.001]
LR_15=[0.005,0.005,0.005]
rng=np.random.RandomState(888)

base_dir= os.getcwd()
# train_csv_path = os.path.join(base_dir,'trainingData.csv')
test_csv_path=os.path.join(base_dir,'TestData.csv')
valid_csv_path=os.path.join(base_dir,'ValidationData.csv')
train_csv_path=os.path.join(base_dir,'TrainingData.csv')

log_dir='New_access_log.txt'
if __name__ == '__main__':
    # Load data
    (train_x, train_y), (valid_x, valid_y), (test_x, test_y) = data_helper.load_data_all(train_csv_path, valid_csv_path,test_csv_path)

    b = 2.8
    p = 3
    epoch_sae = 40
    epoch_building=40
    epoch_floor = 40
    epoch_position = 60
    dp = 0.7
    info="""
    b = 2.8
    p = 3
    epoch_sae = 40
    epoch_floor = 40
    epoch_building = 40
    epoch_position = 60
    dp = 0.7
    """
    with open(log_dir, 'a') as file:
        file.write('\n' + info)

    for loss in LOSS:
        for opt in OPT:
            if opt==RMSprop:
                LR=LR_23
            else:
                LR=LR_15

            for lr in LR:
                # Training
                encode_dnn_model = EncoderDNN()
                encode_dnn_model.patience=int(p)
                encode_dnn_model.b=b
                encode_dnn_model.epoch_AE=epoch_sae
                encode_dnn_model.epoch_floor=epoch_floor
                encode_dnn_model.epoch_position=epoch_position
                encode_dnn_model.epoch_building=epoch_building
                encode_dnn_model.dropout=dp
                encode_dnn_model.loss=loss
                encode_dnn_model.opt=opt(lr=lr)
                strat = time.time()
                # tbCallBack=keras.callbacks.TensorBoard(log_dir='./Graph',
                #                                        histogram_freq=1,
                #                                        write_graph=True,
                #                                        write_images=True)

                h=encode_dnn_model.fit(train_x, train_y, valid_x=valid_x, valid_y=valid_y)#,tensorbd=tbCallBack)
                end=time.time()
                trining_time=end-strat

                building_right, floor_right, longitude_error, latitude_error, longitude_std_dev, latitude_std_dev, mean_error = encode_dnn_model.error(
                    test_x, test_y)


                with open(log_dir, 'a') as file:
                    file.write('\n test data')
                    file.write('\nloss,opt,lr,b_hr,f_hr,pos_longi_err,pos_lati_err,longi_std,lati_std,mean_err,time')
                    file.write(f"\n{loss},{opt},{lr},{(building_right / 31.0) * 100}%,{(floor_right / 31.0) * 100}%," +
                               f"{longitude_error},{latitude_error},{longitude_std_dev},{latitude_std_dev},{mean_error}," +
                               f"{end - strat}")

                building_right, floor_right, longitude_error, latitude_error, longitude_std_dev, latitude_std_dev, mean_error = encode_dnn_model.error(
                    valid_x, valid_y)

                del encode_dnn_model

                with open(log_dir, 'a') as file:
                    file.write('\n valid data')
                    file.write('\nloss,opt,lr,b_hr,f_hr,pos_longi_err,pos_lati_err,longi_std,lati_std,mean_err,time')
                    file.write(f"\n{loss},{opt},{lr},{(building_right / 52.0) * 100}%,{(floor_right / 52.0) * 100}%," +
                               f"{longitude_error},{latitude_error},{longitude_std_dev},{latitude_std_dev},{mean_error}," +
                               f"{end - strat}")