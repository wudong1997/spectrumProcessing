import excel_file as xl
import numpy as np
import matplotlib.pyplot as plt
import figure


def draw_series_spectrum(file_name, sheet_name,
                         spectrum_type=None, spectrum_name=None,
                         y_max=None, y_label=None,
                         sava_path=None, title=None):
    """
    绘制光谱
    :param title: 图表标题
    :param sava_path: 图片保存路径
    :param sheet_name: excel表格名称
    :param file_name: 文件名称
    :param y_label: 设置y轴标签
    :param y_max: 设置y轴最大值
    :param spectrum_type: 选择绘制TriOS光谱或是ASD光谱
    :param spectrum_name: 单独绘制某一条曲线
    """
    data = xl.xl_file(file_name, sheet_name)
    data.read_excel()
    x_range = np.arange(350, 951, 1)
    for i in range(data.table.nrows):
        if spectrum_type in data.table.row_values(i)[0] \
                or spectrum_name == data.table.row_values(i)[0]:
            spectrum = data.table.row_values(i)[1:]
            figure.draw_figure(x_range, spectrum,
                               x_min=350, x_max=950,
                               y_min=0, y_max=y_max,
                               y_label=y_label, x_label='wavelength/nm',
                               title=title)

    # um.Meris.meris_band_display()
    if sava_path is not None:
        plt.savefig(sava_path)
    plt.show()


if __name__ == '__main__':
    file = 'H:\\field work data\\20210323霞ヶ浦データ\\TriOS\\rrs by profile.xlsx'
    sheet = 'Sheet2'
    # save_path = 'H:\\field work data\\20210323霞ヶ浦データ\\TriOS\\underwater_profile.png'

    draw_series_spectrum(file, sheet,
                         spectrum_type='1',
                         y_max=0.012, y_label=r'$R_{rs}$', title='station_1')
