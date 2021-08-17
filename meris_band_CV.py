import matplotlib.pyplot as plt
import numpy
import excel_file as xl
import meris


def cv_cal(spectrum):
    band = meris.initial(spectrum)
    cv = []
    for i in range(len(band)):
        cv.append(numpy.std(band[i], ddof=1) / numpy.mean(band[i]) * 100)
    return cv


def read_spectrum(path, sheet, spectrum_type=None, spectrum_name=None, label=None):
    data = xl.xl_file(path, sheet)
    data.read_excel()
    cv_arr = []
    for i in range(data.table.nrows):
        if spectrum_type in data.table.row_values(i)[0] \
                or spectrum_name == data.table.row_values(i)[0]:
            spectrum = data.table.row_values(i)
            cv_arr.append(cv_cal(spectrum))
    cv_arr = numpy.array(cv_arr)
    plt.plot(meris.wave_length, cv_arr.mean(axis=0), label=label)


if __name__ == '__main__':
    read_spectrum('H:\\field work data\\最佳scan数选取\\scan 1.xlsx', 'Sheet1', spectrum_type='ASD', label='1 scan')
    read_spectrum('H:\\field work data\\最佳scan数选取\\scan 15.xlsx', 'Sheet1', spectrum_type='ASD', label='15 scans')
    read_spectrum('H:\\field work data\\最佳scan数选取\\scan 30.xlsx', 'Sheet1', spectrum_type='ASD', label='30 scans')
    read_spectrum('H:\\field work data\\最佳scan数选取\\scan 60.xlsx', 'Sheet1', spectrum_type='ASD', label='60 scans')
    plt.legend()
    plt.grid()
    plt.title('Coefficient of Variance')
    plt.ylabel('CV/%')
    plt.xlabel('wavelength/nm')
    meris.meris_band_display()
    plt.savefig('H:\\field work data\\最佳scan数选取\\cvfig.png')
    plt.show()
