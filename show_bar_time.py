import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from simplelog import cal_naive_time_separately_single, cal_naive_whole_time, cal_time_separately, cal_time_separately_single 
from dp_office import cal_all_time, cal_ave_time
import seaborn as sns
import scipy.stats

def plot_with_matplotlib():
    # 错误的，不要跑
    our_time = cal_time_separately()
    office_time = cal_ave_time()
    print("total: ", (np.sum(office_time) - np.sum(our_time)) / np.sum(office_time))
    print("separate: ", [(office_time[i] - our_time[i]) / office_time[i] for i in range(4)])
    print(our_time)
    print(office_time)
    # 用来正常显示负号
    plt.rcParams['axes.unicode_minus']=False

    fig,ax=plt.subplots()

    fig_width = 0.25
    ax.bar([1, 2, 3, 4], our_time, fig_width, color='r', label="our")
    ax.bar(np.array([1, 2, 3, 4]) + fig_width, office_time, fig_width, color='b', label="office")
    ax.set_xticks(np.array([1, 2, 3, 4]) + fig_width / 2)
    ax.set_xticklabels(['1', '2', '3', '4'])

    # ax.set_title('')

    ax.legend()

    plt.show()

def plot_with_sns():
    people_num = 24
    our_time = cal_time_separately_single()
    our_time_flattern = cal_time_separately_single().flatten()
    # naive_time = cal_naive_whole_time().flatten()
    office_time = np.array(cal_all_time(), dtype=np.float64)
    office_time_flattern = np.array(cal_all_time(), dtype=np.float64).flatten()
    all_time = np.concatenate((our_time_flattern, office_time_flattern))
    # all_time = np.concatenate((all_time, naive_time))
    df = pd.DataFrame({
        'time': all_time,
        'task': [1] * people_num + [2] * people_num + [3] * people_num + [4] * people_num + 
             [1] * people_num + [2] * people_num + [3] * people_num + [4] * people_num,
        'label': ["CNET"] * people_num * 4 + ["office"] * people_num * 4
    })
    print("total: {}".format((np.mean(office_time_flattern) - np.mean(our_time_flattern)) / np.mean(office_time_flattern)))
    print("separate: {}".format([(np.mean(office_time[i]) - np.mean(our_time[i])) / np.mean(office_time[i]) for i in range(4)]))
    for i in range(4):
        print(np.mean(our_time[i]))
        print(np.mean(office_time[i]))
        print("anova: task_{} {}".format(i + 1, scipy.stats.f_oneway(our_time[i], office_time[i])))
    sns.barplot(x="task", y="time", hue="label", data=df)
    plt.show()

def plot_separately():
    people_num = 12
    FIRST_PEOPLE = "azd crj cyy djy frw lly lzj tty xq ylc ytj zyx".split(" ")
    SECOND_PEOPLE = "lyf zyw zxy lgz lbc hmf zhp ywt dyc jjx xtx wzz".split(" ")
    our_time_0 = cal_time_separately_single(FIRST_PEOPLE)
    our_time_1 = cal_time_separately_single(SECOND_PEOPLE)
    our_time_flattern_0 = our_time_0.flatten()
    our_time_flattern_1 = our_time_1.flatten()
    # naive_time = cal_naive_whole_time().flatten()
    FIRST_OFFICE_FILENAME = "office-time-0.txt"
    SECOND_OFFICE_FILENAME = "office-time-1.txt"
    office_time_0 = np.array(cal_all_time(filename=FIRST_OFFICE_FILENAME, start=0), dtype=np.float64)
    office_time_flattern_0 = np.array(office_time_0, dtype=np.float64).flatten()
    office_time_1 = np.array(cal_all_time(filename=SECOND_OFFICE_FILENAME, start=12), dtype=np.float64)
    office_time_flattern_1 = np.array(office_time_1, dtype=np.float64).flatten()
    all_time = np.concatenate((our_time_flattern_0, our_time_flattern_1, office_time_flattern_0, office_time_flattern_1))
    df = pd.DataFrame({
        'time': all_time,
        'task': [1] * people_num + [2] * people_num + [3] * people_num + [4] * people_num + 
             [1] * people_num + [2] * people_num + [3] * people_num + [4] * people_num + 
             [1] * people_num + [2] * people_num + [3] * people_num + [4] * people_num +
             [1] * people_num + [2] * people_num + [3] * people_num + [4] * people_num ,
        'label': ["CNET-0"] * people_num * 4 + ["CNET-1"] * people_num * 4 + ["office-0"] * people_num * 4 + ["office-1"] * people_num * 4
    })
    print("total-0: {}".format((np.mean(office_time_flattern_0) - np.mean(our_time_flattern_0)) / np.mean(office_time_flattern_0)))
    print("total-1: {}".format((np.mean(office_time_flattern_1) - np.mean(our_time_flattern_1)) / np.mean(office_time_flattern_1)))
    print("separate-0: {}".format([(np.mean(office_time_0[i]) - np.mean(our_time_0[i])) / np.mean(office_time_0[i]) for i in range(4)]))
    print("separate-1: {}".format([(np.mean(office_time_1[i]) - np.mean(our_time_1[i])) / np.mean(office_time_1[i]) for i in range(4)]))
    for i in range(4):
        # print(np.mean(our_time[i]))
        # print(np.mean(office_time[i]))
        print("anova-0: task_{} {}".format(i + 1, scipy.stats.f_oneway(our_time_0[i], office_time_0[i])))
        print("anova-1: task_{} {}".format(i + 1, scipy.stats.f_oneway(our_time_1[i], office_time_1[i])))
    sns.barplot(x="task", y="time", hue="label", data=df)
    plt.show()

if __name__ == "__main__":
    plot_with_sns()