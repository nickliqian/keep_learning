from keras.models import Sequential

model = Sequential()

from keras.layers import Dense, Activation

# 将各网络层通过add堆叠起来，构成模型
# Dense全连接层 units-输出维度
# Activation 激活层对一个层的输出施加激活函数
model.add(Dense(units=64, input_dim=100))
model.add(Activation("relu"))
model.add(Dense(units=10))
model.add(Activation("softmax"))

# 编译模型时必须指明损失函数和优化器 loss-损失函数 optimizer-优化器
model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

'''
# 自己定制优化器
from keras.optimizers import SGD
model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.01, momentum=0.9, nesterov=True))
'''


# 完成模型编译后，我们在训练数据上按batch进行一定次数的迭代来训练网络
model.fit(x_train, y_train, epochs=5, batch_size=32)

# 当然，我们也可以手动将一个个batch的数据送入网络中训练，这时候需要使用：
model.train_on_batch(x_batch, y_batch)

# 随后，我们可以使用一行代码对我们的模型进行评估，看看模型的指标是否满足我们的要求：
loss_and_metrics = model.evaluate(x_test, y_test, batch_size=128)

# 或者，我们可以使用我们的模型，对新的数据进行预测：
classes = model.predict(x_test, batch_size=128)
