import matplotlib.pyplot as plt

number = [0,100,200,300,400,500]

SDHP21 = [0.0, 2.4897282123565674, 4.909003019332886, 7.146596193313599, 9.443500518798828, 11.777631282806396]
Ours = [0.0, 4.432475328445435, 8.272367238998413, 12.26508116722107, 16.694133520126343, 20.32093048095703]

plt.figure(figsize=(15,10),linewidth = 3)

plt.plot(number,SDHP21,'d-',color = 'b', markersize=25, linewidth=2,label="SDH$\mathregular{^+}$21")
plt.plot(number,Ours,'*-',color = 'r', markersize=25, linewidth=2, label="Ours")


plt.xticks(fontsize=25)

plt.yticks(fontsize=25)

plt.xlabel("Number of Executions", fontsize=30, labelpad = 15)

plt.xlim([0,500])
plt.ylim([0, 25])

plt.ylabel("Time Cost of Encryption (ms)", fontsize=30, labelpad = 20)


plt.legend(loc = "best", fontsize=25)

plt.savefig("enc.png",dpi=600)
plt.show()