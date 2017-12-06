import tensorflow as tf
import os


# 读取图片
def picread(file_list):

    # 文件队列
    file_queue = tf.train.string_input_producer(file_list)

    # 构造阅读器
    reader = tf.WholeFileReader()

    # 读取队列中文件的内容
    key, value = reader.read(file_queue)
    # print(key)  # Tensor("ReaderReadV2:0", shape=(), dtype=string)
    # print(value)  # Tensor("ReaderReadV2:1", shape=(), dtype=string)

    # 解码图片文件
    images = tf.image.decode_jpeg(value)  # shape=(?, ?, ?)

    # 处理图片的大小和形状
    image_size = tf.image.resize_images(images, size=[256, 256])  # shape=(256, 256, ?)
    image_size.set_shape([256, 256, 3])  # shape=(256, 256, 3)

    # 批处理 - *批处理前需要确定图片的形状是否完整
    # batch_size 处理个数；num_threads 线程数量；capacity 队列中元素的最大数量；
    image_bath = tf.train.batch([image_size], batch_size=100, num_threads=1, capacity=100)  # shape=(100, 256, 256, 3)
    return image_bath


if __name__ == "__main__":

    # 读取文件路径
    filename = os.listdir('D:\A\data\dog')
    file_list = [os.path.join('D:\A\data\dog', file) for file in filename]

    # 读取图片
    image = picread(file_list)

    with tf.Session() as sess:
        # 线程协调器
        coord = tf.train.Coordinator()
        # 开启线程
        threads = tf.train.start_queue_runners(sess, coord=coord)

        # 执行计算
        print(sess.run(image))

        # 回收线程
        coord.request_stop()
        coord.join(threads)
