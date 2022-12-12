import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy import optimize
from dp_office import cal_all_time
from dp_txwj import getAveScore
from simplelog import cal_time_separately_single

def plotLine(x, y, x_scale=[], color='red'):
    # draw line, return x and y
    def residuals(p): 
        k,b = p
        return y - (k*x + b)
    r = optimize.leastsq(residuals, [1, 0])
    k, b = r[0]
    print ("k =" ,k, "b =" ,b)
    xx=np.arange(0,1000 / 60,1 / 60)
    if len(x_scale) != 0:
        xx=x_scale
    yy=k*xx+b
    correlation = np.corrcoef(y, x)[0,1]
    print("correlation", correlation**2)
    plt.plot(xx,yy,c=color)
    return xx, yy

def plot():
    people_num = 24
    ave_score = getAveScore()
    cnet_time = cal_time_separately_single()
    office_time = cal_all_time()
    # all_time = [[]]
    # all_score = [[]]
    # all_label = [[]]
    # c_time = [[]]
    # o_time = [[]]
    # c_score = [[]]
    # o_score = [[]]
    all_time = [[], [], [], []]
    all_score = [[], [], [], []]
    all_label = [[], [], [], []]
    c_time = [[], [], [], []]
    o_time = [[], [], [], []]
    c_score = [[], [], [], []]
    o_score = [[], [], [], []]
    for i in range(4):
        for j in range(people_num):
            all_time[i].append(cnet_time[i][j])
            c_time[i].append(cnet_time[i][j])
            all_label[i].append('CNET')
        for j in range(people_num):
            all_time[i].append(office_time[i][j])
            o_time[i].append(office_time[i][j])
            all_label[i].append('PPT')
    for i in range(4):
        for j in range(people_num):
            c_score[i].append(ave_score[i][j][0])
        for j in range(people_num, people_num * 2):
            o_score[i].append(ave_score[i][j][0])
        for j in range(people_num * 2):
            all_score[i].append(ave_score[i][j][0])

    # for i in range(3, 4):
    #     for j in range(12):
    #         all_time[0].append(cnet_time[i][j])
    #         c_time[0].append(cnet_time[i][j])
    #         all_label[0].append('CNET')
    #     for j in range(12):
    #         all_time[0].append(office_time[i][j])
    #         o_time[0].append(office_time[i][j])
    #         all_label[0].append('PPT')
    # for i in range(3, 4):
    #     for j in range(12):
    #         c_score[0].append(ave_score[i][j][0])
    #     for j in range(12, 24):
    #         o_score[0].append(ave_score[i][j][0])
    #     for j in range(24):
    #         all_score[0].append(ave_score[i][j][0])
    
    c_time = np.array(c_time).flatten()
    o_time = np.array(o_time).flatten()
    c_score = np.array(c_score).flatten()
    o_score = np.array(o_score).flatten()

    gap = 80
    x_right = np.array([gap * i for i in range(1, int(1000 / gap) + 1)])
    x_center = x_right - gap / 2
    basket = []
    for _ in range(len(x_center)):
        basket.append([])
    for i in range(len(o_time)):
        basket[int(o_time[i] / gap)].append(o_score[i])
    split_time_office = []
    split_score_office = []
    split_label = []
    for i in range(len(basket)):
        if basket[i]:
            split_time_office.append(x_center[i])
            split_score_office.append(np.mean(basket[i]))
            split_label.append("PPT-CENTER")
    
    basket = []
    for _ in range(len(x_center)):
        basket.append([])
    for i in range(len(c_time)):
        basket[int(c_time[i] / gap)].append(c_score[i])
    split_time_cnet = []
    split_score_cnet = []
    for i in range(len(basket)):
        if len(basket[i]) > 1:
            split_time_cnet.append(x_center[i])
            split_score_cnet.append(np.mean(basket[i]))
            split_label.append("CNET-CENTER")
    
    split_time_office = np.array(split_time_office).flatten()
    split_score_office = np.array(split_score_office).flatten()
    split_time_cnet = np.array(split_time_cnet).flatten()
    split_score_cnet = np.array(split_score_cnet).flatten()
    split_time = np.concatenate((split_time_office, split_time_cnet))
    split_score = np.concatenate((split_score_office, split_score_cnet))

    all_time = np.array(all_time).flatten() / 60
    all_score = np.array(all_score).flatten()
    all_label = np.array(all_label).flatten()

    # for i in range(len(all_label)):
    #     print("cur: ", i)
    # all_label_copy = all_label.copy()
    # all_label_copy[i] = 'CHOSEN'

    df = pd.DataFrame({
        'time': all_time,
        'score': all_score,
        'label': all_label,
    })
    # df = pd.DataFrame({
    #     'time': np.concatenate((np.array(all_time).flatten(), np.array(split_time).flatten())),
    #     'score': np.concatenate((np.array(all_score).flatten(), np.array(split_score).flatten())),
    #     'label': np.concatenate((np.array(all_label).flatten(), np.array(split_label).flatten())),
    # })
    # sns.scatterplot(x='time', y='score', hue='label', data=df, palette=['blue', 'yellow', 'red', 'black'])
    sns.scatterplot(x='time', y='score', hue='label', data=df)
    
    cnet_upper = [29, 32, 33, 48, 49, 59, 78, 79, 83]
    cnet_lower = [5, 9, 26, 28, 30, 35, 77]
    office_upper = [36, 37, 38, 40, 45, 60, 62, 84, 88, 92, 93]
    office_lower = [39, 47, 68, 87, 89]
    # x0, y0 = plotLine(np.array([all_time[i] for i in cnet_upper]), np.array([all_score[i] for i in cnet_upper]), np.arange(3, 8.8, 1/60), 'b')
    # x1, y1 = plotLine(np.array([all_time[i] for i in cnet_lower]), np.array([all_score[i] for i in cnet_lower]), np.arange(3, 8.8, 1/60), 'b')
    # x2, y2 = plotLine(np.array([all_time[i] for i in office_upper]), np.array([all_score[i] for i in office_upper]), np.arange(4, 14, 1/60), 'orange')
    # x3, y3 = plotLine(np.array([all_time[i] for i in office_lower]), np.array([all_score[i] for i in office_lower]), np.arange(4, 14, 1/60), 'orange')

    # plt.fill_between(x0, y1, y0, color='blue', alpha=0.2)
    # plt.fill_between(x2, y3, y2, color='orange', alpha=0.2)

    # plt.text(6, 92, "cnet upper bound")
    # plt.text(7.9, 78, "cnet lower bound")
    # plt.text(11.5, 72, "ppt upper bound")
    # plt.text(10, 42, "cnet lower bound")
    # plt.xlim(40 / 60, 1000 / 60)
    # plt.ylim(30, 100)
    plt.show()

if __name__ == "__main__":
    plot()