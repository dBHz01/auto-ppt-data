import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from simplelog import cal_naive_time_separately_single, cal_naive_whole_time, cal_think_time, cal_time_separately, cal_time_separately_single 
from dp_office import cal_all_time, cal_ave_time
import seaborn as sns

def plot_separately():
    time = cal_think_time()
    ax = [0, 0, 0, 0]
    plot_time = [0, 0, 0, 0]
    for i in range(4):
        plot_time[i] = [np.array(j) for j in time[i]]
    for i in range(4):
        ax[i] = plt.subplot(2, 2, i + 1)
        # ax[1] = plt.subplot(2, 2, 2)
        # ax[2] = plt.subplot(2, 2, 3)
        # ax[3] = plt.subplot(2, 2, 4)
        cur_time = np.array([])
        for j in range(4):
            cur_time = np.concatenate((cur_time, plot_time[i][j]))
        df = pd.DataFrame({
            'time': cur_time,
            'label': [1] * len(plot_time[i][0]) + [2] * len(plot_time[i][1]) + [3] * len(plot_time[i][2]) + [4] * len(plot_time[i][3])
        })
        ax[i] = sns.boxplot(x="label", y="time", data=df)
    plt.show()

def plot_whole():
    time = cal_think_time()
    whole_time = [0, 0, 0, 0]
    cnt = [0, 0, 0, 0]
    for i in time:
        for j in range(4):
            # i[j] = [np.mean(i[j]), len(i[j])]
            if (i[j]):
                i[j] = np.mean(i[j])
                cnt[j] += 1
            else:
                i[j] = 0
            whole_time[j] += i[j]
    for j in range(4):
        whole_time[j] /= cnt[j]
    df = pd.DataFrame({
        'time': whole_time,
        'label': [1, 2, 3, 4]
    })
    sns.lineplot(x="label", y="time", data=df)
    plt.show()

if __name__ == "__main__":
    plot_whole()