import tensorflow as tf
import json
import numpy as np
from scipy.interpolate import interp1d
from keras.models import Sequential, Model

# with tf.device('/cpu:0'):
#     model_path = "./app/airsign/20220719_170457_f1_d3_vgg16_finetune_degree_range_30.h5"
#     model = tf.keras.models.load_model(
#         model_path)
#     sub_model = Model(inputs=model.input,
#                       outputs=model.get_layer('latent').output)


def linear_interpolate(scale_sample: int, origin_point: list):
    origin_time = np.linspace(0, 10, len(origin_point))
    f1 = interp1d(origin_time, origin_point, kind='cubic')
    x = np.linspace(0, 10, scale_sample)
    y = f1(x)
    return x, y


def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def airsign_predict(landmark):
    finger_position_x = []
    finger_position_y = []
    finger_position_z = []
    finger_speed_x = []
    finger_speed_y = []
    finger_speed_z = []

    for frame_number in landmark[0:-45]:
        finger_tip = frame_number['landmark'][8]
        finger_x = finger_tip['x']
        finger_y = finger_tip['y']
        finger_z = finger_tip['z']
        finger_position_x.append(finger_x)
        finger_position_y.append(finger_y)
        finger_position_z.append(finger_z)
        inter_point = 512

    x_axis, x_position_spline = linear_interpolate(
        inter_point, NormalizeData(finger_position_x))
    x_axis, y_position_spline = linear_interpolate(
        inter_point, NormalizeData(finger_position_y))
    x_axis, z_position_spline = linear_interpolate(
        inter_point, NormalizeData(finger_position_z))

    sign_3d = [x_position_spline, y_position_spline, z_position_spline]
    sign_3d = np.array(sign_3d)

    print(sign_3d.shape)
    sign = sign_3d.reshape(1, 3, 512)
    print(sign.shape)
    y_pred = sub_model.predict(sign)
    print(y_pred)
    y_pred = y_pred > 0.5
    y_pred = np.multiply(y_pred, 1)
    print(y_pred)
    mm = "".join([str(i) for i in y_pred[0]])
    return(int(mm, 2))
