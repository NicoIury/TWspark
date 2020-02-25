import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from collections import OrderedDict
new_neg_dict={}
new_pos_dict={}
pos_dict= {'02-Feb-2020': 10, '01-Feb-2020': 20, '31-Jan-2020': 2, '30-Jan-2020': 1, '29-Jan-2020': 43, '28-Jan-2020': 6, '27-Jan-2020': 1}
neg_dict= {'02-Feb-2020': 1, '01-Feb-2020': 2, '31-Jan-2020': 20, '30-Jan-2020': 10, '29-Jan-2020': 11, '28-Jan-2020': 1, '27-Jan-2020': 0}

somma = dict(Counter(pos_dict)+Counter(neg_dict))

#
for k in sorted(somma, key=somma.get, reverse=True):
    new_neg_dict[k]=neg_dict[k]
    new_pos_dict[k] = pos_dict[k]

print(new_neg_dict)
print(new_pos_dict)

print(f"Valori da plottare:\nPositivi: {pos_dict.values()}\nNegativi: {neg_dict.values()}")
labels=new_neg_dict.keys()

x = np.arange(len(labels))  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, new_pos_dict.values(),width, label='Positive',color='y')
rects2 = ax.bar(x + width/2, new_neg_dict.values(),width, label='Negative',color='g')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Sentiment')
ax.set_title('Polarità nei giorni')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=40)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
autolabel(rects1)
autolabel(rects2)
fig.tight_layout()
#ax.invert_xaxis()
plt.show()