import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from dp_txwj import getScore
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
    people_num = 20 * 12
    cnet_score, office_score, img_score = getScore()
    cnet_score = np.array(cnet_score)
    office_score = np.array(office_score)
    cnet_score_flattern = cnet_score.flatten()
    office_score_flattern = office_score.flatten()
    all_score = np.concatenate((cnet_score_flattern, office_score_flattern))
    df = pd.DataFrame({
        'score': all_score,
        'task': [1] * people_num + [2] * people_num + [3] * people_num + [4] * people_num + 
             [1] * people_num + [2] * people_num + [3] * people_num + [4] * people_num,
        'label': ["CNET"] * people_num * 4 + ["office"] * people_num * 4
    })
    print("average: cnet: {} office: {}".format(np.mean(cnet_score_flattern), np.mean(office_score_flattern)))
    print("total: {}".format((np.mean(cnet_score_flattern) - np.mean(office_score_flattern)) / np.mean(office_score_flattern)))
    print("separate: {}".format([(np.mean(cnet_score[i]) - np.mean(office_score[i])) / np.mean(office_score[i]) for i in range(4)]))
    for i in range(4):
        print(np.mean(cnet_score[i]))
        print(np.mean(office_score[i]))
        print("anova: task_{} {}".format(i + 1, scipy.stats.f_oneway(cnet_score[i], office_score[i])))
    sns.barplot(x="task", y="score", hue="label", data=df)
    plt.show()

if __name__ == "__main__":
    plot_with_sns()