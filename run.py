import matplotlib.pyplot as plt
from rho import RMSE, correction
import underwater_measurement as um
import excel_file as xl
import numpy

excel = 'G:\\field work data\\20200317霞ヶ浦データ\\水下.xlsx'
irr_sheet = 'Ed'
rad_sheet = 'Lu'

Rrs_profile = um.rrs_cal(excel, irr_sheet, rad_sheet)

excel = xl.xl_file('G:\\field work data\\20200317霞ヶ浦データ\\rho拟合.xlsx', 'asd1')
excel.read_excel()
TriOS = correction(excel.get_row('TriOS'))[50:551]

rmse = RMSE(Rrs_profile, TriOS)
x_range = numpy.arange(400, 901, 1)
plt.cla()
plt.plot(x_range, Rrs_profile, color='red')
plt.plot(x_range, TriOS, color='blue')
plt.title('comparison of Rrs by SBA and profile')
plt.xlim(400, 900)
plt.text(800, 0.008, r'$RMSE=%.6f$' % rmse)
plt.grid()
plt.ylim(0)

plt.show()
