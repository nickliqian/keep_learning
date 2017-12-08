import tensorflow as tf
import os
from selenium import webdriver

webdriver.Chrome()

# 设定命令行参数 (name, default_value, doc)
tf.app.flags.DEFINE_string("data_dir", "./data", "二进制目录")
tf.app.flags.DEFINE_string("tfrecords_dir", "./data", "TFRecords文件的名字")
tf.app.flags.DEFINE_integer("batch_size", 100, "每批次读取数据的大小")
FLAGS = tf.app.flags.FLAGS


class CifarRead(object):

    def __init__(self, file_list):
        # 文件名的列表
        self.file_list = file_list

        # 定义图片的属性
        self.height = 32
        self.width = 32
        self.channel = 3
        self.label_bytes = 1
        self.image_bytes = self.height * self.width * self.channel
        self.bytes = self.label_bytes + self.image_bytes

    # 读取二进制数据
    def read_and_decode(self):
        # 构造文件列表
        file_queue = tf.train.string_input_producer(self.file_list)

        # 构造二进制数据阅读器
        reader = tf.FixedLengthRecordReader(self.bytes)
        key, value = reader.read(file_queue)

        # 解码数据 value包括标签和数值
        label_image = tf.decode_raw(value, tf.uint8)

        # 进行特征值和目标值的分割，类型转换，形状转换
        # 按照label的bytes大小抽离label, 并转为int32 -> image(实际数据)同样原理
        label = tf.cast(tf.slice(label_image, [0], [self.label_bytes]), tf.int32)
        image = tf.slice(label_image, [self.label_bytes], [self.image_bytes])

        # 改变image形状(批量处理要求) (?) -> (32, 32, 3)
        image_reshape = tf.reshape(image, [self.height, self.width, self.channel])

        # 类型改变
        image_type = tf.cast(image_reshape, tf.float32)

        # 批处理，线程将队列中元素取完
        image_batch, label_batch =\
            tf.train.batch([image_type, label], batch_size=FLAGS.batch_size, num_threads=1, capacity=FLAGS.batch_size)

        return image_batch, label_batch

    # 将Tensor数据写入tfrecords文件中
    def write_to_tfrecords(self, image_batch, label_batch):

        # 构造一个文件储存器
        writer = tf.python_io.TFRecordWriter(FLAGS.tfrecords_dir)

        # 循环取出每个样本，构造example协议，序列化后写入文件
        for i in range(10):
            # 取出单个图片特征值和标签值
            image_string = image_batch[i].eval().tostring()
            label_string = int(label_batch[i].eval()[0])

            # 构造example协议
            example = tf.train.Example(features=tf.train.Feature(feature={
                "image": tf.train.Feature(bytes_list=tf.train.BytesList(value=[image_string])),
                "lebel": tf.train.Feature(int64_list=tf.train.Int64List(value=[label_string]))
            }))

            # 写入数据操作
            writer.write(example.SerializeToString())

        # 关闭储存器
        writer.close()

    def read_from_tfrecords(self, tfrecords_path):

        # 构建文件队列
        file_queue = tf.train.string_input_producer([tfrecords_path])

        # 构建文件阅读器，读取内容
        reader = tf.TFRecordReader()
        key, value = reader.read(file_queue)  # 一次取一个

        # 解析example协议，注意解析的只是一个样本
        features = tf.parse_single_example(value, features={
            "image": tf.FixedLenFeature([], tf.string),
            "label": tf.FixedLenFeature([], tf.int64)
        })

        # 如果图片是字符串数据则需要解码，整型则不需要
        image = tf.decode_raw(features["image"], tf.uint8)

        # 改变形状
        image_reshape = tf.reshape(image, [self.height, self.width, self.channel])
        image_tensor = tf.cast(image_reshape, tf.float32)

        # 改变标签值类型为tensor类型
        label = tf.cast(features["label"], tf.int32)

        # 批处理
        image_batch, label_batch = tf.train.batch([image_reshape, label], batch_size=10, num_threads=1, capacity=10)

        return image_batch, label_batch


if __name__ == "__main__":

    # 获取文件名的路径列表
    filename = os.listdir(FLAGS.data_dir)
    file_list = [os.path.join(FLAGS.data_dir, file) for file in filename if file[-3:] == "bin"]

    # 构造对象
    crf = CifarRead(file_list)

    # 从二进制中读取数据
    image_batch, label_batch = crf.read_and_decode()

    # 从TFRecords文件中读取
    tfrecords_path = "./data"
    image_batch, label_batch = crf.read_from_tfrecords(tfrecords_path)

    with tf.Session() as sess:
        # 开启线程协调器和线程 线程数量
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess, coord=coord)

        print(sess.run([image_batch, label_batch]))

        print("存进tfrecords文件中")
        crf.write_to_tfrecords(image_batch, label_batch)
        print("存进tfrecords文件结束")

        # 回收线程
        coord.request_stop()
        coord.join(threads)

