import json
import os
from os import listdir
from dp_insts import PEOPLE, PEOPLE_NAIVE, SEQUENCE, instructions
import matplotlib.pyplot as plt
import numpy as np
from utils import find_indices

def show_simple():
    '''
    查看每次的指令及执行时间
    '''
    for people in PEOPLE_NAIVE:
        for dir in listdir(os.path.join("naive", people)):
            pathname = os.path.join("naive", people, dir, "log.json")
            all = 0
            with open(pathname, "r", encoding="utf-8") as f:
                try:
                    data = json.loads(f.read())
                    for i, single_log in enumerate(data):
                        instructions.index(single_log["msg"])
                        if i + 1 < len(data):
                            print(single_log["msg"], data[i + 1]["ts"] - data[i]["ts"])
                            all += data[i + 1]["ts"] - data[i]["ts"]
                except Exception:
                    print("wrong")
                    print(single_log["msg"])
                    input()
            print(pathname, all)
            input()

def show_single(id: int):
    '''
    查看任意id的后续指令及时间
    '''
    for people in PEOPLE:
        for dir in listdir(people):
            pathname = os.path.join(people, dir, "log.json")
            all = 0
            with open(pathname, "r", encoding="utf-8") as f:
                try:
                    data = json.loads(f.read())
                    for i, single_log in enumerate(data):
                        # if i + 1 < len(data):
                        #     # print(single_log["msg"], data[i + 1]["ts"] - data[i]["ts"])
                        #     if instructions.index(single_log["msg"]) == id:
                        #         print(single_log["msg"], data[i + 1]["ts"] - data[i]["ts"], data[i+1]["msg"])
                        #     all += data[i + 1]["ts"] - data[i]["ts"]
                        if instructions.index(single_log["msg"]) == id:
                            print(single_log["msg"], i)
                except Exception:
                    print(pathname, "error")
            print(pathname, all)
            input()

def show_single_round():
    '''
    从xx开始至执行结束 or 候选结果切换的一整轮
    '''
    for people in PEOPLE_NAIVE:
        for dir in listdir(os.path.join("naive", people)):
            pathname = os.path.join("naive", people, dir, "log.json")
            all = 0
            inst_rounds = [] # all rounds
            cur_round = []
            wait_for_choosing = False
            with open(pathname, "r", encoding="utf-8") as f:
                try:
                    data = json.loads(f.read())
                    for i, single_log in enumerate(data):
                        if i + 1 < len(data):
                            if (instructions.index(single_log["msg"]) == 7):
                                if (wait_for_choosing):
                                    inst_rounds[-1].append([[single_log["msg"], data[i + 1]["ts"] - data[i]["ts"], data[i+1]["msg"]]])
                                    continue
                            else:
                                wait_for_choosing = False
                            cur_round.append([single_log["msg"], data[i + 1]["ts"] - data[i]["ts"], data[i+1]["msg"]])
                            if (instructions.index(single_log["msg"]) == 6):
                                wait_for_choosing = True
                                inst_rounds.append(cur_round)
                                for i in cur_round:
                                    print(i[0], i[1])
                                input()
                                cur_round = []
                    
                except Exception:
                    print(pathname)
            print(pathname, inst_rounds)
            input()

def show_certain_round(id: int):
    '''
    包含 id 指令的 round
    '''
    for people in PEOPLE:
        for dir in listdir(people):
            pathname = os.path.join(people, dir, "log.json")
            all = 0
            inst_rounds = [] # all rounds
            cur_round = []
            wait_for_choosing = False
            with open(pathname, "r", encoding="utf-8") as f:
                try:
                    data = json.loads(f.read())
                    for i, single_log in enumerate(data):
                        if i + 1 < len(data):
                            if (instructions.index(single_log["msg"]) == 7):
                                if (wait_for_choosing):
                                    inst_rounds[-1].append([[single_log["msg"], data[i + 1]["ts"] - data[i]["ts"], data[i+1]["msg"]]])
                                    continue
                            else:
                                wait_for_choosing = False
                            cur_round.append([single_log["msg"], data[i + 1]["ts"] - data[i]["ts"], data[i+1]["msg"]])
                            if (instructions.index(single_log["msg"]) == 6):
                                wait_for_choosing = True
                                inst_rounds.append(cur_round)
                                if instructions[id] in [i[0] for i in cur_round]:
                                    for i in cur_round:
                                        print(i[0], i[1])
                                    input()
                                cur_round = []
                    
                except Exception:
                    print(pathname)
            print(pathname)
            input()

def show_certain_person(person, number):
    '''
    从xx开始至执行结束 or 候选结果切换的一整轮
    '''
    for dir in listdir(person):
        if dir.split("-")[1] == str(number):
            pathname = os.path.join(person, dir, "log.json")
            all = 0
            inst_rounds = [] # all rounds
            cur_round = []
            wait_for_choosing = False
            with open(pathname, "r", encoding="utf-8") as f:
                try:
                    data = json.loads(f.read())
                    for i, single_log in enumerate(data):
                        if i + 1 < len(data):
                            if (instructions.index(single_log["msg"]) == 7):
                                if (wait_for_choosing):
                                    inst_rounds[-1].append([[single_log["msg"], data[i + 1]["ts"] - data[i]["ts"], data[i+1]["msg"]]])
                                    continue
                            else:
                                wait_for_choosing = False
                            cur_round.append([single_log["msg"], data[i + 1]["ts"] - data[i]["ts"], data[i+1]["msg"]])
                            if (instructions.index(single_log["msg"]) == 6):
                                wait_for_choosing = True
                                inst_rounds.append(cur_round)
                                for i in cur_round:
                                    print(i[0], i[1])
                                input()
                                cur_round = []
                    
                except Exception:
                    print(single_log)
                    print(pathname)
            print(pathname, inst_rounds)
            input()

