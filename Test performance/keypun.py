import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(15,10), linewidth = 3)

number = [10,20,30,40,50]

Ours_1 = [0.2606344223022461, 0.4581029415130615, 0.6449337005615234, 0.8742117881774902, 1.0665478706359863]
Ours_2 = [0.2606344223022461, 0.4581029415130615, 0.6449337005615234, 0.8742117881774902, 1.0665478706359863]

x = np.arange(len(number))
width = 0.3

bar1 = plt.bar(x, Ours_1, width, color='#4daf4a', hatch='|', label='m = 5')
bar2 = plt.bar(x + width, Ours_2, width, color='#377eb8', hatch='//', label='m = 10')

plt.ylim([0, 1.5])

plt.xticks(x + width / 2, number, fontsize=30)

plt.yticks(fontsize=30)

plt.xlabel("Number of Tags", fontsize=30, labelpad = 20)

plt.ylabel("Time Cost", fontsize=30, labelpad = 15)

plt.legend(loc = "best", fontsize=25)

for bar in bar1:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width(), height,
             '{:.3f}'.format(height),
             ha='center', va='bottom',fontsize=25)
    
plt.savefig("keypun.png",dpi=600)
plt.show()
