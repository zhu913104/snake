import numpy  as np
import matplotlib.pyplot as plt


train_historys1 = np.load("data/useful/train_historys_map7_GA_3(9, 15,8, 3).npy")
train_historys2 = np.load("data/useful/train_historys_map7_GA_4(9, 15,8, 3).npy")
train_historys3 = np.load("data/useful/train_historys_map7_GA_5(9, 15,8, 3).npy")
train_historys4 = np.load("data/useful/train_historys_map7_GA_6(9, 15,8, 3).npy")
train_historys5 = np.load("data/useful/train_historys_map7_GA_9(9, 15,8, 3).npy")

train_historys6 = np.load("data/useful/train_historys_map7_CGA_3(9, 15,8, 3).npy")
train_historys7 = np.load("data/useful/train_historys_map7_CGA_4(9, 15,8, 3).npy")
train_historys8 = np.load("data/useful/train_historys_map7_CGA_5(9, 15,8, 3).npy")
train_historys9 = np.load("data/useful/train_historys_map7_CGA_6(9, 15,8, 3).npy")
train_historys10 = np.load("data/useful/train_historys_map7_CGA_2(9, 15,8, 3).npy")


train_historys_cga=np.dstack((train_historys6[:300,:],train_historys7[:300,:],train_historys8[:300,:],train_historys9[:300,:],train_historys10[:300,:]))
train_historys_cga=np.mean(train_historys_cga,axis=2)

train_historys_ga=np.dstack((train_historys1[:300,:],train_historys2[:300,:],train_historys3[:300,:],train_historys4[:300,:],train_historys5[:300,:]))
train_historys_ga=np.mean(train_historys_ga,axis=2)

meandistance_idx,meandistance=[i  for i,data in enumerate(train_historys_ga[:,0])],[data  for i,data in enumerate(train_historys_ga[:,0])]
maxdistance_idx,maxdistance=[i  for i,data in enumerate(train_historys_ga[:,1])],[data  for i,data in enumerate(train_historys_ga[:,1])]


meandistance_CGA_idx,meandistance_CGA=[i  for i,data in enumerate(train_historys_cga[:300,0])],[data  for i,data in enumerate(train_historys_cga[:300,0])]
maxdistance_CGA_idx,maxdistance_CGA=[i  for i,data in enumerate(train_historys_cga[:300,1])],[data  for i,data in enumerate(train_historys_cga[:300,1])]
# plt.subplot(1, 2, 1)
plt.plot(meandistance_idx,meandistance,label="GA")
# plt.plot(maxdistance_CGA_idx,meandistance_CGA,label="CGA")
plt.axis([-1, 300 ,-1, 5000])
plt.ylabel("Mean Distance", fontsize=16)
plt.xlabel("generation", fontsize=16)
plt.legend(loc=9, borderaxespad=0.)
# plt.subplot(1, 2, 2)
# plt.plot(maxdistance_idx,maxdistance,label="GA")
# plt.plot(maxdistance_CGA_idx,maxdistance_CGA,label="CGA")
# plt.axis([-1, 300 ,-1, 350000])
# plt.ylabel("Distance", fontsize=16)
# plt.xlabel("generation", fontsize=16)
# plt.legend(loc=9, borderaxespad=0.)
plt.show()