import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# 分类中的箱线图
def draw_box(df, value_field, y_col):
    data = pd.concat([df[value_field], df[y_col]], axis=1)
    sns.set_color_codes(palette='deep')
    # 生成图
    f, ax = plt.subplots(figsize=(8, 6))
    fig = sns.lineplot(x=df[y_col], y=value_field, data=df)

    # 图形基本配置
    title_size = 26
    xy_label_size = 24
    xy_value_size = 18
    fontdict = {"family": "SimHei"}  # 字体相关

    plt.grid(b=True, ls=':', color='#606060')  # 网格
    plt.tick_params(labelsize=xy_value_size)  # 轴数值大小
    plt.ylabel(value_field, fontsize=xy_label_size, fontdict=fontdict)  # y轴标题
    plt.xlabel(y_col, fontsize=xy_label_size, fontdict=fontdict)  # x轴标题
    plt.title("折线图", fontsize=title_size, fontdict=fontdict)  # 标题
    sns.despine(trim=True, left=True)  # 去掉框线
    plt.yticks(rotation=360, horizontalalignment='right', fontname="SimHei")  # y轴值旋转
    plt.xticks(rotation=45, horizontalalignment='right', fontname="SimHei")   # x轴值旋转

    # 设置坐标字体方向
    # label_y = ax.get_yticklabels()
    # plt.setp(label_y, rotation=360, horizontalalignment='right')
    # label_x = ax.get_xticklabels()
    # plt.setp(label_x, rotation=45, horizontalalignment='right')

    plt.show()


def main():
    # df = pd.DataFrame(np.random.randint(0, 10, size=(300, 4)), columns=["a", "b", "c", "Y"])
    # print(df)
    # df.to_csv("data.csv")
    df = pd.read_csv("data.csv")
    draw_box(df, "a", "Y")


if __name__ == '__main__':
    main()

