# import tensorflow as tf
import json
import numpy as np
from scipy.interpolate import interp1d
import tensorflow as tf
from keras.models import Model

with tf.device('/cpu:0'):
    model_path = "./app/airsign/customNN.h5"
    
    model = tf.keras.models.load_model(
        model_path)
    sub_model = Model(inputs=model.input,
                      outputs=model.get_layer('dense_2').output)


def linear_interpolate(scale_sample: int, origin_point: list):
    origin_time = np.linspace(0, 10, len(origin_point))
    f1 = interp1d(origin_time, origin_point, kind='cubic')
    x = np.linspace(0, 10, scale_sample)
    y = f1(x)
    return x, y


def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def airsign_predict(landmark):
    frame_time_sequence = []
    finger_position_x = []
    finger_position_y = []
    finger_position_z = []
    finger_speed_x = []
    finger_speed_y = []
    finger_speed_z = []

    for frame_number in landmark[0:-45]:
        frame_time = frame_number['unix_time']
        finger_tip = frame_number['landmark'][8]
        finger_x = finger_tip['x']
        finger_y = finger_tip['y']
        finger_z = finger_tip['z']
        finger_position_x.append(finger_x)
        finger_position_y.append(finger_y)
        finger_position_z.append(finger_z)
        frame_time_sequence.append(frame_time)
        inter_point = 512

    point_pair = list(zip(finger_position_x,
                      finger_position_y, finger_position_z))
    time_diff = np.diff(frame_time_sequence)
    for i in range(len(point_pair)-1):
        finger_speed_x.append(
            finger_position_x[i+1]-finger_position_x[i])
        finger_speed_y.append(
            finger_position_y[i+1]-finger_position_y[i])
        finger_speed_z.append(
            finger_position_z[i+1]-finger_position_z[i])
    finger_acc_x = np.divide(finger_speed_x, time_diff)
    finger_acc_y = np.divide(finger_speed_y, time_diff)
    finger_acc_z = np.divide(finger_speed_z, time_diff)
    x_axis, x_position_spline = linear_interpolate(
        inter_point, NormalizeData(finger_position_x))
    x_axis, y_position_spline = linear_interpolate(
        inter_point, NormalizeData(finger_position_y))
    x_axis, z_position_spline = linear_interpolate(
        inter_point, NormalizeData(finger_position_z))
    x_axis, x_speed_spline = linear_interpolate(
        inter_point, NormalizeData(finger_speed_x))
    x_axis, y_speed_spline = linear_interpolate(
        inter_point, NormalizeData(finger_speed_y))
    x_axis, z_speed_spline = linear_interpolate(
        inter_point, NormalizeData(finger_speed_z))
    x_axis, x_acc_spline = linear_interpolate(
        inter_point, NormalizeData(finger_acc_x))
    x_axis, y_acc_spline = linear_interpolate(
        inter_point, NormalizeData(finger_acc_y))
    x_axis, z_acc_spline = linear_interpolate(
        inter_point, NormalizeData(finger_acc_z))

    sign_9d = [x_position_spline, y_position_spline, z_position_spline,
               x_speed_spline, y_speed_spline, z_speed_spline,
               x_acc_spline, y_acc_spline, z_acc_spline]
    sign_9d = np.array(sign_9d)
    sign = sign_9d.reshape(1, 9, 512)
    y_pred = sub_model.predict(sign)

    y_pred = y_pred > 0.5
    y_pred = np.multiply(y_pred, 1)
    print(y_pred)
    mm = "".join([str(i) for i in y_pred[0]])
    return(int(mm, 2))
