import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

data1 = pd.read_csv("/home/thanhhai/Desktop/DistributedAI/evaluate/loss1.txt", delimiter=",", header=None)
data1 = np.array(data1)
data1 = data1[0]

data2 = pd.read_csv("/home/thanhhai/Desktop/DistributedAI/evaluate/loss2.txt", delimiter=",", header=None)
data2 = np.array(data2)
data2 = data2[0]

data3 = pd.read_csv("/home/thanhhai/Desktop/DistributedAI/evaluate/loss3.txt", delimiter=",", header=None)
data3 = np.array(data3)
data3 = data3[0]

data4 = pd.read_csv("/home/thanhhai/Desktop/DistributedAI/evaluate/loss4.txt", delimiter=",", header=None)
data4 = np.array(data4)
data4 = data4[0]


#plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], data1,'ko-', label='client 1')
plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], data2,'ro-', label='client 2')
plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], data3,'bo-', label='client 3')
#plt.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], data4,'yo-', label='client 4')

plt.ylabel('Log Loss')
plt.xlabel('Round')
plt.savefig("loss_graph.png")
