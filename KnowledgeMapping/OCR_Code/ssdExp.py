import os
import math
import random
import sys
import numpy as np
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt
import matplotlib.cm as mpcm
sys.path.append('D:\\A\\Desktop\\项目+更新\\SSD-Tensorflow')
from nets import ssd_vgg_300, ssd_common, np_methods
from preprocessing import ssd_vgg_preprocessing

# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

gpu_options = tf.GPUOptions(allow_growth=True)
config = tf.ConfigProto(log_device_placement=False, gpu_options=gpu_options)
isess = tf.InteractiveSession(config=config)


#我们用的TensorFlow下的一个集成包slim，比tensor要更加轻便
slim = tf.contrib.slim
#训练数据中包含了一下已知的类别，也就是我们可以识别出以下的东西，不过后续我们将自己自己训练自己的模型，来识别自己想识别的东西
l_VOC_CLASS = [
                'aeroplane',   'bicycle', 'bird',  'boat',      'bottle',
                'bus',         'car',     'cat',   'chair',     'cow',
                'diningTable', 'dog',     'horse', 'motorbike', 'person',
                'pottedPlant', 'sheep',   'sofa',  'train',     'TV'
]
# 定义数据格式
net_shape = (300, 300)
data_format = 'NHWC'  # [Number, height, width, color]，Tensorflow backend 的格式

# 预处理将输入图片大小改成 300x300，作为下一步输入
img_input = tf.placeholder(tf.uint8, shape=(None, None, 3))
image_pre, labels_pre, bboxes_pre, bbox_img = ssd_vgg_preprocessing.preprocess_for_eval(
    img_input,
    None,
    None,
    net_shape,
    data_format,
    resize=ssd_vgg_preprocessing.Resize.WARP_RESIZE
)
image_4d = tf.expand_dims(image_pre, 0)


# 定义 SSD 模型结构
reuse = True if 'ssd_net' in locals() else None
ssd_net = ssd_vgg_300.SSDNet()
with slim.arg_scope(ssd_net.arg_scope(data_format=data_format)):
    predictions, localisations, _, _ = ssd_net.net(image_4d, is_training=False, reuse=reuse)
# 导入官方给出的 SSD 模型参数
#这边修改成你自己的路径
ckpt_filename = 'D:\\A\\Desktop\\项目+更新\\SSD-Tensorflow\\checkpoints\\ssd_300_vgg.ckpt'
isess.run(tf.global_variables_initializer())
saver = tf.train.Saver()
saver.restore(isess, ckpt_filename)
ssd_anchors = ssd_net.anchors(net_shape)


#不同类别，我们以不同的颜色表示
def colors_subselect(colors, num_classes=21):
    dt = len(colors) // num_classes
    sub_colors = []
    for i in range(num_classes):
        color = colors[i*dt]
        if isinstance(color[0], float):
            sub_colors.append([int(c * 255) for c in color])
        else:
            sub_colors.append([c for c in color])
    return sub_colors
#画出在图中的位置
def bboxes_draw_on_img(img, classes, scores, bboxes, colors, thickness=5):
    shape = img.shape
    for i in range(bboxes.shape[0]):
        bbox = bboxes[i]
        color = colors[classes[i]]
        # Draw bounding box...
        p1 = (int(bbox[0] * shape[0]), int(bbox[1] * shape[1]))
        p2 = (int(bbox[2] * shape[0]), int(bbox[3] * shape[1]))
        cv2.rectangle(img, p1[::-1], p2[::-1], color, thickness)
        # Draw text...
        s = '%s:%.3f' % ( l_VOC_CLASS[int(classes[i])-1], scores[i])
        p1 = (p1[0]-5, p1[1])
        cv2.putText(img, s, p1[::-1], cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
colors_plasma = colors_subselect(mpcm.plasma.colors, num_classes=21)


def process_image(img, select_threshold=0.3, nms_threshold=.8, net_shape=(300, 300)):
    #先获取SSD网络的层相关的参数
    rimg, rpredictions, rlocalisations, rbbox_img = isess.run([image_4d, predictions, localisations, bbox_img],
                                                              feed_dict={img_input: img})
    #获取分类结果，位置
    rclasses, rscores, rbboxes = np_methods.ssd_bboxes_select(
            rpredictions, rlocalisations, ssd_anchors,
            select_threshold=select_threshold, img_shape=net_shape, num_classes=21, decode=True)
    rbboxes = np_methods.bboxes_clip(rbbox_img, rbboxes)
    rclasses, rscores, rbboxes = np_methods.bboxes_sort(rclasses, rscores, rbboxes, top_k=400)
    rclasses, rscores, rbboxes = np_methods.bboxes_nms(rclasses, rscores, rbboxes, nms_threshold=nms_threshold)
    # 让我们在图中画出来就行了
    rbboxes = np_methods.bboxes_resize(rbbox_img, rbboxes)
    bboxes_draw_on_img(img, rclasses, rscores, rbboxes, colors_plasma, thickness=2)
    return img


#读取数据
img = cv2.imread("123.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(process_image(img))
plt.show()