def check_input_text():
    '''
    查看是否加上了 '输入文本框变化' 的 log
    '''
    for people in PEOPLE:
        have_input_text_log = False
        for dir in listdir(people):
            pathname = os.path.join(people, dir, "log.json")
            with open(pathname, "r", encoding="utf-8") as f:
                try:
                    data = json.loads(f.read())
                    for i, single_log in enumerate(data):
                        if (instructions.index(single_log["msg"]) == 3):
                            have_input_text_log = True
                            break
                    
                except Exception:
                    print(pathname)
            if (have_input_text_log):
                break
        print(people, have_input_text_log)

def cal_time():
    '''
    分成7段分别计算时间:
    0. 开始输入之前的时间（包括切换功能栏、撤销等）
    1. 第一次开始输入到最后一次开始输入之间的时间
    2. 最后一次开始输入到结束输入的时间，也就是 实际输入 的时间
    3. 最后一次结束输入到最后一次系统接收指令输入的时间（其中统计出文本修改的时间，也就是 调整指令 的时间）
    4. 最后一次系统接收指令输入到执行完毕的时间
    5. 执行完毕之后的若干次候选切换时间
    6. 切换候选之后到下一次开始之前的时间
    '''
    change_text_time = 0
    all_time_0 = [0, 0, 0, 0, 0, 0, 0] # last is gap time
    all_time_1 = [0, 0, 0, 0]
    all_time_2 = [0, 0, 0, 0]
    round_type_num = [0, 0, 0]
    round_num = 0
    total_time = 0
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
            last_end_time = 0
            cur_type = 0
            total_time += inst_rounds[-1][-1][1] - inst_rounds[0][0][1]

            for r in inst_rounds:
                all_time_0_bak = all_time_0.copy()
                all_time_1_bak = all_time_1.copy()
                all_time_2_bak = all_time_2.copy()
                log_texts = [i[0] for i in r]
                log_timestamps = [i[1] for i in r]
                

                # find all pos
                all_input_pos = find_indices(log_texts, instructions[0])
                all_end_input_pos = find_indices(log_texts, instructions[1])
                all_text_input_pos = find_indices(log_texts, instructions[3])
                all_get_inst_pos = find_indices(log_texts, instructions[4])
                all_change_chosen_pos = find_indices(log_texts, instructions[7])
                done_pos = log_texts.index(instructions[6])

                if instructions[0] in log_texts:
                    # 有语音
                    cur_type = 0
                    round_type_num[0] += 1
                    all_time_0[0] += log_timestamps[all_input_pos[0]] - log_timestamps[0]
                    if len(all_input_pos) > 1:
                        all_time_0[1] += log_timestamps[all_input_pos[-1]] - log_timestamps[all_input_pos[0]]
                    if instructions[1] in log_texts:
                        if all_end_input_pos[-1] - all_input_pos[-1] > 0:
                            all_time_0[2] += log_timestamps[all_end_input_pos[-1]] - log_timestamps[all_input_pos[-1]]
                        else:
                            print(pathname, "最后一次输入没有结束")
                            all_time_0 = all_time_0_bak.copy()
                            continue
                    else:
                        print(pathname, "没有结束语音输入")
                        all_time_0 = all_time_0_bak.copy()
                        continue
                    if instructions[4] in log_texts:
                        if all_get_inst_pos[-1] - all_end_input_pos[-1] > 0:
                            all_time_0[3] += log_timestamps[all_get_inst_pos[-1]] - log_timestamps[all_end_input_pos[-1]]
                        else:
                            print(pathname, "最后一次输入结束晚于指令输入")
                            all_time_0 = all_time_0_bak.copy()
                            continue
                    else:
                        print(pathname, "没有指令输入")
                        all_time_0 = all_time_0_bak.copy()
                        continue
                    all_time_0[4] += log_timestamps[done_pos] - log_timestamps[all_get_inst_pos[-1]]
                    if instructions[7] in log_texts:
                        if all_change_chosen_pos[-1] > done_pos:
                            all_time_0[5] += log_timestamps[all_change_chosen_pos[-1]] - log_timestamps[done_pos]
                        else:
                            print(pathname, "最后一次切换候选早于执行结束")
                            all_time_0 = all_time_0_bak.copy()
                            continue
                    if instructions[3] in log_texts:
                        for pos in all_text_input_pos:
                            if pos > 0:
                                change_text_time += log_timestamps[pos] - log_timestamps[pos - 1]
                elif instructions[3] in log_texts:
                    # 无语音，有文本变化
                    cur_type = 1
                    round_type_num[1] += 1 # 计数
                    all_end_input_pos = find_indices(log_texts, instructions[3])
                    if instructions[4] in log_texts:
                        all_time_1[0] += log_timestamps[all_get_inst_pos[-1]] - log_timestamps[0]
                        # if all_get_inst_pos[-1] - all_end_input_pos[-1] > 0:
                        #     all_time_1[0] += log_timestamps[all_get_inst_pos[-1]] - log_timestamps[all_end_input_pos[-1]]
                        # else:
                        #     print(pathname, "最后一次输入结束晚于指令输入")
                        #     all_time_1 = all_time_1_bak.copy()
                        #     continue
                    else:
                        print(pathname, "没有指令输入")
                        all_time_1 = all_time_1_bak.copy()
                        continue
                    all_time_1[1] += log_timestamps[done_pos] - log_timestamps[all_get_inst_pos[-1]]
                    if instructions[7] in log_texts:
                        if all_change_chosen_pos[-1] > done_pos:
                            all_time_1[2] += log_timestamps[all_change_chosen_pos[-1]] - log_timestamps[done_pos]
                        else:
                            print(pathname, "最后一次切换候选早于执行结束")
                            all_time_1 = all_time_1_bak.copy()
                            continue
                else:
                    # 无语音，无文本变化
                    cur_type = 2
                    round_type_num[2] += 1
                    if instructions[4] in log_texts:
                        all_time_2[0] += log_timestamps[all_get_inst_pos[-1]] - log_timestamps[0]
                    else:
                        print(pathname, "没有指令输入")
                        all_time_2 = all_time_2_bak.copy()
                        continue
                    all_time_2[1] += log_timestamps[done_pos] - log_timestamps[all_get_inst_pos[-1]]
                    if instructions[7] in log_texts:
                        if all_change_chosen_pos[-1] > done_pos:
                            all_time_2[2] += log_timestamps[all_change_chosen_pos[-1]] - log_timestamps[done_pos]
                        else:
                            print(pathname, "最后一次切换候选早于执行结束")
                            all_time_2 = all_time_2_bak.copy()
                            continue
                if last_end_time > 0:
                    if cur_type == 0:
                        all_time_0[6] += log_timestamps[0] - last_end_time
                    elif cur_type == 1:
                        all_time_1[3] += log_timestamps[0] - last_end_time
                    elif cur_type == 2:
                        all_time_2[3] += log_timestamps[0] - last_end_time
                
                if last_end_time == 0:
                    last_end_time = log_timestamps[-1]
                else:
                    # all_time_0[6] += log_timestamps[0] - last_end_time
                    # think_time += log_timestamps[0] - last_end_time
                    last_end_time = log_timestamps[-1]

            # input()
    # print(all_time_0, np.sum(all_time_0))
    # print(all_time_1, np.sum(all_time_1))
    # print(all_time_2, np.sum(all_time_2))
    # print(change_text_time)
    all_time = all_time_0
    all_time[2] += all_time_1[0]
    all_time[2] += all_time_2[0]
    all_time[4] += all_time_1[1]
    all_time[4] += all_time_2[1]
    all_time[5] += all_time_1[2]
    all_time[5] += all_time_2[2]
    all_time[6] += all_time_1[3]
    all_time[6] += all_time_2[3]
    # print("all time: ", all_time, np.sum(all_time))
    print(round_type_num)
    # print(round_num)
    # print(total_time)
    time_display = all_time
    time_display.insert(4, change_text_time)
    time_display[3] -= change_text_time
    time_display.append(total_time - np.sum(all_time))
    return time_display, round_num

