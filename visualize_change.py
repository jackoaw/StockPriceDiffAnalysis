import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import time
import sys

# File
readfile = sys.argv[1]
# Day period to examine
DAYS = int(sys.argv[2])

# used for counting 
change_map = {}

# used for distribution graph
change_list = []



data = None
with open (readfile, "r") as f:
    data=f.readlines()

allnums = 0 

prev_close = 0
for i in range(1,len(data), DAYS):
	line = data[i]
	cols = line.split(",")
	close_price = float(cols[4])
	if prev_close is 0:
		prev_close = close_price
		continue
	else:
		dif = close_price - prev_close
		prev_close = close_price
		poc = dif/close_price *100 #percent of change
		poc = float("%.1f"%poc)
		if poc in change_map.keys():
			change_map[poc] += 1
		else:
		 	change_map[poc] = 1
		change_list.append(poc)
		allnums +=1

for key in sorted(change_map.keys()):
    print("%s%%: %.2f%%" % (key, change_map[key]*1.0/allnums*100))

sns.set(color_codes=True)
sns.distplot(change_list, kde=True, rug=True);

plt.show()

# data = np.random.multivariate_normal([0, 0], [[5, 2], [2, 2]], size=2000)
# data = pd.DataFrame(data, columns=['x', 'y'])

# for col in 'xy':
#     plt.hist(data[col], alpha=0.5)
# plt.show()