# Assignment : Implementation of TCP congestion control algorithm (Tahoe)

import matplotlib.pyplot as plt
import seaborn as sns
import math

x = []
y = []

cwnd = int(input("Enter cwnd:"))
ssthresh = math.floor(cwnd/2)
limit = math.floor(cwnd*0.75)
value = 0
x.append(1)
y.append(0)
data_packet=1
for i in range(2,50):
    x.append(i)
    #exponential increase
    if 2**data_packet <ssthresh:
        value = 2**data_packet
        data_packet=data_packet+1
        y.append(value)
    #additive increase
    elif (value+1)<limit:
        value = value+1
        y.append(value)
    #multiplicative decrease
    else:
        data_packet = 0
        value = 0
        ssthresh = limit/2
        limit = limit*0.75
        y.append(value)

    print("Data Packet Value = ",value, ", ssthresh = ",ssthresh)

sns.set()
plt.plot(x,y)
plt.title("TCP Tahoe Congestion Window")
plt.ylabel("Congestion Window Size(in segments)")
plt.xlabel("Number of Transmissions")
plt.show()