def cal_time_separately():
    '''
    按照不同任务来计算时间
    分成7段分别计算时间:
    0. 开始输入之前的时间（包括切换功能栏、撤销等）
    1. 第一次开始输入到最后一次开始输入之间的时间
    2. 最后一次开始输入到结束输入的时间，也就是 实际输入 的时间
    3. 最后一次结束输入到最后一次系统接收指令输入的时间（其中统计出文本修改的时间，也就是 调整指令 的时间）
    4. 最后一次系统接收指令输入到执行完毕的时间
    5. 执行完毕之后的若干次候选切换时间
    6. 切换候选之后到下一次开始之前的时间
    '''
    change_text_time = [0, 0, 0, 0]
    all_time_0 = []
    for i in range(4):
        all_time_0.append([0, 0, 0, 0, 0, 0, 0]) # last is gap time
    round_type_num = [0, 0, 0]
    round_num = 0
    total_time = 0
    for people in PEOPLE:
        for dir in listdir(people):
            pathname = os.path.join(people, dir, "log.json")
            label = int(dir.split("-")[1]) - 1
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
            last_end_time = 0
            cur_type = 0
            total_time += inst_rounds[-1][-1][1] - inst_rounds[0][0][1]

            for r in inst_rounds:
                all_time_0_bak = [i.copy() for i in all_time_0]
                log_texts = [i[0] for i in r]
                log_timestamps = [i[1] for i in r]
                

                # find all pos
                all_input_pos = find_indices(log_texts, instructions[0])
                all_end_input_pos = find_indices(log_texts, instructions[1])
                all_text_input_pos = find_indices(log_texts, instructions[3])
                all_get_inst_pos = find_indices(log_texts, instructions[4])
                all_change_chosen_pos = find_indices(log_texts, instructions[7])
                done_pos = log_texts.index(instructions[6])

                if instructions[0] in log_texts:
                    # 有语音
                    cur_type = 0
                    round_type_num[0] += 1
                    all_time_0[label][0] += log_timestamps[all_input_pos[0]] - log_timestamps[0]
                    if len(all_input_pos) > 1:
                        all_time_0[label][1] += log_timestamps[all_input_pos[-1]] - log_timestamps[all_input_pos[0]]
                    if instructions[1] in log_texts:
                        if all_end_input_pos[-1] - all_input_pos[-1] > 0:
                            all_time_0[label][2] += log_timestamps[all_end_input_pos[-1]] - log_timestamps[all_input_pos[-1]]
                        else:
                            print(pathname, "最后一次输入没有结束")
                            all_time_0 = all_time_0_bak.copy()
                            continue
                    else:
                        print(pathname, "没有结束语音输入")
                        all_time_0 = all_time_0_bak.copy()
                        continue
                    if instructions[4] in log_texts:
                        if all_get_inst_pos[-1] - all_end_input_pos[-1] > 0:
                            all_time_0[label][3] += log_timestamps[all_get_inst_pos[-1]] - log_timestamps[all_end_input_pos[-1]]
                        else:
                            print(pathname, "最后一次输入结束晚于指令输入")
                            all_time_0 = all_time_0_bak.copy()
                            continue
                    else:
                        print(pathname, "没有指令输入")
                        all_time_0 = all_time_0_bak.copy()
                        continue
                    all_time_0[label][4] += log_timestamps[done_pos] - log_timestamps[all_get_inst_pos[-1]]
                    if instructions[7] in log_texts:
                        if all_change_chosen_pos[-1] > done_pos:
                            all_time_0[label][5] += log_timestamps[all_change_chosen_pos[-1]] - log_timestamps[done_pos]
                        else:
                            print(pathname, "最后一次切换候选早于执行结束")
                            all_time_0 = all_time_0_bak.copy()
                            continue
                    if instructions[3] in log_texts:
                        for pos in all_text_input_pos:
                            if pos > 0:
                                change_text_time[label] += log_timestamps[pos] - log_timestamps[pos - 1]
                elif instructions[3] in log_texts:
                    # 无语音，有文本变化
                    cur_type = 1
                    round_type_num[1] += 1 # 计数
                    all_end_input_pos = find_indices(log_texts, instructions[3])
                    if instructions[4] in log_texts:
                        all_time_0[label][2] += log_timestamps[all_get_inst_pos[-1]] - log_timestamps[0]
                        # if all_get_inst_pos[-1] - all_end_input_pos[-1] > 0:
                        #     all_time_0[2] += log_timestamps[all_get_inst_pos[-1]] - log_timestamps[all_end_input_pos[-1]]
                        # else:
                        #     print(pathname, "最后一次输入结束晚于指令输入")
                        #     all_time_1 = all_time_1_bak.copy()
                        #     continue
                    else:
                        print(pathname, "没有指令输入")
                        all_time_0 = all_time_0_bak.copy()
                        continue
                    all_time_0[label][4] += log_timestamps[done_pos] - log_timestamps[all_get_inst_pos[-1]]
                    if instructions[7] in log_texts:
                        if all_change_chosen_pos[-1] > done_pos:
                            all_time_0[label][5] += log_timestamps[all_change_chosen_pos[-1]] - log_timestamps[done_pos]
                        else:
                            print(pathname, "最后一次切换候选早于执行结束")
                            all_time_0 = all_time_0_bak.copy()
                            continue
                else:
                    # 无语音，无文本变化
                    cur_type = 2
                    round_type_num[2] += 1
                    if instructions[4] in log_texts:
                        all_time_0[label][2] += log_timestamps[all_get_inst_pos[-1]] - log_timestamps[0]
                    else:
                        print(pathname, "没有指令输入")
                        all_time_0 = all_time_0_bak.copy()
                        continue
                    all_time_0[label][4] += log_timestamps[done_pos] - log_timestamps[all_get_inst_pos[-1]]
                    if instructions[7] in log_texts:
                        if all_change_chosen_pos[-1] > done_pos:
                            all_time_0[label][5] += log_timestamps[all_change_chosen_pos[-1]] - log_timestamps[done_pos]
                        else:
                            print(pathname, "最后一次切换候选早于执行结束")
                            all_time_0 = all_time_0_bak.copy()
                            continue
                if last_end_time > 0:
                    if cur_type == 0:
                        all_time_0[label][6] += log_timestamps[0] - last_end_time
                    elif cur_type == 1:
                        all_time_0[label][6] += log_timestamps[0] - last_end_time
                    elif cur_type == 2:
                        all_time_0[label][6] += log_timestamps[0] - last_end_time
                
                if last_end_time == 0:
                    last_end_time = log_timestamps[-1]
                else:
                    # all_time_0[6] += log_timestamps[0] - last_end_time
                    # think_time += log_timestamps[0] - last_end_time
                    last_end_time = log_timestamps[-1]

            # input()
    separate_time = []
    for label in range(4):
        # print(all_time_0[label], np.sum(all_time_0[label]))
        # print(change_text_time)
        # print("all time: ", all_time_0[label], np.sum(all_time_0[label]))
        # print(round_type_num)
        # print(round_num)
        # print(total_time)
        time_display = all_time_0[label]
        time_display.insert(4, change_text_time[label])
        time_display[3] -= change_text_time[label]
        print("all time: ", time_display, np.sum(time_display))
        separate_time.append(time_display)
        # time_display.append(total_time - np.sum(all_time_0[0]))
        time_display_text = ['开始输入之前各类指令时间', '第一次至最后一次开始输入(可删除)', '实际输入时间', '结束输入后的调整时间', '结束输入后修改文本时间(可删除)', '系统运行时间', '切换候选时间', '两轮之间思考时间']
        # plt.pie(time_display, labels=time_display_text, autopct='%.2f%%')
        # plt.show()
    # print([np.sum(i) / 1000 / len(PEOPLE) for i in separate_time])
    for t in separate_time:
        t[1] = 0
        t[4] = 0
    return [np.sum(i) / 1000 / len(PEOPLE) for i in separate_time]

