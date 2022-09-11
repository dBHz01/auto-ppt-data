import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from dp_insts import inst_num_ave
from simplelog import cal_time

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = pct*total/100.0
        # 同时显示数值和占比的饼图
        return '{p:.2f}% ({v:.2f}s)'.format(p=pct,v=val)
    return my_autopct

def plot_inst_num():
    inst_num = inst_num_ave()
    inst_label = ["Both speech and gesture", "Only speech", "Only gesture", "Neither speech nor gesture (GUI)"]
    patched, l_text, p_text = plt.pie(inst_num, labels=inst_label, autopct='%.2f%%')
    for i in l_text:
        i.set_size(20)
    for i in p_text:
        i.set_size(15)
    plt.show()

def plot_inst_time():
    inst_time, round_num = cal_time()
    del(inst_time[-1])
    del(inst_time[4])
    del(inst_time[1])
    new_inst_time = [inst_time[i] for i in [1, 2, 3, 4, 0, 5]]
    new_inst_time = np.array(new_inst_time, dtype=np.float64) / round_num / 1000
    # time_display_text = ['开始输入之前各类指令时间', '第一次至最后一次开始输入(可删除)', '实际输入时间', '结束输入后的调整时间', '结束输入后修改文本时间(可删除)', '系统运行时间', '切换候选时间', '两轮之间思考时间', '忽略的时间']
    time_display_text = ['Speech input', 'Gesture input', 'System execution', 'Selecting candidates', 'Other commands', 'Interval between two commands']
    patched, l_text, p_text = plt.pie(new_inst_time, labels=time_display_text, autopct=make_autopct(new_inst_time))
    for i in l_text:
        i.set_size(20)
    for i in p_text:
        i.set_size(15)
    plt.show()

if __name__ == "__main__":
    plot_inst_num()
    plot_inst_time()