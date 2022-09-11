import pandas as pd
import numpy as np
import scipy.stats
# from statsmodels.formula.api import ols
# from statsmodels.stats.anova import anova_lm

TXWJ_FILENAME = "score-txwj.txt"

task_seq = [[3, 13, 12, 9, 10, 20, 8, 7, 11, 18, 6, 19, 2, 15, 4, 14, 22, 1, 21, 17, 5, 16, 23, 24],
            [2, 4, 8, 23, 3, 14, 11, 15, 5, 17, 16, 18, 20, 10, 1, 12, 21, 19, 7, 9, 24, 6, 13, 22],
            [20, 10, 12, 14, 18, 7, 9, 15, 2, 19, 1, 16, 6, 4, 22, 17, 24, 13, 23, 3, 11, 21, 8, 5],
            [8, 6, 21, 12, 18, 2, 16, 1, 20, 7, 15, 19, 3, 10, 24, 4, 23, 22, 17, 14, 13, 11, 5, 9]]

def raw_id(id, task):
    # id start from 1
    return task_seq[task][id - 1]

cnet_score = []
for i in range(4):
    cnet_score.append([])
cnet_seq = []
for i in range(4):
    cnet_seq.append([])
office_score = []
for i in range(4):
    office_score.append([])
office_seq = []
for i in range(4):
    office_seq.append([])

if __name__ == "__main__":
    with open(TXWJ_FILENAME, "r") as f:
        data = f.read().split("\n")
        for line in data:
            line = line.split("\t")
            seq = [0] * 24 # 第 i 位表示第 i 张图的名次
            for task_id in range(4):
                for i in range(24):
                    id = 48 * task_id + i
                    seq[i] = int(line[id])
                    if (raw_id(i + 1, task_id) <= 12):
                        cnet_seq[task_id].append(int(line[id]))
                    else:
                        office_seq[task_id].append(int(line[id]))
                # for i in range(24):
                #     id = 48 * task_id + i
                #     seq.append(raw_id(int(line[id]), task_id))
                #     if (raw_id(int(line[id]), task_id) <= 12):
                #         cnet_seq[task_id].append(i)
                #     else:
                #         office_seq[task_id].append(i)
                for i in range(24):
                    id = 48 * task_id + 24 + i
                    if (raw_id(seq.index(i + 1) + 1, task_id) <= 12):
                        cnet_score[task_id].append(int(line[id]))
                    else:
                        office_score[task_id].append(int(line[id]))
            # print(seq)
        # print(np.mean(np.array(cnet_score)))
        # print(np.mean(np.array(office_score)))
        # print(np.mean(np.array(cnet_seq)))
        # print(np.mean(np.array(office_seq)))
        for i in range(4):
            print("task {} cnet average score: {} ppt average score: {}".format(i + 1, np.mean(cnet_score[i]), np.mean(office_score[i])))
            # print("wilcoxon: {}".format(scipy.stats.wilcoxon(cnet_score[i], office_score[i])))
            print("task {} cnet average rank: {} ppt average rank: {}".format(i + 1, np.mean(cnet_seq[i]), np.mean(office_seq[i])))
            # print("wilcoxon: {}".format(scipy.stats.wilcoxon(cnet_seq[i], office_seq[i])))
            print("anova: {}".format(scipy.stats.f_oneway(cnet_score[i], office_score[i])))
            print()