def cal_time_separately_single(all_people=PEOPLE):
    '''
    按照不同任务来计算时间, 但不分段, 除去该删除的时间不算
    0. 开始输入之前的时间（包括切换功能栏、撤销等）
    1. 第一次开始输入到最后一次开始输入之间的时间 (可删除)
    2. 最后一次开始输入到结束输入的时间，也就是 实际输入 的时间
    3. 最后一次结束输入到最后一次系统接收指令输入的时间（其中统计出文本修改的时间，也就是 调整指令 的时间 (可删除) ）
    4. 最后一次系统接收指令输入到执行完毕的时间
    5. 执行完毕之后的若干次候选切换时间
    6. 切换候选之后到下一次开始之前的时间
    '''
    all_time_0 = []
    for i in range(4):
        all_time_0.append([])
    round_type_num = [0, 0, 0]
    round_num = 0
    total_time = 0
    for people in all_people:
        for dir in listdir(people):
            pathname = os.path.join(people, dir, "log.json")
            label = int(dir.split("-")[1]) - 1
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
            last_end_time = 0
            cur_type = 0
            total_time += inst_rounds[-1][-1][1] - inst_rounds[0][0][1]
            cur_time = 0
            change_text_time = 0

            for r in inst_rounds:
                all_time_0_bak = [i.copy() for i in all_time_0]
                log_texts = [i[0] for i in r]
                log_timestamps = [i[1] for i in r]
                

                # find all pos
                all_input_pos = find_indices(log_texts, instructions[0])
                all_end_input_pos = find_indices(log_texts, instructions[1])
                all_text_input_pos = find_indices(log_texts, instructions[3])
                all_get_inst_pos = find_indices(log_texts, instructions[4])
                all_change_chosen_pos = find_indices(log_texts, instructions[7])
                done_pos = log_texts.index(instructions[6])

                if instructions[0] in log_texts:
                    # 有语音
                    cur_type = 0
                    round_type_num[0] += 1
                    cur_time += log_timestamps[all_input_pos[0]] - log_timestamps[0]
                    # if len(all_input_pos) > 1:
                    #     cur_time += log_timestamps[all_input_pos[-1]] - log_timestamps[all_input_pos[0]]
                    if instructions[1] in log_texts:
                        if all_end_input_pos[-1] - all_input_pos[-1] > 0:
                            cur_time += log_timestamps[all_end_input_pos[-1]] - log_timestamps[all_input_pos[-1]]
                        else:
                            print(pathname, "最后一次输入没有结束")
                            all_time_0 = all_time_0_bak.copy()
                            continue
                    else:
                        print(pathname, "没有结束语音输入")
                        all_time_0 = all_time_0_bak.copy()
                        continue
                    if instructions[4] in log_texts:
                        if all_get_inst_pos[-1] - all_end_input_pos[-1] > 0:
                            cur_time += log_timestamps[all_get_inst_pos[-1]] - log_timestamps[all_end_input_pos[-1]]
                        else:
                            print(pathname, "最后一次输入结束晚于指令输入")
                            all_time_0 = all_time_0_bak.copy()
                            continue
                    else:
                        print(pathname, "没有指令输入")
                        all_time_0 = all_time_0_bak.copy()
                        continue
                    cur_time += log_timestamps[done_pos] - log_timestamps[all_get_inst_pos[-1]]
                    if instructions[7] in log_texts:
                        if all_change_chosen_pos[-1] > done_pos:
                            cur_time += log_timestamps[all_change_chosen_pos[-1]] - log_timestamps[done_pos]
                        else:
                            print(pathname, "最后一次切换候选早于执行结束")
                            all_time_0 = all_time_0_bak.copy()
                            continue
                    if instructions[3] in log_texts:
                        for pos in all_text_input_pos:
                            if pos > 0:
                                change_text_time += log_timestamps[pos] - log_timestamps[pos - 1]
                elif instructions[3] in log_texts:
                    # 无语音，有文本变化
                    cur_type = 1
                    round_type_num[1] += 1 # 计数
                    all_end_input_pos = find_indices(log_texts, instructions[3])
                    if instructions[4] in log_texts:
                        cur_time += log_timestamps[all_get_inst_pos[-1]] - log_timestamps[0]
                        # if all_get_inst_pos[-1] - all_end_input_pos[-1] > 0:
                        #     all_time_0[2] += log_timestamps[all_get_inst_pos[-1]] - log_timestamps[all_end_input_pos[-1]]
                        # else:
                        #     print(pathname, "最后一次输入结束晚于指令输入")
                        #     all_time_1 = all_time_1_bak.copy()
                        #     continue
                    else:
                        print(pathname, "没有指令输入")
                        all_time_0 = all_time_0_bak.copy()
                        continue
                    cur_time += log_timestamps[done_pos] - log_timestamps[all_get_inst_pos[-1]]
                    if instructions[7] in log_texts:
                        if all_change_chosen_pos[-1] > done_pos:
                            cur_time += log_timestamps[all_change_chosen_pos[-1]] - log_timestamps[done_pos]
                        else:
                            print(pathname, "最后一次切换候选早于执行结束")
                            all_time_0 = all_time_0_bak.copy()
                            continue
                else:
                    # 无语音，无文本变化
                    cur_type = 2
                    round_type_num[2] += 1
                    if instructions[4] in log_texts:
                        cur_time += log_timestamps[all_get_inst_pos[-1]] - log_timestamps[0]
                    else:
                        print(pathname, "没有指令输入")
                        all_time_0 = all_time_0_bak.copy()
                        continue
                    cur_time += log_timestamps[done_pos] - log_timestamps[all_get_inst_pos[-1]]
                    if instructions[7] in log_texts:
                        if all_change_chosen_pos[-1] > done_pos:
                            cur_time += log_timestamps[all_change_chosen_pos[-1]] - log_timestamps[done_pos]
                        else:
                            print(pathname, "最后一次切换候选早于执行结束")
                            all_time_0 = all_time_0_bak.copy()
                            continue
                if last_end_time > 0:
                    if cur_type == 0:
                        cur_time += log_timestamps[0] - last_end_time
                    elif cur_type == 1:
                        cur_time += log_timestamps[0] - last_end_time
                    elif cur_type == 2:
                        cur_time += log_timestamps[0] - last_end_time
                
                if last_end_time == 0:
                    last_end_time = log_timestamps[-1]
                else:
                    # all_time_0[6] += log_timestamps[0] - last_end_time
                    # think_time += log_timestamps[0] - last_end_time
                    last_end_time = log_timestamps[-1]
            all_time_0[label].append(cur_time - change_text_time)
            # input()

    return np.array(all_time_0) / 1000

