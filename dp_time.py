import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from simplelog import cal_time_separately_single 
from dp_office import cal_all_time, cal_ave_time
import seaborn as sns
import scipy.stats

def cal_time():
    people_num = 12
    FIRST_PEOPLE = "azd crj cyy djy frw lly lzj tty xq ylc ytj zyx".split(" ")
    SECOND_PEOPLE = "lyf zyw zxy lgz lbc hmf zhp ywt dyc jjx xtx wzz".split(" ")
    our_time_0 = cal_time_separately_single(FIRST_PEOPLE)
    our_time_1 = cal_time_separately_single(SECOND_PEOPLE)
    our_time_flattern_0 = our_time_0.flatten()
    our_time_flattern_1 = our_time_1.flatten()
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
    our_time_0 = np.array(our_time_0)
    our_time_1 = np.array(our_time_1)
    office_time_0 = np.array(office_time_0)
    office_time_1 = np.array(office_time_1)
    our_whole_time_0 = (our_time_0[0] + our_time_0[1] + our_time_0[2] + our_time_0[3]) / 4
    our_whole_time_1 = (our_time_1[0] + our_time_1[1] + our_time_1[2] + our_time_1[3]) / 4
    office_whole_time_0 = (office_time_0[0] + office_time_0[1] + office_time_0[2] + office_time_0[3]) / 4
    office_whole_time_1 = (office_time_1[0] + office_time_1[1] + office_time_1[2] + office_time_1[3]) / 4
    print(f"mean: {np.mean(our_whole_time_0)} {np.mean(our_whole_time_1)} {np.mean(office_whole_time_0)} {np.mean(office_whole_time_1)}")
    print(f"std: {np.std(our_whole_time_0)} {np.std(our_whole_time_1)} {np.std(office_whole_time_0)} {np.std(office_whole_time_1)}")
    print(f"anova-0-1 {scipy.stats.f_oneway(our_whole_time_0, our_whole_time_1)}")
    print(f"anova-0-2 {scipy.stats.f_oneway(our_whole_time_0, office_whole_time_0)}")
    print(f"anova-0-3 {scipy.stats.f_oneway(our_whole_time_0, office_whole_time_1)}")
    print(f"anova-1-2 {scipy.stats.f_oneway(our_whole_time_1, office_whole_time_0)}")
    print(f"anova-1-3 {scipy.stats.f_oneway(our_whole_time_1, office_whole_time_1)}")
    print(f"anova-2-3 {scipy.stats.f_oneway(office_whole_time_0, office_whole_time_1)}")

if __name__ == "__main__":
    cal_time()