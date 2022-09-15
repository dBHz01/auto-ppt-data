import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import optimize
from dp_office import cal_all_time
from dp_txwj import getAveScore
from simplelog import cal_time_separately_single

def plot():
    ave_score = getAveScore()
    cnet_time = cal_time_separately_single()
    office_time = cal_all_time()
    all_time = [[], [], [], []]
    all_score = [[], [], [], []]
    all_label = [[], [], [], []]
    c_time = [[], [], [], []]
    o_time = [[], [], [], []]
    c_score = [[], [], [], []]
    o_score = [[], [], [], []]
    for i in range(4):
        for j in range(12):
            all_time[i].append(cnet_time[i][j])
            c_time[i].append(cnet_time[i][j])
            all_label[i].append('CNET')
        for j in range(12):
            all_time[i].append(office_time[i][j])
            o_time[i].append(office_time[i][j])
            all_label[i].append('PPT')
    for i in range(4):
        for j in range(12):
            c_score[i].append(ave_score[i][j][0])
        for j in range(12, 24):
            o_score[i].append(ave_score[i][j][0])
        for j in range(24):
            all_score[i].append(ave_score[i][j][0])
    df = pd.DataFrame({
        'time': np.array(all_time).flatten(),
        'score': np.array(all_score).flatten(),
        'label': np.array(all_label).flatten()
    })
    sns.scatterplot(x='time', y='score', hue='label', data=df)
    c_time = np.array(c_time).flatten()
    o_time = np.array(o_time).flatten()
    c_score = np.array(c_score).flatten()
    o_score = np.array(o_score).flatten()
    def residuals(p): 
        k,b = p
        return o_score - (k*o_time + b)
    r = optimize.leastsq(residuals, [1, 0]) 
    k, b = r[0]
    print ("k =" ,k, "b =" ,b)
    # #####将计算结果可视化
    XX=np.arange(1,1000,1)
    YY=k*XX+b
    correlation = np.corrcoef(o_score, o_time)[0,1]  #相关系数
    correlation**2
    print("correlation", correlation)
    print(o_time)
    print(o_score)
    plt.plot(XX,YY)
    # plt.plot(X,Y,'o')
    plt.show()

if __name__ == "__main__":
    plot()