def cal_naive_time_separately_single():
    '''
    按照不同任务来计算时间, 但不分段, 除去该删除的时间不算
    0. 开始输入之前的时间（包括切换功能栏、撤销等）
    1. 第一次开始输入到最后一次开始输入之间的时间 (可删除)
    2. 最后一次开始输入到结束输入的时间，也就是 实际输入 的时间
    3. 最后一次结束输入到最后一次系统接收指令输入的时间（其中统计出文本修改的时间，也就是 调整指令 的时间 (可删除) ）
    4. 最后一次系统接收指令输入到执行完毕的时间
    5. 执行完毕之后的若干次候选切换时间
    6. 切换候选之后到下一次开始之前的时间
    '''
    all_time_0 = []
    for i in range(4):
        all_time_0.append([]) # last is gap time
    round_type_num = [0, 0, 0]
    round_num = 0
    total_time = 0
    for people in PEOPLE_NAIVE:
        for dir in listdir(os.path.join("naive", people)):
            pathname = os.path.join("naive", people, dir, "log.json")
            label = int(dir.split("-")[1]) - 1
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
            last_end_time = 0
            cur_type = 0
            total_time += inst_rounds[-1][-1][1] - inst_rounds[0][0][1]
            cur_time = 0
            change_text_time = 0

            for r in inst_rounds:
                all_time_0_bak = [i.copy() for i in all_time_0]
                log_texts = [i[0] for i in r]
                log_timestamps = [i[1] for i in r]
                

                # find all pos
                all_input_pos = find_indices(log_texts, instructions[0])
                all_end_input_pos = find_indices(log_texts, instructions[1])
                all_text_input_pos = find_indices(log_texts, instructions[3])
                all_get_inst_pos = find_indices(log_texts, instructions[4])
                all_change_chosen_pos = find_indices(log_texts, instructions[7])
                done_pos = log_texts.index(instructions[6])

                if instructions[0] in log_texts:
                    # 有语音
                    cur_type = 0
                    round_type_num[0] += 1
                    cur_time += log_timestamps[all_input_pos[0]] - log_timestamps[0]
                    # if len(all_input_pos) > 1:
                    #     cur_time += log_timestamps[all_input_pos[-1]] - log_timestamps[all_input_pos[0]]
                    if instructions[1] in log_texts:
                        if all_end_input_pos[-1] - all_input_pos[-1] > 0:
                            cur_time += log_timestamps[all_end_input_pos[-1]] - log_timestamps[all_input_pos[-1]]
                        else:
                            print(pathname, "最后一次输入没有结束")
                            all_time_0 = all_time_0_bak.copy()
                            continue
                    else:
                        print(pathname, "没有结束语音输入")
                        all_time_0 = all_time_0_bak.copy()
                        continue
                    # if instructions[4] in log_texts:
                    #     if all_get_inst_pos[-1] - all_end_input_pos[-1] > 0:
                    #         cur_time += log_timestamps[all_get_inst_pos[-1]] - log_timestamps[all_end_input_pos[-1]]
                    #     else:
                    #         print(pathname, "最后一次输入结束晚于指令输入")
                    #         all_time_0 = all_time_0_bak.copy()
                    #         continue
                    # else:
                    #     print(pathname, "没有指令输入")
                    #     all_time_0 = all_time_0_bak.copy()
                    #     continue
                    cur_time += log_timestamps[done_pos] - log_timestamps[all_end_input_pos[-1]]
                    if instructions[7] in log_texts:
                        if all_change_chosen_pos[-1] > done_pos:
                            cur_time += log_timestamps[all_change_chosen_pos[-1]] - log_timestamps[done_pos]
                        else:
                            print(pathname, "最后一次切换候选早于执行结束")
                            all_time_0 = all_time_0_bak.copy()
                            continue
                    if instructions[3] in log_texts:
                        for pos in all_text_input_pos:
                            if pos > 0:
                                change_text_time += log_timestamps[pos] - log_timestamps[pos - 1]
                elif instructions[3] in log_texts:
                    # 无语音，有文本变化
                    cur_type = 1
                    round_type_num[1] += 1 # 计数
                    all_end_input_pos = find_indices(log_texts, instructions[3])
                    # if instructions[4] in log_texts:
                    #     cur_time += log_timestamps[all_get_inst_pos[-1]] - log_timestamps[0]
                    #     # if all_get_inst_pos[-1] - all_end_input_pos[-1] > 0:
                    #     #     all_time_0[2] += log_timestamps[all_get_inst_pos[-1]] - log_timestamps[all_end_input_pos[-1]]
                    #     # else:
                    #     #     print(pathname, "最后一次输入结束晚于指令输入")
                    #     #     all_time_1 = all_time_1_bak.copy()
                    #     #     continue
                    # else:
                    #     print(pathname, "没有指令输入")
                    #     all_time_0 = all_time_0_bak.copy()
                    #     continue
                    # cur_time += log_timestamps[done_pos] - log_timestamps[all_get_inst_pos[-1]]
                    cur_time += log_timestamps[done_pos] - log_timestamps[0]
                    if instructions[7] in log_texts:
                        if all_change_chosen_pos[-1] > done_pos:
                            cur_time += log_timestamps[all_change_chosen_pos[-1]] - log_timestamps[done_pos]
                        else:
                            print(pathname, "最后一次切换候选早于执行结束")
                            all_time_0 = all_time_0_bak.copy()
                            continue
                else:
                    # 无语音，无文本变化
                    cur_type = 2
                    round_type_num[2] += 1
                    # if instructions[4] in log_texts:
                    #     cur_time += log_timestamps[all_get_inst_pos[-1]] - log_timestamps[0]
                    # else:
                    #     print(pathname, "没有指令输入")
                    #     all_time_0 = all_time_0_bak.copy()
                    #     continue
                    cur_time += log_timestamps[done_pos] - log_timestamps[0]
                    if instructions[7] in log_texts:
                        if all_change_chosen_pos[-1] > done_pos:
                            cur_time += log_timestamps[all_change_chosen_pos[-1]] - log_timestamps[done_pos]
                        else:
                            print(pathname, "最后一次切换候选早于执行结束")
                            all_time_0 = all_time_0_bak.copy()
                            continue
                if last_end_time > 0:
                    if cur_type == 0:
                        cur_time += log_timestamps[0] - last_end_time
                    elif cur_type == 1:
                        cur_time += log_timestamps[0] - last_end_time
                    elif cur_type == 2:
                        cur_time += log_timestamps[0] - last_end_time
                
                if last_end_time == 0:
                    last_end_time = log_timestamps[-1]
                else:
                    # all_time_0[6] += log_timestamps[0] - last_end_time
                    # think_time += log_timestamps[0] - last_end_time
                    last_end_time = log_timestamps[-1]
            # print(cur_time)
            # print(change_text_time)
            all_time_0[label].append(cur_time - change_text_time)
            # input()

    return np.array(all_time_0) / 1000

