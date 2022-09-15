import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from dp_insts import candidate_ave_index
from dp_txwj import getScore
from simplelog import cal_naive_time_separately_single, cal_naive_whole_time, cal_time_separately, cal_time_separately_single 
from dp_office import cal_all_time, cal_ave_time
import seaborn as sns
import scipy.stats

def plot_with_sns():
    _, all_candidates = candidate_ave_index()
    wrong_num = 88
    accuracy = [1 - wrong_num / 2356]
    for i in range(4):
        wrong_num -= all_candidates[i]
        accuracy.append(1 - wrong_num / 2356)
    df = pd.DataFrame({
        'inst': accuracy,
        'task': ["top1", "top2", "top3", "top4", "top5"]
    })
    sns.barplot(x="task", y="inst", data=df)
    plt.show()

if __name__ == "__main__":
    plot_with_sns()