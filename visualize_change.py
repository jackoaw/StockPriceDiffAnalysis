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

# prev_close = 0
for i in range(1, len(data)):
	line = data[i]
	try:
		comp_line = data[i + DAYS]
	except:
		#There is no more data to compare against if this is reached
		break
	cols1 = line.split(",")
	close_price1 = float(cols1[4])
	cols2 = comp_line.split(",")
	close_price2 = float(cols2[4])
	dif = close_price2 - close_price1
	poc = dif/close_price2 *100 #percent of change
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