def cal_naive_whole_time():
    all_time_0 = []
    for _ in range(4):
        all_time_0.append([]) # last is gap time
    for people in PEOPLE_NAIVE:
        for dir in listdir(os.path.join("naive", people)):
            pathname = os.path.join("naive", people, dir, "log.json")
            label = int(dir.split("-")[1]) - 1
            with open(pathname, "r", encoding="utf-8") as f:
                try:
                    data = json.loads(f.read())
                    all_time_0[label].append(data[-1]["ts"] - data[0]["ts"])
                except Exception:
                    print(pathname)
    print(np.array(all_time_0) / 1000)
    return np.array(all_time_0) / 1000

def cal_think_time(all_people=PEOPLE):
    '''
    按照不同任务来计算时间, 但不分段, 除去该删除的时间不算
    0. 开始输入之前的时间（包括切换功能栏、撤销等）
    1. 第一次开始输入到最后一次开始输入之间的时间 (可删除)
    2. 最后一次开始输入到结束输入的时间，也就是 实际输入 的时间
    3. 最后一次结束输入到最后一次系统接收指令输入的时间（其中统计出文本修改的时间，也就是 调整指令 的时间 (可删除) ）
    4. 最后一次系统接收指令输入到执行完毕的时间
    5. 执行完毕之后的若干次候选切换时间
    6. 切换候选之后到下一次开始之前的时间
    '''
    all_think_time = []
    think_time_with_people = []
    for i in range(4):
        all_think_time.append([[], [], [], []]) # last is gap time
    for people in all_people:
        for dir in listdir(people):
            pathname = os.path.join(people, dir, "log.json")
            label = int(dir.split("-")[1]) - 1
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
            last_end_time = 0
            cur_type = 0
            cur_time = 0
            change_text_time = 0

            for r in inst_rounds:
                # all_time_0_bak = [i.copy() for i in all_time_0]
                log_texts = [i[0] for i in r]
                log_timestamps = [i[1] for i in r]
                

                # find all pos
                all_input_pos = find_indices(log_texts, instructions[0])
                all_end_input_pos = find_indices(log_texts, instructions[1])
                all_text_input_pos = find_indices(log_texts, instructions[3])
                all_get_inst_pos = find_indices(log_texts, instructions[4])
                all_change_chosen_pos = find_indices(log_texts, instructions[7])
                done_pos = log_texts.index(instructions[6])

                if instructions[0] in log_texts:
                    # 有语音
                    cur_type = 0
                    cur_time += log_timestamps[all_input_pos[0]] - log_timestamps[0]
                    if instructions[1] in log_texts:
                        if all_end_input_pos[-1] - all_input_pos[-1] > 0:
                            cur_time += log_timestamps[all_end_input_pos[-1]] - log_timestamps[all_input_pos[-1]]
                        else:
                            print(pathname, "最后一次输入没有结束")
                            # all_time_0 = all_time_0_bak.copy()
                            continue
                    else:
                        print(pathname, "没有结束语音输入")
                        # all_time_0 = all_time_0_bak.copy()
                        continue
                    if instructions[4] in log_texts:
                        if all_get_inst_pos[-1] - all_end_input_pos[-1] > 0:
                            cur_time += log_timestamps[all_get_inst_pos[-1]] - log_timestamps[all_end_input_pos[-1]]
                        else:
                            print(pathname, "最后一次输入结束晚于指令输入")
                            # all_time_0 = all_time_0_bak.copy()
                            continue
                    else:
                        print(pathname, "没有指令输入")
                        # all_time_0 = all_time_0_bak.copy()
                        continue
                    cur_time += log_timestamps[done_pos] - log_timestamps[all_get_inst_pos[-1]]
                    if instructions[7] in log_texts:
                        if all_change_chosen_pos[-1] > done_pos:
                            cur_time += log_timestamps[all_change_chosen_pos[-1]] - log_timestamps[done_pos]
                        else:
                            print(pathname, "最后一次切换候选早于执行结束")
                            # all_time_0 = all_time_0_bak.copy()
                            continue
                    if instructions[3] in log_texts:
                        for pos in all_text_input_pos:
                            if pos > 0:
                                change_text_time += log_timestamps[pos] - log_timestamps[pos - 1]
                elif instructions[3] in log_texts:
                    # 无语音，有文本变化
                    cur_type = 1
                    all_end_input_pos = find_indices(log_texts, instructions[3])
                    if instructions[4] in log_texts:
                        cur_time += log_timestamps[all_get_inst_pos[-1]] - log_timestamps[0]
                        # if all_get_inst_pos[-1] - all_end_input_pos[-1] > 0:
                        #     all_time_0[2] += log_timestamps[all_get_inst_pos[-1]] - log_timestamps[all_end_input_pos[-1]]
                        # else:
                        #     print(pathname, "最后一次输入结束晚于指令输入")
                        #     all_time_1 = all_time_1_bak.copy()
                        #     continue
                    else:
                        print(pathname, "没有指令输入")
                        # all_time_0 = all_time_0_bak.copy()
                        continue
                    cur_time += log_timestamps[done_pos] - log_timestamps[all_get_inst_pos[-1]]
                    if instructions[7] in log_texts:
                        if all_change_chosen_pos[-1] > done_pos:
                            cur_time += log_timestamps[all_change_chosen_pos[-1]] - log_timestamps[done_pos]
                        else:
                            print(pathname, "最后一次切换候选早于执行结束")
                            # all_time_0 = all_time_0_bak.copy()
                            continue
                else:
                    # 无语音，无文本变化
                    cur_type = 2
                    if instructions[4] in log_texts:
                        cur_time += log_timestamps[all_get_inst_pos[-1]] - log_timestamps[0]
                    else:
                        print(pathname, "没有指令输入")
                        # all_time_0 = all_time_0_bak.copy()
                        continue
                    cur_time += log_timestamps[done_pos] - log_timestamps[all_get_inst_pos[-1]]
                    if instructions[7] in log_texts:
                        if all_change_chosen_pos[-1] > done_pos:
                            cur_time += log_timestamps[all_change_chosen_pos[-1]] - log_timestamps[done_pos]
                        else:
                            print(pathname, "最后一次切换候选早于执行结束")
                            # all_time_0 = all_time_0_bak.copy()
                            continue
                if last_end_time > 0:
                    all_think_time[label][SEQUENCE[PEOPLE.index(people)].index(label + 1)].append(log_timestamps[0] - last_end_time)
                
                if last_end_time == 0:
                    last_end_time = log_timestamps[-1]
                else:
                    last_end_time = log_timestamps[-1]
            # input()
        # for i in all_think_time:
        #     for j in range(4):
        #         # i[j] = [np.mean(i[j]), len(i[j])]
        #         if (i[j]):
        #             i[j] = np.mean(i[j])
        #         else:
        #             i[j] = 0

        # print(all_think_time)
        # print(people)
        # print(SEQUENCE[PEOPLE.index(people)])
        # # for i in SEQUENCE[PEOPLE.index(people)]:
        # #     print(i)
        # #     print(all_think_time[i - 1][SEQUENCE[PEOPLE.index(people)].index(i)])
        # print([all_think_time[i - 1][SEQUENCE[PEOPLE.index(people)].index(i)] for i in SEQUENCE[PEOPLE.index(people)]])
        # think_time_with_people.append([all_think_time[i - 1][SEQUENCE[PEOPLE.index(people)].index(i)] for i in SEQUENCE[PEOPLE.index(people)]])
        # all_think_time = []
        # for i in range(4):
        #     all_think_time.append([[], [], [], []]) # last is gap time
        # input()

    # for i in all_think_time:
    #     for j in range(4):
    #         # i[j] = [np.mean(i[j]), len(i[j])]
    #         i[j] = [np.mean(i[j])]
    # print(all_think_time)
    return all_think_time
    # return np.array(all_think_time) / 1000
    # return think_time_with_people

if __name__ == "__main__":
    # show_certain_person("stp", 1)
    show_single(instructions.index("应用推荐修改"))
    # show_simple()
    # cal_naive_whole_time()
    # cal_time()
    # t = cal_think_time()
    # print([np.mean(i) for i in np.array(t).T])