import numpy  as np
import matplotlib.pyplot as plt


train_historys = np.load("data/train_historys_map7_1(9, 15,8, 3).npy")

meandistance_idx,meandistance=[i  for i,data in enumerate(train_historys[:,0])],[data  for i,data in enumerate(train_historys[:,0])]
maxdistance_idx,maxdistance=[i  for i,data in enumerate(train_historys[:,1])],[data  for i,data in enumerate(train_historys[:,1])]
plt.subplot(1, 2, 1)
plt.plot(meandistance_idx,meandistance,label="Mean distance")
plt.ylabel("Distance", fontsize=16)
plt.xlabel("generation", fontsize=16)
plt.legend(loc=9, borderaxespad=0.)
plt.subplot(1, 2, 2)
plt.plot(maxdistance_idx,maxdistance,label="Max distance")
plt.ylabel("Distance", fontsize=16)
plt.xlabel("generation", fontsize=16)
plt.legend(loc=9, borderaxespad=0.)
plt.show()