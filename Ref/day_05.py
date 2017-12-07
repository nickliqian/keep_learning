# @Time    : 2017/10/7 上午8:54
# @File    : day_05.py
# @Software: PyCharm
import tensorflow as tf
import os


# 同步读取过程

## 1、创建队列、往队列里面填充内容
# Q = tf.FIFOQueue(3, tf.float32)
#
# en_many = Q.enqueue_many(([0.1, 0.2, 0.3], ))
#
# # 2、定义出队列，+1，入队列操作
# out_q = Q.dequeue()
#
# data = out_q + 1
#
# en_q = Q.enqueue(data)
#
# # 3、创建会话，去运行操作，或者读取队列数据
# with tf.Session() as sess:
#     sess.run(en_many)
#
#     # 先处理数据
#     for i in range(2):
#         sess.run(en_q)
#
#     # 取出数据
#     for i in range(Q.size().eval()):
#         print(sess.run(Q.dequeue()))


# 异步的读取过程，（主线程+子线程）
# 子线程，不断的往队列里面添加数据
# 主线程不需要等待队列填充满，直接去读取
# 需要添加线程同步的功能

# # 创建一个队列
# Q = tf.FIFOQueue(1000, tf.float32)
#
# # 定义变量，自增1，放入队列
# var = tf.Variable(0.0, tf.float32)
#
# encrement_op = tf.assign_add(var, tf.constant(1.0))
#
# en_q = Q.enqueue(encrement_op)
#
# # 创建队列管理器，添加入队列操作
# qr = tf.train.QueueRunner(Q, enqueue_ops=[en_q] * 1)
#
# # 初始化变量
# init_op = tf.global_variables_initializer()
#
# with tf.Session() as sess:
#     sess.run(init_op)
#
#     # 创建一个线程协调器
#     coord = tf.train.Coordinator()
#
#     threads = qr.create_threads(sess, coord=coord, start=True)
#
#     # 异步读取
#     for i in range(100):
#         print(sess.run(Q.dequeue()))
#
#     # 请求是否停止
#     coord.request_stop()
#
#     # 回收线程
#     coord.join(threads)

# def csvread(file_list):
#     """
#     读取CSV文件
#     :param file_list: 文件名的路径列表
#     :return: 数据
#     """
#     # 构建文件的队列
#     file_queue = tf.train.string_input_producer(file_list)
#
#     # 构建文件阅读器，读取内容
#     reader = tf.TextLineReader()
#
#     key, value = reader.read(file_queue)
#
#     # 解码内容，指定每一行的默认值或者缺省值，[["None"],["None"]]
#     records = [["None"], ["None"]]
#
#     example, label = tf.decode_csv(value, record_defaults=records)
#
#     # 批处理
#     example_batch, label_batch = tf.train.batch([example, label], batch_size=12, num_threads=1, capacity=20)
#
#     return examle_batch, label_batch
#
#
# if __name__ == "__main__":
#     # 找到文件的路径列表
#     filename = os.listdir("./data/csvdata/")
#
#     file_list = [os.path.join("./data/csvdata/", file) for file in filename]
#
#     print(file_list)
#
#     example_batch, label_batch = csvread(file_list)
#
#     # 会话
#     with tf.Session() as sess:
#         # 线程协调器
#         coord = tf.train.Coordinator()
#
#         # 开启线程操作
#         threads = tf.train.start_queue_runners(sess, coord=coord)
#
#         # 打印读取的内容
#         print(sess.run([example_batch, label_batch]))
#
#         # 回收线程
#         coord.request_stop()
#
#         coord.join(threads)


# 读取图片

# def picread(file_list):
#     """
#     读取狗的图片转换成张量
#     :param file_list: 图片名字路径
#     :return: image_batch
#     """
#     # 构造文件队列
#     file_queue = tf.train.string_input_producer(file_list)
#
#     # 构造阅读器，读取内容
#     reader = tf.WholeFileReader()
#
#     key, value = reader.read(file_queue)
#
#     # 解码图片
#     image = tf.image.decode_jpeg(value)
#
#     # 处理图片的大小，形状
#     image_size = tf.image.resize_images(image, [256, 256])
#
#     # print(image_size)
#
#     image_size.set_shape([256, 256, 3])
#
#     # print(image_size)
#     # 批处理,一定要确定图片的形状，否则批处理不知道读取多少图片
#     image_batch = tf.train.batch([image_size], batch_size=100, num_threads=1, capacity=100)
#
#     print(image_batch)
#
#     return image_batch
#
#
# if __name__ == "__main__":
#     # 找到文件的路径列表
#     filename = os.listdir("./data/dog/")
#
#     file_list = [os.path.join("./data/dog/", file) for file in filename]
#
#     image_batch = picread(file_list)
#
#     with tf.Session() as sess:
#         # 线程协调器
#         coord = tf.train.Coordinator()
#
#         # 开启线程
#         threads = tf.train.start_queue_runners(sess, coord=coord)
#
#         print(sess.run(image_batch))
#
#         # 回收线程
#         coord.request_stop()
#
#         coord.join(threads)


