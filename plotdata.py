import numpy  as np
import matplotlib.pyplot as plt


train_historys = np.load("data/train_historys_map7_1(9, 15,8, 3).npy")

train_historys_CAG = np.load("data/train_historys_map7_CGA(9, 15,8, 3).npy")

meandistance_idx,meandistance=[i  for i,data in enumerate(train_historys[:,0])],[data  for i,data in enumerate(train_historys[:,0])]
maxdistance_idx,maxdistance=[i  for i,data in enumerate(train_historys[:,1])],[data  for i,data in enumerate(train_historys[:,1])]


meandistance_CGA_idx,meandistance_CGA=[i  for i,data in enumerate(train_historys_CAG[:,0])],[data  for i,data in enumerate(train_historys_CAG[:,0])]
maxdistance_CGA_idx,maxdistance_CGA=[i  for i,data in enumerate(train_historys_CAG[:,1])],[data  for i,data in enumerate(train_historys_CAG[:,1])]
plt.subplot(1, 2, 1)
plt.plot(meandistance_idx,meandistance,label="GA")
plt.plot(maxdistance_CGA_idx,meandistance_CGA,label="CGA")
plt.ylabel("Distance", fontsize=16)
plt.xlabel("generation", fontsize=16)
plt.legend(loc=9, borderaxespad=0.)
plt.subplot(1, 2, 2)
plt.plot(maxdistance_idx,maxdistance,label="GA")
plt.plot(maxdistance_CGA_idx,maxdistance_CGA,label="CGA")
plt.ylabel("Distance", fontsize=16)
plt.xlabel("generation", fontsize=16)
plt.legend(loc=9, borderaxespad=0.)
plt.show()