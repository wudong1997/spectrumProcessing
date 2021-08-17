import matplotlib.pyplot as plt
import numpy as np


def draw_figure(x_arr, y_arr,
                x_label=None, y_label=None,
                x_min=None, y_min=None,
                x_max=None, y_max=None,
                marker=None, figure_type=None,
                title=None):
    """
    :param x_arr: x数组
    :param y_arr: y数组
    :param x_label: x标签
    :param y_label: y标签
    :param x_min: x轴最小值
    :param y_min: y轴最小值
    :param x_max: x轴最大值
    :param y_max: y轴最大值
    :param marker: 散点图点
    :param figure_type: 图表类型，默认是plot
    :param title: 图表标题
    :return:
    """
    plt.xlabel(x_label)  # 设置x坐标信息
    plt.ylabel(y_label)  # 设置y坐标信息

    # 设置坐标变化范围
    plt.ylim(y_min, y_max)
    plt.xlim(x_min, x_max)

    if figure_type == 'scatter':
        plt.scatter(x_arr, y_arr, marker=marker)  # 绘制散点图
    else:
        plt.plot(x_arr, y_arr)
    plt.title(title)
    plt.grid(True)  # 设置网格线


def figure_ax():
    ax = plt.gca()
    ax.spines['right'].set_color('none')  # 去掉右边边框
    ax.spines['bottom'].set_color('none')  # 去掉下边边框
    ax.xaxis.set_ticks_position('top')
    ax.yaxis.set_ticks_position('left')
    ax.spines['bottom'].set_position(('data', 0))  # 指定 data  设置的bottom(也就是指定的x轴)绑定到y轴的0这个点上
    ax.spines['left'].set_position(('data', 0))

