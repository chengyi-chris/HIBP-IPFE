import matplotlib.pyplot as plt

number = [0,100,200,300,400,500]

SDHP21 = [0.0, 0.36129236221313477, 0.8510441780090332, 1.1819829940795898, 1.5737345218658447, 1.8352644443511963]
Ours = [0.0, 0.7133011817932129, 1.7107572555541992, 2.568082571029663, 3.4493861198425293, 4.361863136291504]

plt.figure(figsize=(15,10),linewidth = 3)

plt.plot(number,SDHP21,'d-',color = 'b', markersize=25, linewidth=2,label="SDH$\mathregular{^+}$21")
plt.plot(number,Ours,'*-',color = 'r', markersize=25, linewidth=2, label="Ours")


plt.xticks(fontsize=25)

plt.yticks(fontsize=25)

plt.xlabel("Number of Executions", fontsize=30, labelpad = 15)

plt.xlim([0,500])
plt.ylim([0, 6])

plt.ylabel("Time Cost of Decryption (ms)", fontsize=30, labelpad = 20)


plt.legend(loc = "best", fontsize=25)

plt.savefig("dec.png",dpi=600)
plt.show()