import math
import numpy
import excel_file as xl
import matplotlib.pyplot as plt
from scipy import interpolate


xl_file = 'H:\\field work data\\20210323霞ヶ浦データ\\TriOS\\rrs by profile.xlsx'
sheet = '1'

srf = []
srf_wave = []

spec = []
spec_wave = []


def read_srf(band_num):
    srf_file = xl.xl_file('H:\\field work data\\计算参数\\MERIS响应函数.xlsx', 'NominalSRF Model2004')
    srf_file.read_excel()

    table = srf_file.table

    global srf_wave
    srf_wave = table.col_values(2 * band_num - 2)[2:]
    while '' in srf_wave:
        srf_wave.remove('')

    global srf
    srf = table.col_values(2 * band_num - 1)[2:]
    while '' in srf:
        srf.remove('')


def read_spec(file_name, sheet_name):
    spec_file = xl.xl_file(file_name, sheet_name)
    spec_file.read_excel()
    return spec_file.table


def modify():
    max_len = math.ceil(srf_wave[len(srf_wave) - 1])
    min_len = math.floor(srf_wave[0])

    meris_band = numpy.array(spec_wave)
    meris_spec = numpy.array(spec)

    for i in range(len(meris_band)):
        if meris_band[i] < min_len or meris_band[i] > max_len:
            meris_band[i] = 0

    mask = ~(meris_band == 0)
    meris_band = meris_band[mask]
    meris_spec = meris_spec[mask]

    # plt.scatter(meris_band, meris_spec)

    func = interpolate.UnivariateSpline(meris_band, meris_spec, s=0)
    y = func(srf_wave)

    # plt.plot(srf_wave, y)

    srf_result = 0
    for i in range(len(srf)):
        srf_result += srf[i]*y[i]

    srf_result /= numpy.sum(srf)
    return srf_result


def spec_to_meris(file_name, sheet_name):
    table = read_spec(file_name, sheet_name)
    global spec_wave
    global spec
    spec_wave = table.row_values(0)[1:]

    for i in range(1, table.nrows):
        spec = table.row_values(i)[1:]
        res_arr = []
        for j in range(1, 15):
            read_srf(j)
            res_arr.append(modify())
        print(res_arr)


if __name__ == '__main__':
    spec_to_meris(xl_file, sheet)
