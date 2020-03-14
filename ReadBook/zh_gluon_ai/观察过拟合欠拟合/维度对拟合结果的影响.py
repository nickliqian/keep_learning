import torch
import torch.nn as nn
import numpy as np
import sys
sys.path.append("../")
import d2lzh1981 as d2l
from matplotlib import pyplot as plt

print(torch.__version__)


# 定义参数初始化函数，初始化模型参数并且附上梯度
def init_params():
    w = torch.randn((num_inputs, 1), requires_grad=True)
    b = torch.zeros(1, requires_grad=True)
    return [w, b]


def l2_penalty(w):
    return (w**2).sum() / 2


def semilogy(x_vals, y_vals, x_label, y_label, x2_vals=None, y2_vals=None,
             legend=None, figsize=(3.5, 2.5)):
    """
    x_vals 第一组点 x
    y_vals 第二组点 y
    x_label x轴名称
    y_label y轴名称
    x2_vals 第一组点 x
    y2_vals 第一组点 y
    legend 图例
    figsize 图的尺寸
    """
    # d2l.set_figsize(figsize)
    d2l.plt.xlabel(x_label)
    d2l.plt.ylabel(y_label)
    d2l.plt.semilogy(x_vals, y_vals)
    if x2_vals and y2_vals:
        d2l.plt.semilogy(x2_vals, y2_vals, linestyle=':')
        d2l.plt.legend(legend)

    plt.savefig("num_inputs_{}.png".format(num_inputs))
    plt.show()


def fit_and_plot(lambd):
    """
    超参数 lambd
    """
    w, b = init_params()  # 参数初始化
    train_ls, test_ls = [], []  # 损失列表
    for _ in range(num_epochs):
        for X, y in train_iter:
            # 添加了L2范数惩罚项
            l = loss(net(X, w, b), y) + lambd * l2_penalty(w)  # 计算损失
            l = l.sum()  # 向量加和

            # 梯度归零
            if w.grad is not None:
                w.grad.data.zero_()
                b.grad.data.zero_()
            l.backward()  # 计算梯度

            d2l.sgd([w, b], lr, batch_size)  # 梯度下降优化参数
        train_ls.append(loss(net(train_features, w, b), train_labels).mean().item())
        test_ls.append(loss(net(test_features, w, b), test_labels).mean().item())
    semilogy(range(1, num_epochs + 1), train_ls, 'epochs', 'loss',
                 range(1, num_epochs + 1), test_ls, ['train', 'test'])
    print('L2 norm of w:', w.norm().item())


if __name__ == '__main__':
    n_train, n_test, num_inputs = 20, 100, 100
    true_w, true_b = torch.ones(num_inputs, 1) * 0.01, 0.05

    features = torch.randn((n_train + n_test, num_inputs))
    labels = torch.matmul(features, true_w) + true_b
    labels += torch.tensor(np.random.normal(0, 0.01, size=labels.size()), dtype=torch.float)
    train_features, test_features = features[:n_train, :], features[n_train:, :]
    train_labels, test_labels = labels[:n_train], labels[n_train:]

    batch_size, num_epochs, lr = 1, 100, 0.003
    net, loss = d2l.linreg, d2l.squared_loss

    dataset = torch.utils.data.TensorDataset(train_features, train_labels)
    train_iter = torch.utils.data.DataLoader(dataset, batch_size, shuffle=True)

    # 维度太多导致过拟合
    fit_and_plot(lambd=0)