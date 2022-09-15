import numpy as np

OFFICE_FILENAME = "office-time.txt"
# PEOPLE = "jjx lbc lgz xtx ywt zhp zxy zyw lyf dyc wzz hmf"
PEOPLE = "dyc hmf jjx lbc lgz lyf wzz xtx ywt zhp zxy zyw"

def time2second(t: str):
    '''
    for example 01:01 to 61
    '''
    t = t.replace(" ", "")
    t = t.split(":")
    return int(t[0]) * 60 + int(t[1])

def cal_all_time():
    '''
    return [[a, b, c, ...] * task_num]
    '''
    all_time = []
    with open(OFFICE_FILENAME, "r", encoding="utf-8-sig") as f:
        data = f.read().split("\n")
        for single_data in data:
            single_person_time = []
            t_array = single_data.split("|")[2:-1]
            for i in range(4):
                single_person_time.append(time2second(t_array[2 * i + 1]) - time2second(t_array[2 * i]))
            # for t in t_array:
            #     t = t.replace(" ", "")
            #     t = t.split(":")
            #     print(t)
            #     single_person_time.append(int(t[0]) * 60 + int(t[1]))
            all_time.append(single_person_time)
    return np.array(all_time).T

def cal_ave_time():
    all_time = cal_all_time()
    ave_time = [np.mean(np.array(all_time)[:, j]) for j in range(4)]
    return ave_time

if __name__ == "__main__":
    print(cal_all_time())
    print(cal_ave_time())