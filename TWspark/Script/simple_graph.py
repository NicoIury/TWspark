import matplotlib
import matplotlib.pyplot as plt
import numpy as np
#from scipy.interpolate import spline

pos_dict= {'02-Feb-2020': 2, '01-Feb-2020': 0, '31-Jan-2020': 2, '30-Jan-2020': 3, '29-Jan-2020': 43, '28-Jan-2020': 6, '27-Jan-2020': 1}
neg_dict= {'02-Feb-2020': 2, '01-Feb-2020': 1, '31-Jan-2020': 0, '30-Jan-2020': 3, '29-Jan-2020': 11, '28-Jan-2020': 1, '27-Jan-2020': 0}


# Data for plotting

# 300 represents number of points to make between T.min and T.max

labels=pos_dict.keys()

x_len=np.arange(len(labels))

fig, ax = plt.subplots()

line1=ax.plot(x_len, pos_dict.values(),label="Positive",color='y')
line2=ax.plot(x_len, neg_dict.values(),label="Negative",color='g')

ax.set(xlabel='Day', ylabel='sentiment',
       title='Polarità nei giorni')

ax.set_xticks(x_len)
ax.set_xticklabels(labels, rotation=35)
ax.grid()
ax.legend()
#
fig.savefig("test.png")
plt.show()