# cifar10图片二进制数据读取

tf.app.flags.DEFINE_string("data_dir", "./data/cifar10/cifar-10-batches-bin/", "二进制文件的目录")
tf.app.flags.DEFINE_string("tfrecords_dir", "./tmp/tfrecords/cifar10.tfrecords", "TFRecords文件的名字")

tf.app.flags.DEFINE_integer("batch_size", 100, "每批次读取数据的大小")


FLAGS = tf.app.flags.FLAGS


class CifarRead(object):

    def __init__(self, file_list):
        # 文件名的列表
        self.file_list = file_list

        # 定义图片属性
        self.height = 32
        self.width = 32
        self.channel = 3
        self.label_bytes = 1
        self.image_bytes = self.height * self.width * self.channel
        self.bytes = self.label_bytes + self.image_bytes

    def read_and_decode(self):
        """
        读取二进制图片数据
        :return: image_batch, label_batch
        """
        # 构造文件队列
        file_queue = tf.train.string_input_producer(self.file_list)
        print(self.file_list)

        # 构造阅读器，读取数据
        reader = tf.FixedLengthRecordReader(self.bytes)

        print(self.bytes)

        key, value = reader.read(file_queue)

        # 解码数据
        label_image = tf.decode_raw(value, tf.uint8)

        # 进行特征值和目标值的分割，类型的转换，形状的转换
        label = tf.cast(tf.slice(label_image, [0], [self.label_bytes]), tf.int32)

        image = tf.slice(label_image, [self.label_bytes], [self.image_bytes])

        print(image, label)

        # 形状改变（批处理要求）
        image_reshape = tf.reshape(image, [self.height, self.width, self.channel])

        # 类型改变
        image_type = tf.cast(image_reshape, tf.float32)

        # 批处理
        image_batch, label_batch = tf.train.batch([image_type, label], batch_size=FLAGS.batch_size, num_threads=1, capacity=FLAGS.batch_size)

        print(image_batch, label_batch)
        return image_batch, label_batch

    def write_to_tfrecords(self, image_batch, label_batch):
        """
        将Tensor数据写入到tfrecords文件
        :param image_batch: 批处理结果的图片特征值
        :param label_batch: 批处理结果的图片标签值
        :return: None
        """
        # 构造一个文件存储器
        writer = tf.python_io.TFRecordWriter(FLAGS.tfrecords_dir)

        # 循环取出每个样本，构造example协议，序列化后写入文件
        for i in range(10):
            print(image_batch[i], label_batch[i])
            # 取出单个图片特征值
            image_string = image_batch[i].eval().tostring()

            # 取出单个图片标签值
            label_int = int(label_batch[i].eval()[0])

            # 构造example协议
            example = tf.train.Example(features=tf.train.Features(feature={
                "image": tf.train.Feature(bytes_list=tf.train.BytesList(value=[image_string])),
                "label": tf.train.Feature(int64_list=tf.train.Int64List(value=[label_int]))
            }))

            writer.write(example.SerializeToString())

        writer.close()

        return None

    def read_from_tfrecords(self):
        """
        从TFRecords文件中读取数据
        :return: image_batch, label_batch
        """
        # 构建文件队列
        file_queue = tf.train.string_input_producer(["./tmp/tfrecords/cifar10.tfrecords"])

        # 构建文件阅读器，读取内容
        reader = tf.TFRecordReader()

        key, value = reader.read(file_queue)

        # 解析example协议,注意解析的只是一个样本（图片）数据
        features = tf.parse_single_example(value, features={
            "image": tf.FixedLenFeature([], tf.string),
            "label": tf.FixedLenFeature([], tf.int64)
        })

        # 如果是图片字符串数据要进行解码，整型不需要，形状改变，类型改变
        image = tf.decode_raw(features["image"], tf.uint8)

        # 改变形状
        image_reshape = tf.reshape(image, [self.height, self.width, self.channel])

        # 标签值
        label = tf.cast(features["label"], tf.int32)

        # image_tensor = tf.cast(image_reshape, tf.float32)

        # 批处理
        image_batch, label_batch = tf.train.batch([image_reshape, label], batch_size=10, num_threads=1, capacity=10)

        return image_batch, label_batch


if __name__ == "__main__":

    # 获取文件名的路径列表
    filename = os.listdir(FLAGS.data_dir)

    file_list = [os.path.join(FLAGS.data_dir, file) for file in filename if file[-3:] == "bin"]

    crf = CifarRead(file_list)

    # 从原始二进制文件中读取
    image_batch, label_batch = crf.read_and_decode()

    # 从TFRecords文件中读取
    # image_batch, label_batch = crf.read_from_tfrecords()

    # 会话
    with tf.Session() as sess:
        coord = tf.train.Coordinator()

        # 开启线程
        threads = tf.train.start_queue_runners(sess, coord=coord)

        print(sess.run([image_batch, label_batch]))

        print("存进tfrecords文件中")

        crf.write_to_tfrecords(image_batch, label_batch)

        print("存进tfrecords文件结束")

        # 回收线程
        coord.request_stop()

        coord.join(threads)




