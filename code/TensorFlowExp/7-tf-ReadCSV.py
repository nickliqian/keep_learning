import tensorflow as tf
import os


# 读取csv数据
def csvread(file_list):

    # 文件队列
    file_queue = tf.train.string_input_producer(file_list)

    # 构造阅读器
    reader = tf.TextLineReader()

    # 读取队列中文件的内容 key文件名字，value默认的内容(行，字节)
    # 执行一次value默认取一行,如果是批处理就会一直从队列中取出
    key, value = reader.read(file_queue)
    # print(key)  # 文件名称
    # print(value)  # 文件内容

    # 解码内容，指定每一行的默认值或者缺省值
    record = [['None'], ['None']]
    example, label = tf.decode_csv(value, record_defaults=record)  # shape=(?, ?, ?)
    # print(example)  # 列一
    # print(label)  # 列二

    # 批处理操作 - 指定处理的数据 [example, label]
    example_batch, label_batch = tf.train.batch([example, label], batch_size=12, num_threads=1, capacity=20)

    return example_batch, label_batch


if __name__ == "__main__":

    # 读取文件路径
    filename = os.listdir('D:\A\data\csvdata')
    file_list = [os.path.join('D:\A\data\csvdata', file) for file in filename]

    # 读取csv数据
    example, label = csvread(file_list)

    with tf.Session() as sess:
        # 线程协调器
        coord = tf.train.Coordinator()
        # 开启线程
        threads = tf.train.start_queue_runners(sess, coord=coord)

        # 执行计算
        print(sess.run([example, label]))

        # 回收线程
        coord.request_stop()
        coord.join(threads)
