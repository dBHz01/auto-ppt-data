from base64 import decode
import json
import os
from os import listdir
import numpy as np
import matplotlib.pyplot as plt
from utils import find_indices, remove_all

plt.rcParams['font.sans-serif'] = 'simhei'

# PEOPLE = "azd crj cyy djy frw lly lzj stp tty xq ylc ytj zyx".split(" ")
PEOPLE = "azd crj cyy djy frw lly lzj tty xq ylc ytj zyx lyf zyw zxy lgz lbc hmf zhp ywt dyc jjx xtx wzz".split(" ")
PEOPLE_NAIVE = "cyx dhc fsy pyk sms tyq yxy znn".split(" ")
# SEQUENCE = [[3, 1, 4, 2], # 4312
#             [3, 4, 2, 1], # 3142
#             [1, 2, 4, 3], # 3421
#             [4, 2, 3, 1], # 1243
#             [1, 4, 2, 3], # 4231
#             # [3, 1, 2, 4],
#             [2, 3, 4, 1], # 1423
#             [1, 3, 4, 2], # 1234
#             [1, 2, 3, 4], # 4213
#             [1, 2, 3, 4], # 1234
#             [4, 2, 1, 3], # 4123
#             [4, 3, 1, 2], # 2341
#             [4, 1, 2, 3]  # 1342
#             ]
SEQUENCE = [[4, 3, 1, 2],
            [3, 1, 4, 2],
            [3, 4, 2, 1],
            [1, 2, 4, 3],
            [4, 2, 3, 1],
            [1, 4, 2, 3],
            [1, 2, 3, 4],
            [4, 2, 1, 3],
            [1, 2, 3, 4],
            [4, 1, 2, 3],
            [2, 3, 4, 1],
            [1, 3, 4, 2],

            [1, 4, 3, 2],
            [3, 4, 2, 1],
            [2, 4, 1, 3],
            [2, 1, 3, 4],
            [2, 1, 4, 3],
            [1, 4, 3, 2],
            [4, 2, 1, 3],
            [1, 3, 4, 2],
            [3, 1, 2, 4],
            [1, 2, 4, 3],
            [4, 2, 1, 3],
            [1, 4, 3, 2],
            ]
instructions = "开始语音输入 \
                结束语音输入 \
                识别结束 \
                输入框文本变化 \
                系统接收指令输入 \
                解析结束 \
                指令执行结束 \
                选择候选 \
                选中图表元素 \
                取消元素选择 \
                结束对元素的拖拽 \
                切换功能栏TAG_DISP_SET_GLOBAL \
                切换功能栏TAG_DISP_MOD \
                切换功能栏TAG_DISP_CDT \
                切换功能栏TAG_DISP_SET \
                切换功能栏TAG_DISP_INS \
                清空路径 \
                撤销 \
                重做 \
                选择元素标签 \
                取消选择元素标签 \
                指令展示-修改元素 \
                增加亮度 \
                选择颜色 \
                修改箭头显示情况 \
                删除箭头 \
                虚线设置 \
                修改元素类型 \
                调节元素大小 \
                应用推荐修改 \
                显示关系信息 \
                ".split(" ")
while "" in instructions:
    instructions.remove("")


def inst_time_ave():
    '''
    每条指令平均时间
    '''
    log_time_all = [] # [[time0, time1] * len]
    log_time_ave = [] # [[ave_time, num] * len]
    all_time = 0
    for i in range(len(instructions)):
        log_time_all.append([])
    for people in PEOPLE:
        for dir in listdir(people):
            pathname = os.path.join(people, dir, "log.json")
            with open(pathname, "r", encoding="utf-8") as f:
                try:
                    data = json.loads(f.read())
                    for i, single_log in enumerate(data):
                        if single_log["msg"] in instructions:
                            if i > 0:
                                log_time_all[instructions.index(single_log["msg"])].append(data[i]["ts"] - data[i - 1]["ts"])
                        else:
                            print(single_log["msg"])
                except Exception:
                    print(pathname)
                # print(json.loads(f.read()))
    for inst_time in log_time_all:
        all_time += np.sum(inst_time)
    for i, inst_time in enumerate(log_time_all):
        log_time_ave.append([np.mean(inst_time), len(inst_time), np.sum(inst_time), np.sum(inst_time) / all_time, np.max(inst_time), instructions[i]])
    print(log_time_ave)
    percentage_data = [i[3] for i in log_time_ave]
    plt.pie(percentage_data, labels=instructions, autopct='%.2f%%')
    plt.show()

