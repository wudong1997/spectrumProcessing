import numpy
import matplotlib.pyplot as plt
from sklearn import linear_model
import scipy.stats as stats
import math
import excel_file as xl
import meris
import figure


def draw_spectrum(x_arr, y_arr, title=None):
    plt.cla()
    plt.plot(x_arr, y_arr)
    plt.title(title)
    plt.grid()


class spectrum:
    depth = None
    radiance = None
    ln_rad = None
    par_dep = None

    def __init__(self, depth, radiance, par_dep=None):
        self.depth = depth
        self.radiance = radiance
        self.ln_rad = []

    def rebuild_arr(self, par_dep=-10000):
        """
        重建数组,剔除无效值
        """
        for i in range(len(self.depth)):
            self.depth[i] = -1 * self.depth[i]  # 将深度值转换为负数

        shallowest = 0  # 最浅深度，排除传感器浮出水面的情况
        deepest = len(self.depth)
        for i in range(len(self.depth)):
            if self.depth[i] < 0:
                shallowest = i
                break

        for i in range(len(self.depth)):
            if self.depth[i] < par_dep:
                deepest = i
                break

        for i in range(len(self.depth)):
            if i < shallowest:
                self.ln_rad.append(None)
            elif self.radiance[i] > 0 and i <= deepest:
                ln_rad_value = numpy.log(self.radiance[i])
                self.ln_rad.append(ln_rad_value)
            else:
                self.ln_rad.append(None)

        self.ln_rad = numpy.array(self.ln_rad)
        self.depth = numpy.array(self.depth)
        self.radiance = numpy.array(self.radiance)

        mask = ~(self.ln_rad == None)
        self.ln_rad = self.ln_rad[mask]
        self.depth = self.depth[mask]
        self.radiance = self.radiance[mask]


class regression:
    x = None
    y = None
    slope = None
    intercept = None
    corr = None

    rad_just_blow_surface = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def linear_regression(self, showplt=None):
        figure.draw_figure(self.x, self.y, y_min=-5, y_max=0, x_min=-3, x_max=14, figure_type='scatter')


        # 计算线性回归的斜率和截距
        model = linear_model.LinearRegression()
        model.fit(self.x.reshape(-1, 1), self.y.reshape(-1, 1))
        b = model.intercept_[0]
        k = model.coef_[0]

        x_range = numpy.arange(numpy.min(self.x), numpy.max(self.x) + 1,
                               (numpy.max(self.x) + 1 - numpy.min(self.x)) / 10)
        y_range = k * x_range + b
        plt.plot(x_range, y_range, linestyle='--', color='red')

        corr = stats.pearsonr(self.x, self.y)[0]
        Kd = 1/k
        # plt.text(1, -4.5, r'$K=%.2f$' % Kd)
        # plt.text(1, -4.7, r'$corr=%.2f$' % corr)
        # if showplt:
        #     figure.figure_ax()
        #     plt.show()

        self.slope = k
        self.intercept = b
        self.corr = corr

    def just_under_water_radiance(self, showplt=None):
        """
        计算恰好在水面下的辐射
        """
        self.linear_regression(showplt=showplt)
        rad_0 = math.exp(-self.intercept/self.slope)
        return rad_0


def under_water_spectrum(filename, sheet_name, showplt=None):
    data = xl.xl_file(filename, sheet_name)
    data.read_excel()
    unw_rad = []
    for i in range(len(meris.band_name)):
        rad_arr = xl.xl_file.get_column(data, meris.band_name[i])
        depth_arr = xl.xl_file.get_column(data, ' Depth')
        sp = spectrum(depth_arr, rad_arr)
        sp.rebuild_arr()
        reg = regression(sp.ln_rad, sp.depth)
        unw_value = reg.just_under_water_radiance(showplt=showplt)
        unw_rad.append(unw_value)
    return unw_rad


def under_water_full_spectrum(filename, sheet_name, showplt=None):
    par_dep = par_depth(filename, sheet_name)
    data = xl.xl_file(filename, sheet_name)
    data.read_excel()
    unw_rad = []
    slope_arr =[]
    r2 = []
    band_name = data.table.row_values(0)[5:606]

    for i in range(len(band_name)):
        rad_arr = xl.xl_file.get_column(data, str(band_name[i]))
        depth_arr = xl.xl_file.get_column(data, ' Depth')
        sp = spectrum(depth_arr, rad_arr)
        sp.rebuild_arr(par_dep=-par_dep)
        reg = regression(sp.ln_rad, sp.depth)
        unw_value = reg.just_under_water_radiance(showplt=showplt)
        unw_rad.append(unw_value)
        slope_arr.append(1/reg.slope)
        r2.append(reg.corr)
    # draw_spectrum(band_name, slope_arr, title="Diffuse Attenuation coefficient")
    # meris.meris_band_display()
    # plt.show()
    # draw_spectrum(band_name, r2, title=r"$R^2$")
    # plt.show()
    return unw_rad, slope_arr


