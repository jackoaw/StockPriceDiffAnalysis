import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
from scipy import stats
import time
import sys
from datetime import date
from yahoofinancials import YahooFinancials

def retrieve_data(symbol, start_date, end_date):
    symbol_yahoo_finance_interactor = YahooFinancials(symbol)
    days_data = symbol_yahoo_finance_interactor.get_historical_price_data(start_date, end_date, 'daily')
    # Convert it into a similiar CSV so I don't have to code a seperate method for this
    csv_str = "Date,Open,High,Low,Close,Adj Close,Volume\n"
    for price in days_data[symbol]["prices"]:
        csv_str += "%s,%s,%s,%s,%s,%s,%s\n"%(price["date"], price["open"], price["high"], price["low"], price["close"], price["adjclose"], price["volume"])
    csv_str = csv_str[:-1]
    f = open("symboldata\\" + symbol + ".csv", "w")
    f.write(csv_str)
    f.close()
    return csv_str[:-1]

# example commands:
# python .\visualize_change.py TSLA 3
# python .\visualize_change.py TSLA 3 2015-01-03

def start():

    # data contains all the daily csv data from Yahoo
    data = None
    try:
        # File
        symbol = sys.argv[1]
        # Day period to examine
        DAYS = int(sys.argv[2])
    except:
        print("Please enter valid parameters")
        exit(0)

    if len(sys.argv) > 3:
        #Start Date:
        start = sys.argv[3]
        #End Date, get the latest:
        end = date.today().strftime('%Y-%m-%d')
        data = retrieve_data(symbol, start, end).split('\n')
    else:
        with open ("symboldata\\" + symbol + ".csv", "r") as f:
           data=f.readlines()

    # used for counting 
    change_map = {}
    # used for distribution graph
    change_list = []
    #Option for rounding for accuracy, turn off for volotile stocks
    round_bool = True
    # Option for filtering out extreme data beyond 3 standard deviations
    filtering = False

    # # If file exists locally, use it
    # try:
    # # Otherwise pull the data
    # except:

    # Contains a count of the numbers
    allnums = 0 

    # Parse through the CSV
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

    # Code for printing out individual percentages and counts
    # for key in sorted(change_map.keys()):
    #     print("%s%%: %.2f%%" % (key, change_map[key]*1.0/allnums*100))

    std_dev = np.std(change_list)
    print("Standard Deviation: " + str(std_dev))
    # Filter out extreme data
    if filtering:
       change_list = list(filter(lambda x: x > -3*std_dev and x < 3*std_dev, change_list))
       std_dev = np.std(change_list)
       print("New Filtered Standard Deviation: " + str(std_dev))
    mean = np.mean(change_list)
    print("Mean: " + str(mean))
    median = np.median(change_list)
    print("Median: " + str(median))
    # Print out the standard deviations from the average up to 2 std deviations
    print("***********************")
    print("%.1f - %.1f : 95.4%%"%(mean-(std_dev*2), mean-std_dev))
    print("%.1f - %.1f : 68.2%%"%(mean-std_dev, mean))
    print("%.1f - %.1f : 68.2%%"%(mean, mean+std_dev))
    print("%.1f - %.1f : 95.4%%"%(mean+std_dev, mean+(std_dev*2)))
    print("***********************")

    df = pd.DataFrame(data=change_list, columns=["data"])
    bins = np.array([-5,-4.5,-4,-3.5,-3,-2.5,-2,-1.5,-1,-.5,0,.5,1,1.5,2,2.5,3,3.5,4,4.5,5])
    df["bucket"] = pd.cut(df.data, bins)

    histo = np.histogram(change_list, bins)

    for i in range(0, len(histo[0])):
       print("<%.1f : %i : %.2f%%"%(histo[1][i], histo[0][i], histo[0][i]/allnums*100))

    # sns.set(color_codes=True)
    # print(change_list)
    # sns.distplot(change_list, norm_hist=True, kde=True, rug=True);
    fig, axs = plt.subplots(1, 1, sharey=True, tight_layout=True)

    # We can set the number of bins with the `bins` kwarg
    axs.hist(change_list, bins=40, density=True)
    axs.yaxis.set_major_formatter(PercentFormatter(xmax=1))

    plt.show()

if __name__ == '__main__':
    start()