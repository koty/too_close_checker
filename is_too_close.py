import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

from skimage.color import rgb2gray
from skimage import io, exposure, img_as_float, img_as_ubyte
import warnings

# 顔検出器
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
THRESHOLD_METER = 1.5

def _convert2meter(raw_depth):
    # https://openkinect.org/wiki/Imaging_Information#Depth_Camera
    if raw_depth > 1050:
        # 2.5m以内の場合にしか適用できない数式なので、おおむねそれ以上のraw_depthの場合は一律999mと返す
        return 999
    return 0.1236 * math.tan(raw_depth / 2842.5 + 1.1863)

def _convert2gray(img):
    # https://qiita.com/yoya/items/dba7c40b31f832e9bc2a
    img = img_as_float(img)  # np.array(img/255.0, dtype=np.float64)
    imgL = exposure.adjust_gamma(img, 2.2)  # pow(img, 2.2)
    img_grayL = rgb2gray(imgL)
    img_gray = exposure.adjust_gamma(img_grayL, 1.0/2.2)  # pow(img_grayL, 1.0/2.2)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        img_gray = img_as_ubyte(img_gray)  # np.array(img_gray*255, dtype=np.uint8)
        return img_gray
    
def is_too_close(rgb, depth):
    # http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html
    # グレースケールに変換
    gray = _convert2gray(rgb)
    # 顔検出
    faces = face_cascade.detectMultiScale(gray)
    for face in faces:
        # array([[310, 332,  33,  33]], dtype=int32)
        # depth画像から顔部分を切り出し
        # depth[332:365, 310:343]
        x_start = face[1]
        x_end = x_start + face[3]
        y_start = face[0]
        y_end = y_start + face[2]
        depth_cropped = depth[x_start:x_end,
                              y_start:y_end]
        # 顔領域の平均距離
        distance = _convert2meter(np.average(depth_cropped))
        # 閾値より近かったら too close
        if distance < THRESHOLD_METER:
            return True
    return False

