import numpy as np
import matplotlib.pyplot as plt

band_name = ['412.0', '442.0', '490.0', '510.0', '560.0',
             '620.0', '665.0', '682.0', '709.0', '754.0',
             '761.0', '779.0', '865.0', '885.0', '900.0']

wave_length = [412, 442, 490, 510, 560, 620, 665,
               681, 709, 754, 762, 779, 865, 885, 900]

band_center_wavelength \
    = np.array(wave_length)


def meris_band_display():
    plt.axvspan(402.5, 422.5, facecolor='#696969', alpha=0.3)  # band1 412.5 ± 10
    plt.text(402.5, 0, 'B1')
    plt.axvspan(432.5, 452.5, facecolor='#808080', alpha=0.3)  # band2 442.5 ± 10
    plt.text(432.5, 0, 'B2')
    plt.axvspan(480, 500, facecolor='#696969', alpha=0.3)  # band3 490 ± 10
    plt.text(480, 0, 'B3')
    plt.axvspan(500, 520, facecolor='#808080', alpha=0.3)  # band4 510 ± 10
    plt.text(500, 0, 'B4')
    plt.axvspan(550, 570, facecolor='#696969', alpha=0.3)  # band5 560 ± 10
    plt.text(550, 0, 'B5')
    plt.axvspan(610, 630, facecolor='#808080', alpha=0.3)  # band6 620 ± 10
    plt.text(610, 0, 'B6')
    plt.axvspan(655, 675, facecolor='#696969', alpha=0.3)  # band7 665 ± 10
    plt.text(655, 0, 'B7')
    plt.axvspan(673.75, 688.75, facecolor='#808080', alpha=0.3)  # band8 681.25 ± 7.5
    plt.text(673.75, 0, 'B8')
    plt.axvspan(698.75, 718.75, facecolor='#696969', alpha=0.3)  # band9 708.75 ± 10
    plt.text(698.75, 0, 'B9')
    plt.axvspan(746.25, 761.25, facecolor='#808080', alpha=0.3)  # band10 753.75 ± 7.5
    plt.text(746.25, 0, 'B10-B12')
    plt.axvspan(756.875, 764.375, facecolor='#696969', alpha=0.3)  # band11 760.625 ± 3.75
    plt.axvspan(763.75, 793.75, facecolor='#808080', alpha=0.3)  # band12 778.75 ± 15
    plt.axvspan(863, 867, facecolor='#696969', alpha=0.3)  # band13 865 ± 2
    plt.text(863, 0, 'B13-B15')
    plt.axvspan(875, 895, facecolor='#808080', alpha=0.3)  # band14 885 ± 10
    plt.axvspan(890, 910, facecolor='#696969', alpha=0.3)  # band15 900 ± 10


def initial(data_array):
    band = np.array([data_array[403 - 349: 422 - 349], data_array[433 - 349: 452 - 349],
                     data_array[480 - 349: 500 - 349], data_array[500 - 349: 520 - 349],
                     data_array[550 - 349: 570 - 349], data_array[610 - 349: 630 - 349],
                     data_array[655 - 349: 675 - 349], data_array[674 - 349: 688 - 349],
                     data_array[699 - 349: 718 - 349], data_array[747 - 349: 761 - 349],
                     data_array[757 - 349: 764 - 349], data_array[764 - 349: 793 - 349],
                     data_array[863 - 349: 867 - 349], data_array[875 - 349: 895 - 349],
                     data_array[890 - 349: 910 - 349]])
    return band