def rrs_cal(filename, sheet_irr, sheet_rad):
    band_name = numpy.arange(400, 901, 1)

    Ed_arr, Kd = under_water_full_spectrum(filename, sheet_irr, showplt=False)

    Lu_arr, Kt = under_water_full_spectrum(filename, sheet_rad, showplt=False)

    Rrs = ['Rrs ' + sheet_irr]
    for i in range(len(Ed_arr)):
        rrs = Lu_arr[i]/Ed_arr[i]
        Rrs_value = 0.52 * rrs / (1 - 1.7 * rrs)
        Rrs.append(Rrs_value)

    # draw_spectrum(band_name, Ed_arr, title=r"$E_d(0^-)$")
    # plt.ylabel(r"$E_d(0^-)$")
    # plt.xlabel("wavelength/nm")
    # plt.ylim(0)
    # plt.savefig('H:\\field work data\\20210323霞ヶ浦データ\\TriOS\\水下\\figure\\'+sheet_irr+'Ed0.png')
    # plt.show()
    # plt.cla()

    # draw_spectrum(band_name, Lu_arr, title=r"$L_u(0^-)$")
    # plt.ylabel(r"$L_u(0^-)$")
    # plt.xlabel("wavelength/nm")
    # plt.ylim(0)
    # plt.savefig('H:\\field work data\\20210323霞ヶ浦データ\\TriOS\\水下\\figure\\'+sheet_irr+'Lu0.png')
    # plt.show()
    # plt.cla()

    # draw_spectrum(band_name, Rrs[1:], title=r"$R_{rs}(0^-)$")
    # plt.ylabel(r"$R_{rs}(0^-)$")
    # plt.xlabel("wavelength/nm")
    # plt.ylim(0, 0.014)
    # plt.savefig('H:\\field work data\\20210323霞ヶ浦データ\\TriOS\\水下\\figure\\'+sheet_irr+'Rrs.png')
    # plt.show()

    # ktkd = []
    # for i in range(len(Kd)):
    #     ktkd.append(Kt[i]/Kd[i])
    # plt.plot(band_name, ktkd)
    # meris.meris_band_display()
    # plt.show()
    return Rrs[1:]


def transparency(filename, sheet_name):
    Ed0, slope, intercept = profile_regression(filename,sheet_name)
    # Method 1 透明度处所对应的下行辐照度Ed(z) = 18%Ed(0) from Lee et al.(2018)
    trans_depth_rad = numpy.log(Ed0 * 0.18)
    trans = - (slope * trans_depth_rad + intercept)
    # Method 2 Zsd = 1.48/K(PAR) from Lee et al.(2018)
    ano_result = 1.48*slope
    print('The transparency of this point is %.2f' % trans)
    print('For another method, the transparency is %.2f' % ano_result)


def profile_regression(filename, sheet_name):
    data = xl.xl_file(filename, sheet_name)
    data.read_excel()
    band_integration = []
    band_sum = 0
    for i in range(1, data.table.nrows):
        for j in range(55, data.table.ncols - 250):
            band_sum += data.table.cell_value(i, j)
        band_integration.append(band_sum)
        band_sum = 0

    depth = data.get_column(' Depth')
    sp = spectrum(depth, band_integration)
    sp.rebuild_arr()

    rg = regression(sp.ln_rad, sp.depth)
    rg.linear_regression(showplt=True)

    Ed0 = rg.just_under_water_radiance(showplt=False)
    return Ed0, rg.slope, rg.intercept


def par_depth(filename, sheet_name):
    Ed0, slope, intercept = profile_regression(filename, sheet_name)
    par_dep = - (slope * numpy.log(Ed0 * 0.03) + intercept)

    return par_dep


if __name__ == '__main__':
    excel = 'G:\\field work data\\20200317霞ヶ浦データ\\水下.xlsx'
    irr_sheet = 'Ed'
    rad_sheet = 'Lu'

    rrs_cal(excel, irr_sheet, rad_sheet)
    transparency(excel, irr_sheet)
    # under_water_full_spectrum(excel, irr_sheet)
