# анализ результатов обсчёта

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math


px_2_sm = lambda pxels: 0.081578328*pxels+ 0.16621237  # через LAMBDA и MAP конвертим списки в пикселях в САНТИМЕТРОВЫЕ


with open('Samples/before_control.txt', 'r') as f:
    f_text = f.read().strip().split('\n')
    y_means_before_control = list(float(s) for s in f_text[0].split(', '))
    y_errors_before_control = list(float(s) for s in f_text[1].split(', '))

    y_means_before_control = list(map(px_2_sm, y_means_before_control))
    y_errors_before_control = list(map(px_2_sm, y_errors_before_control))

with open('Samples/before_experiment.txt', 'r') as f:
    f_text = f.read().strip().split('\n')
    y_means_before_experiment = list(float(s) for s in f_text[0].split(', '))
    y_errors_before_experiment = list(float(s) for s in f_text[1].split(', '))

    y_means_before_experiment = list(map(px_2_sm, y_means_before_experiment))
    y_errors_before_experiment = list(map(px_2_sm, y_errors_before_experiment))

with open('Samples/after_control.txt', 'r') as f:
    f_text = f.read().strip().split('\n')
    y_means_after_control = list(float(s) for s in f_text[0].split(', '))
    y_errors_after_control = list(float(s) for s in f_text[1].split(', '))

    y_means_after_control = list(map(px_2_sm, y_means_after_control))
    y_errors_after_control = list(map(px_2_sm, y_errors_after_control))

with open('Samples/after_experiment.txt', 'r') as f:
    f_text = f.read().strip().split('\n')
    y_means_after_experiment = list(float(s) for s in f_text[0].split(', '))
    y_errors_after_experiment = list(float(s) for s in f_text[1].split(', '))

    y_means_after_experiment = list(map(px_2_sm, y_means_after_experiment))
    y_errors_after_experiment = list(map(px_2_sm, y_errors_after_experiment))


# SANTIMETERS = 0.081578328 * PIXELS + 0.16621237



# x = np.arange(1,5)
x = ['ЛЗ', 'ЛП', 'ПЗ', 'ПП']

fig, axs = plt.subplots(2,2)

axs[0][0].bar(x, y_means_before_control,
           yerr = y_errors_before_control,
           capsize = 5,
           ecolor = 'red',
           width = 0.3)
axs[0][0].set_title('контроль (до)')

axs[0][1].bar(x, y_means_before_experiment,
           yerr = y_errors_before_experiment,
           capsize = 5,
           ecolor = 'red',
           width = 0.3)
axs[0][1].set_title('опыт (до)')

axs[1][0].bar(x, y_means_after_control,
           yerr = y_errors_after_control,
           capsize = 5,
           ecolor = 'red',
           width = 0.3)
axs[1][0].set_title('контроль (после)')

axs[1][1].bar(x, y_means_after_experiment,
           yerr = y_errors_after_experiment,
           capsize = 5,
           ecolor = 'red',
           width = 0.3)
axs[1][1].set_title('опыт (после)')

plt.show()
