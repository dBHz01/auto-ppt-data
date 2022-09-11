import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from simplelog import cal_naive_time_separately_single, cal_naive_whole_time, cal_time_separately, cal_time_separately_single 
from dp_office import cal_all_time, cal_ave_time
import seaborn as sns

def plot_with_matplotlib():
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
    people_num = 8
    new_people_num = 12
    our_time = cal_time_separately_single().flatten()
    naive_time = cal_naive_whole_time().flatten()
    office_time = np.array(cal_all_time().flatten(), dtype=np.float64)
    all_time = np.concatenate((our_time, office_time))
    all_time = np.concatenate((all_time, naive_time))
    df = pd.DataFrame({
        'time': all_time,
        'task': [1] * new_people_num + [2] * new_people_num + [3] * new_people_num + [4] * new_people_num + 
             [1] * people_num + [2] * people_num + [3] * people_num + [4] * people_num +
             [1] * people_num + [2] * people_num + [3] * people_num + [4] * people_num,
        'label': ["CNET"] * new_people_num * 4 + ["office"] * people_num * 4 + ["naive"] * people_num * 4
    })
    sns.barplot(x="task", y="time", hue="label", data=df)
    plt.show()


if __name__ == "__main__":
    plot_with_sns()