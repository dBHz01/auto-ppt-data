import pandas as pd
import numpy as np
import scipy.stats
import json
import os
from dp_insts import PEOPLE
from dp_office import PEOPLE as OFFICE_PEOPLE
# from statsmodels.formula.api import ols
# from statsmodels.stats.anova import anova_lm

TXWJ_FILENAME = "score-txwj.txt"

task_seq = [[3, 13, 12, 9, 10, 20, 8, 7, 11, 18, 6, 19, 2, 15, 4, 14, 22, 1, 21, 17, 5, 16, 23, 24],
            [2, 4, 8, 23, 3, 14, 11, 15, 5, 17, 16, 18, 20,
                10, 1, 12, 21, 19, 7, 9, 24, 6, 13, 22],
            [20, 10, 12, 14, 18, 7, 9, 15, 2, 19, 1, 16,
                6, 4, 22, 17, 24, 13, 23, 3, 11, 21, 8, 5],
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

img_score = []
for i in range(4):
    img_score.append([])
    for _ in range(48):
        img_score[i].append([])


def getScore():
    with open(TXWJ_FILENAME, "r") as f:
        data = f.read().split("\n")
        for line in data:
            line = line.split("\t")
            seq = [0] * 24  # 第 i 位表示第 i 张图的名次
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
                    img_score[task_id][raw_id(
                        seq.index(i + 1) + 1, task_id) - 1].append(int(line[id]))
    return cnet_score, office_score, img_score


def calSortedAveScore():
    # img_score.sort(key=)
    def compFirst(a):
        return a[0]
    for i in img_score:
        i.sort(key=compFirst)
    # for i in img_score:
    #     print(i, len(i))


def getAveScore():
    getScoreFromDebugout()
    for i in img_score:
        for j in range(len(i)):
            i[j] = (np.mean(i[j]), j)
    print(img_score)
    return img_score


def getScoreFromDebugout():
    stu_ids = os.listdir("debugout/data")
    if ".DS_Store" in stu_ids:
        stu_ids.remove(".DS_Store")
    # sum_v = 0
    for d in stu_ids:
        with open(f"debugout/data/{d}/{d}.txt", "r") as f:
            data = json.loads(f.read())
            for k, v in data.items():
                k = k.split("/")[-1].split("-")
                if k[1] == "office":
                    office_score[int(k[2][0])-1].append(v)
                elif k[1] == "cnet":
                    cnet_score[int(k[2][0])-1].append(v)
                else:
                    print(k)
                drawer_name = k[0]
                sys_type = 0 if k[1] == "cnet" else 1
                drawer_id = PEOPLE.index(drawer_name) if sys_type == 0 else OFFICE_PEOPLE.index(drawer_name)
                img_type = int(k[2][0])
                # if drawer_name == "wzz" and sys_type == 1:
                #     sum_v += v
                img_score[img_type - 1][drawer_id + sys_type * len(PEOPLE)].append(v)
    return cnet_score, office_score, img_score
    # print(sum_v)


if __name__ == "__main__":
    getScoreFromDebugout()
    # getScore()
    for i in range(4):
        print("task {} cnet average score: {} ppt average score: {}".format(
            i + 1, np.mean(cnet_score[i]), np.mean(office_score[i])))
        # print("wilcoxon: {}".format(scipy.stats.wilcoxon(cnet_score[i], office_score[i])))
        # print("task {} cnet average rank: {} ppt average rank: {}".format(i + 1, np.mean(cnet_seq[i]), np.mean(office_seq[i])))
        # print("wilcoxon: {}".format(scipy.stats.wilcoxon(cnet_seq[i], office_seq[i])))
        print("anova: {}".format(scipy.stats.f_oneway(
            cnet_score[i], office_score[i])))
    print(f"sgdiag mean: {np.mean(np.array(cnet_score).reshape(-1))} std: {np.std(np.array(cnet_score).reshape(-1))}")
    print(f"office mean: {np.mean(np.array(office_score).reshape(-1))} std: {np.std(np.array(office_score).reshape(-1))}")
    for i in img_score:
        for j in range(len(i)):
            i[j] = (np.mean(i[j]), j)
    # calSortedAveScore()
    cnet_score_0 = [np.mean([img_score[j][i][0] for j in range(4)]) for i in range(12)]
    cnet_score_1 = [np.mean([img_score[j][i][0] for j in range(4)]) for i in range(12, 24)]
    office_score_0 = [np.mean([img_score[j][i][0] for j in range(4)]) for i in range(24, 36)]
    office_score_1 = [np.mean([img_score[j][i][0] for j in range(4)]) for i in range(36, 48)]
    print(f"mean: {np.mean(cnet_score_0)} {np.mean(cnet_score_1)} {np.mean(office_score_0)} {np.mean(office_score_1)}")
    print(f"std: {np.std(cnet_score_0)} {np.std(cnet_score_1)} {np.std(office_score_0)} {np.std(office_score_1)}")
    print(f"anova-0-1 {scipy.stats.f_oneway(cnet_score_0, cnet_score_1)}")
    print(f"anova-0-2 {scipy.stats.f_oneway(cnet_score_0, office_score_0)}")
    print(f"anova-0-3 {scipy.stats.f_oneway(cnet_score_0, office_score_1)}")
    print(f"anova-1-2 {scipy.stats.f_oneway(cnet_score_1, office_score_0)}")
    print(f"anova-1-3 {scipy.stats.f_oneway(cnet_score_1, office_score_1)}")
    print(f"anova-2-3 {scipy.stats.f_oneway(office_score_0, office_score_1)}")