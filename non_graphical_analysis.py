# анализ результатов обсчёта

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math


files_to_analyse = ['Samples/before_injection/(4).txt',
                    'Samples/before_injection/(5).txt',
                    'Samples/before_injection/(6).txt',
                    'Samples/before_injection/(8).txt',
                    'Samples/before_injection/(9).txt',]

# after- control
# files_to_analyse = ['Samples/after/1.txt',
#                     'Samples/after/1(2).txt',
#                     'Samples/after/2.txt',
#                     'Samples/after/3.txt',
#                     'Samples/after/7.txt',
#                     'Samples/after/10.txt',]

# after -- experiment
# files_to_analyse = ['Samples/after/4.txt',
#                     'Samples/after/5.txt',
#                     'Samples/after/6.txt',
#                     'Samples/after/8.txt',
#                     'Samples/after/9.txt',]


left_lower_all = []
left_upper_all = []
right_lower_all = []
right_upper_all = []


# func STEP returns a list of step legths
def step(step_list):
    steps = []
    for i, s in enumerate(step_list[:-1]):
        x1 = float(s[1:].split(', ')[0])               ##
        y1 = float(s[1:].split(', ')[1])                # get coordinates of current step
        x2 = float(step_list[i+1][1:].split(', ')[0])  # and the next one
        y2 = float(step_list[i+1][1:].split(', ')[1]) ##
        
        steps.append(math.hypot(abs(x1-x2), abs(y1-y2)))  # hypotenuse (=step length)
    return steps


for file in files_to_analyse:  # analyse all the files from the list
    with open(file, 'r') as file_paws: 
        file_list = file_paws.read().strip().split('\n')

        left_lower = file_list[0][19:]  ## 
        left_upper = file_list[1][21:]   #  read DATA
        right_upper = file_list[2][22:]  #  from input
        right_lower = file_list[3][20:] ##

        left_lower = [s.strip() for s in left_lower[1:-2].split('),')]     ## 
        left_upper = [s.strip() for s in left_upper[1:-2].split('),')]      #  convert 
        right_upper = [s.strip() for s in right_upper[1:-2].split('),')]    #  to list
        right_lower = [s.strip() for s in right_lower[1:-2].split('),')]   ##

        # print(tuple(float(item) for item in left_lower[0][1:].split(', ')))   # создание нормальных кортежей если вдруг надо

        left_lower_all.extend(step(left_lower))    ##
        left_upper_all.extend(step(left_upper))     #  lists with
        right_lower_all.extend(step(right_lower))   #  lengths of steps
        right_upper_all.extend(step(right_upper))  ##


y_means = [np.mean(left_lower_all),
         np.mean(left_upper_all),
         np.mean(right_lower_all),
         np.mean(right_upper_all)]

y_errors = [np.std(left_lower_all),
         np.std(left_upper_all),
         np.std(right_lower_all),
         np.std(right_upper_all)]

with open('Samples/after_experiment.txt', 'w') as f:
    f.write(str(y_means)[1:-1])
    f.write('\n')
    f.write(str(y_errors)[1:-1])

# x = np.arange(1,5)

# fig, axs = plt.subplots(2,2)
# axs[0][0].bar(x, y_means,
#            yerr = y_errors,
#            capsize = 5,
#            ecolor = 'red',
#            width = 0.3)
# axs[0][0].set_title('контроль (до)')
# axs[0][1].bar(x, y_means,
#            yerr = y_errors,
#            capsize = 5,
#            ecolor = 'red',
#            width = 0.3)
# axs[0][1].set_title('опыт (до)')
# axs[1][0].bar(x, y_means,
#            yerr = y_errors,
#            capsize = 5,
#            ecolor = 'red',
#            width = 0.3)
# axs[1][0].set_title('контроль (после)')
# axs[1][1].bar(x, y_means,
#            yerr = y_errors,
#            capsize = 5,
#            ecolor = 'red',
#            width = 0.3)
# axs[1][1].set_title('опыт (после)')

# plt.show()