import tensorflow as tf
hello = tf.constant('Hello, TensorFlow Exp!')
sess = tf.Session()
print(sess.run(hello))