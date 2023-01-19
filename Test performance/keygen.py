import matplotlib.pyplot as plt

number = [0,100,200,300,400,500]

SDHP21 = [0.0, 2.8305749893188477, 5.328500270843506, 7.772222995758057, 10.965435981750488, 13.577021837234497]
Ours = [0.0, 5.834748983383179, 12.076683759689331, 17.971738576889038, 25.773389101028442, 32.4112184047699]

plt.figure(figsize=(15,10),linewidth = 3)

plt.plot(number,SDHP21,'d-',color = 'b', markersize=25, linewidth=2,label="SDH$\mathregular{^+}$21")
plt.plot(number,Ours,'*-',color = 'r', markersize=25, linewidth=2, label="Ours")


plt.xticks(fontsize=25)

plt.yticks(fontsize=25)

plt.xlabel("Number of Executions", fontsize=30, labelpad = 15)

plt.xlim([0,500])
plt.ylim([0, 40])

plt.ylabel("Time Cost of Key Generation (ms)", fontsize=30, labelpad = 20)


plt.legend(loc = "best", fontsize=25)

plt.savefig("keyegn.png",dpi=600)
plt.show()