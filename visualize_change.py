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

#Option for rounding for accuracy, turn off for volotile stocks
round_bool = True

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
	if round_bool:
		poc = round(poc, 1)
	else:
		poc = float("%.1f"%poc)
	if poc in change_map.keys():
		change_map[poc] += 1
	else:
	 	change_map[poc] = 1
	change_list.append(poc)
	allnums +=1

# for key in sorted(change_map.keys()):
#     print("%s%%: %.2f%%" % (key, change_map[key]*1.0/allnums*100))

sns.set(color_codes=True)
sns.distplot(change_list, norm_hist=True, kde=True, rug=True);

# plt.show()

std_dev = np.std(change_list)
print("Standard Deviation: " + str(std_dev))

df = pd.DataFrame(data=change_list, columns=["data"])
bins = np.array([-5,-4.5,-4,-3.5,-3,-2.5,-2,-1.5,-1,-.5,0,.5,1,1.5,2,2.5,3,3.5,4,4.5,5])
df["bucket"] = pd.cut(df.data, bins)
print(df.head(10))

histo = np.histogram(change_list, bins)

print(histo[1])
print(histo[0])
for i in range(0, len(histo[0])):
	print("<%.1f : %i : %.2f%%"%(histo[1][i], histo[0][i], histo[0][i]/allnums*100))

#EXTRA: 

# data = np.random.multivariate_normal([0, 0], [[5, 2], [2, 2]], size=2000)
# data = pd.DataFrame(data, columns=['x', 'y'])

# for col in 'xy':
#     plt.hist(data[col], alpha=0.5)
# plt.show()