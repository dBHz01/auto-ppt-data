from simplelog import cal_naive_time_separately_single, cal_naive_whole_time, cal_think_time, cal_time_separately, cal_time_separately_single 
from dp_insts import PEOPLE
import pandas as pd
from statsmodels.stats.anova import AnovaRM

indexes = []
times = []
people_list = []
for x in PEOPLE:
    res = cal_think_time([x])
    for idx in [0, 1, 2, 3]:
        indexes.append(idx)
        people_list.append(x)
        time_all = sum(res[idx][0]) + sum(res[idx][1]) + sum(res[idx][2]) + sum(res[idx][3])
        l_all = len(res[idx][0]) + len(res[idx][1]) + len(res[idx][2]) + len(res[idx][3])
        times.append(time_all / l_all)
df = pd.DataFrame({
        'name': people_list,
        'idx': indexes,
        'time': times
    })
print(AnovaRM(data=df, depvar='time',
              subject='name', within=['idx']).fit())