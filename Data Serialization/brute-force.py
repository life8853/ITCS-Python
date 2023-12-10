import pickle
import time

datafile = open("substr_1e4.pkl", 'rb')
data = pickle.load(datafile)
datafile.close()
n = len(data)
maxsum = 0
start = time.time()

for p in range(0, n):
    print(p)
    for q in range(p, n):
        s = 0
        for i in range(p, q+1):
            s += data[i]
        maxsum = max(maxsum, s)


t = time.time()-start
print(n, t, maxsum)