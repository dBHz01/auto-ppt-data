import numpy as np
import scipy.stats

SCORE_CNET_FILENAME = "score-cnet.txt"
SCORE_OFFICE_FILENAME = "score-office.txt"

def do_wilcoxon():
    score_cnet = []
    score_office = []
    with open(SCORE_CNET_FILENAME, "r", encoding="utf-8-sig") as f:
        data = f.read().split("\n")
        for single_data in data:
            single_score = []
            s_array = single_data.split("|")[2:-1]
            for i in s_array:
                single_score.append(int(i.replace(" ", "")))
            score_cnet.append(single_score)
    with open(SCORE_OFFICE_FILENAME, "r", encoding="utf-8-sig") as f:
        data = f.read().split("\n")
        for single_data in data:
            single_score = []
            s_array = single_data.split("|")[2:-1]
            for i in s_array:
                single_score.append(int(i.replace(" ", "")))
            score_office.append(single_score)
    score_cnet = np.array(score_cnet).T
    print(f"raw score-cnet {[np.mean(score_cnet[i]) for i in range(6)]}")
    score_cnet = np.delete(score_cnet, [1,2], axis=0)
    score_office = np.array(score_office).T
    print(f"score-cnet: {[np.mean(score_cnet[i]) for i in range(4)]}\nscore-office: {[np.mean(score_office[i]) for i in range(4)]}")
    print(scipy.stats.wilcoxon(score_cnet[0], score_office[0]))
    print(scipy.stats.wilcoxon(score_cnet[1], score_office[1]))
    print(scipy.stats.wilcoxon(score_cnet[2], score_office[2]))
    print(scipy.stats.wilcoxon(score_cnet[3], score_office[3]))


if __name__ == "__main__":
    do_wilcoxon()