def task_time_ave():
    '''
    每个任务的平均时长
    '''
    time_with_label = []
    time_with_label_ave = []
    for i in range(4):
        time_with_label.append([])
    for people in PEOPLE:
        for dir in listdir(people):
            pathname = os.path.join(people, dir, "log.json")
            with open(pathname, "r", encoding="utf-8") as f:
                try:
                    data = json.loads(f.read())
                    label = int(dir.split("-")[1]) - 1
                    time_with_label[label].append(data[-1]["ts"] - data[0]["ts"])
                except Exception:
                    print(pathname)
    # print(time_with_label)
    for i in time_with_label:
        time_with_label_ave.append(np.mean(i))
    print(time_with_label_ave)

def inst_num_ave():
    '''
    指令条数统计
    return [voice & touch, voice & !touch, !voice & touch, !voice & !touch]
    '''
    round_type_num = [0, 0, 0, 0]
    round_num = 0
    total_time = 0
    reuse_num = 0
    for people in PEOPLE:
        for dir in listdir(people):
            pathname = os.path.join(people, dir, "log.json")
            inst_rounds = [] # all rounds
            cur_round = []
            wait_for_choosing = False
            with open(pathname, "r", encoding="utf-8") as f:
                try:
                    data = json.loads(f.read())
                    for i, single_log in enumerate(data):
                        if (instructions.index(single_log["msg"]) == 7):
                            if (wait_for_choosing):
                                inst_rounds[-1].append([single_log["msg"], data[i]["ts"]])
                                continue
                        else:
                            wait_for_choosing = False
                        cur_round.append([single_log["msg"], data[i]["ts"]])
                        if (instructions.index(single_log["msg"]) == 6):
                            wait_for_choosing = True
                            inst_rounds.append(cur_round)
                            # for i in cur_round:
                            #     print(i[0], i[1])
                            # input()
                            cur_round = []
                    
                except Exception:
                    print(pathname)
            # print(pathname, inst_rounds)
            # input()

            round_num += len(inst_rounds)
            total_time += inst_rounds[-1][-1][1] - inst_rounds[0][0][1]

            for r in inst_rounds:
                log_texts = [i[0] for i in r]
                log_timestamps = [i[1] for i in r]

                if instructions[8] in log_texts:
                    round_type_num[0] += 1
                else:
                    round_type_num[1] += 1
                
                all_drag_pos = find_indices(log_texts, instructions[10])
                round_type_num[2] += len(all_drag_pos)

                all_gui_pos_0 = find_indices(log_texts, instructions[-3])
                all_gui_pos_1 = find_indices(log_texts, instructions[-2])
                round_type_num[3] += len(all_gui_pos_0)
                round_type_num[3] += len(all_gui_pos_1)

                all_input_0 = find_indices(log_texts, "开始语音输入")
                all_input_1 = find_indices(log_texts, "输入框文本变化") 
                if not(len(all_input_0) > 0 or len(all_input_1) > 0):
                    reuse_num += 1
    print(round_type_num, "sum: ", np.sum(round_type_num))
    print(f"reuse num: {reuse_num}")
    return round_type_num

