import math
import matplotlib.pyplot as plt
import numpy
import excel_file as xl
import underwater_measurement as um


def correction(spectrum):
    Rrs_810 = spectrum[810 - 350]
    Rrs_780 = spectrum[780 - 350]
    Rrs_840 = spectrum[840 - 350]
    R_810 = Rrs_780 + (Rrs_840 - Rrs_780) * (810 - 780) / (840 - 780)
    RHW = Rrs_810 - R_810
    RR_810 = 16865.541 * math.pow(RHW, 3) + 52.728 * math.pow(RHW, 2) + 3.361 * RHW
    delta = Rrs_810 - RR_810

    for i in range(len(spectrum)):
        spectrum[i] = spectrum[i] - delta

    return spectrum


def RMSE(arr1, arr2):
    if len(arr1) != len(arr2):
        return

    sum = 0
    for i in range(len(arr1)):
        sum += math.pow((arr1[i] - arr2[i]), 2)
    return math.sqrt(sum / len(arr1))


excel = xl.xl_file('G:\\field work data\\20210323霞ヶ浦データ\\ASD\\rho值拟合.xlsx', 'Sheet1')
excel.read_excel()
gray = excel.get_row('gray')
sky = excel.get_row('Lsky')
Rg = excel.get_row('Rg')
Lu = excel.get_row('Lu')
#
# excel = 'G:\\field work data\\20200317霞ヶ浦データ\\水下.xlsx'
# irr_sheet = 'Ed'
# rad_sheet = 'Lu'

TriOS = excel.get_row('TriOS')

rho_max = 0.1
rho_min = 0.028

rho_arr = numpy.arange(rho_min, rho_max, 0.001)
x_range = numpy.arange(350, 951, 1)

Rrs_arr = []
min_RMSE = 9999
min_index = 0
index = 0
for rho in rho_arr:
    Rrs = []
    for i in range(len(gray)):
        Rrs.append((Lu[i] - rho * sky[i]) / (math.pi * gray[i] / Rg[i]))
    Rrs = correction(Rrs)

    delta = Rrs[810-350] - TriOS[810-350]
    for i in range(len(Rrs)):
        Rrs[i] = Rrs[i] - delta

    rmse = RMSE(Rrs, TriOS)

    if rmse < min_RMSE:
        min_RMSE = rmse
        min_index = index

    # plt.plot(x_range, Rrs, color='#3299CC')
    Rrs_arr.append(Rrs)
# 张浩然到此一游
    index += 1

plt.title('Rrs calculation with different p applied')

plt.plot(x_range, TriOS, color='#23238E')
plt.plot(x_range, Rrs_arr[0], color='black')
# plt.text(800, 0.006, r'$rho=%.3f$' % rho_arr[min_index])
plt.ylim(0, 0.014)
plt.xlim(400, 900)

plt.show()
