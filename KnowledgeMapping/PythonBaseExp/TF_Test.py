import tensorflow as tf
hello = tf.constant('Hello, TensorFlowExp!')
sess = tf.Session()
print(sess.run(hello))