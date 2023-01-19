import matplotlib.pyplot as plt

number = [0,100,200,300,400,500]

SDHP21 = [0.0, 2.178166389465332, 4.098397970199585, 6.030190467834473, 8.185086965560913, 10.424789190292358]
Ours = [0.0, 4.892472982406616, 8.530346870422363, 12.630627870559692, 16.68919539451599, 20.30596685409546]

plt.figure(figsize=(15,10),linewidth = 3)

plt.plot(number,SDHP21,'d-',color = 'b', markersize=25, linewidth=2,label="SDH$\mathregular{^+}$21")
plt.plot(number,Ours,'*-',color = 'r', markersize=25, linewidth=2, label="Ours")


plt.xticks(fontsize=25)

plt.yticks(fontsize=25)

plt.xlabel("Number of Executions", fontsize=30, labelpad = 15)

plt.xlim([0,500])
plt.ylim([0, 25])

plt.ylabel("Time Cost of Key Delegation (ms)", fontsize=30, labelpad = 20)


plt.legend(loc = "best", fontsize=25)

plt.savefig("keydel.png",dpi=600)
plt.show()