def pos_related_num():
    '''
    位置相关指令统计
    return num
    '''
    ret_num = 0
    all_analysis_insts = []
    for people in PEOPLE:
        for dir in listdir(people):
            pathname = os.path.join(people, dir, "log.json")
            with open(pathname, "r", encoding="utf-8") as f:
                try:
                    data = json.loads(f.read())
                    for i, single_log in enumerate(data):
                        if (instructions.index(single_log["msg"]) == 5):
                            all_analysis_insts.append(single_log)
                        
                except Exception:
                    print(pathname)
    for i in all_analysis_insts:
        try:
            list(i.keys()).index("posRelated")
            if (i["posRelated"] == True):
                ret_num += 1
        except Exception:
            continue
    print(ret_num)
    return ret_num

def candidate_ave_index():
    '''
    平均候选顺位
    '''
    candidates = []
    for people in PEOPLE:
        for dir in listdir(people):
            pathname = os.path.join(people, dir, "log.json")
            choosing = False
            cur_candidate = None
            with open(pathname, "r", encoding="utf-8") as f:
                try:
                    data = json.loads(f.read())
                    for i, single_log in enumerate(data):
                        if (instructions.index(single_log["msg"]) == 7):
                            choosing = True
                            cur_candidate = single_log["idx"]
                        else:
                            if choosing:
                                choosing = False
                                candidates.append(cur_candidate)
                                cur_candidate = None
                        
                except Exception:
                    print(pathname)
    print(remove_all(candidates, 0))
    candidates = np.array(candidates) + 1
    print(len(remove_all(candidates, 0)))
    # print(list(candidates).count(2))
    # print(list(candidates).count(3))
    # print(list(candidates).count(4))
    # print(list(candidates).count(5))
    print("mean: ", np.mean(remove_all(candidates, 0)))
    print("median: ",np.median(remove_all(candidates, 0)))
    print("std: ", np.std(remove_all(candidates, 0)))
    return np.mean(remove_all(candidates, 0)), [list(candidates).count(i) for i in range(2, 6)]

def inst_classify():
    all_labels = [0, 0, 0, 0] # 执行当前指令 需要补充后执行 需要补充后执行 需要补充后联动调整
    for people in PEOPLE:
        for dir in listdir(people):
            pathname = os.path.join(people, dir, "log.json")
            with open(pathname, "r", encoding="utf-8") as f:
                try:
                    last_instruction = ""
                    data = json.loads(f.read())
                    for i, single_log in enumerate(data):
                        if (instructions.index(single_log["msg"]) == instructions.index("系统接收指令输入")):
                            last_instruction = single_log["uttr"]
                        elif (instructions.index(single_log["msg"]) == instructions.index("指令执行结束")):
                            if "建" in last_instruction:
                                all_labels[1] += 1
                            elif "改" in last_instruction:
                                if "文字" in last_instruction or "文本" in last_instruction:
                                    all_labels[0] += 1
                                elif "色" in last_instruction or "大小" in last_instruction or "宽度" in last_instruction or "高度" in last_instruction:
                                    all_labels[1] += 1
                                elif "箭头" in last_instruction or "直线" in last_instruction:
                                    all_labels[0] += 1
                                elif "距离" in last_instruction or "横坐标" in last_instruction or "纵坐标" in last_instruction:
                                    all_labels[2] += 1
                                else:
                                    print(last_instruction)
                            elif "删" in last_instruction:
                                all_labels[0] += 1
                            elif "复制" in last_instruction:
                                all_labels[2] += 1
                            elif "移动" in last_instruction:
                                if "保持" in last_instruction:
                                    all_labels[1] += 1
                                elif "中点" in last_instruction:
                                    all_labels[2] += 1
                                elif "这里" in last_instruction:
                                    all_labels[3] += 1
                                elif "横坐标" in last_instruction or "纵坐标" in last_instruction:
                                    all_labels[2] += 1
                                elif "右" in last_instruction:
                                    all_labels[3] += 1
                                else:
                                    print(last_instruction)
                            else:
                                print(last_instruction)

                except Exception:
                    print(pathname)
    all_labels[2] += 258
    print(all_labels, f"sum: {np.sum(all_labels)}")

if __name__ == "__main__":
    inst_num_ave()
    # pos_related_num()
    # candidate_ave_index()
    inst_classify()