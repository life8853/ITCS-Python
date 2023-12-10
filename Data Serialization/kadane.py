import pickle
import time

datafile = open("substr_1e4.pkl", 'rb')
data = pickle.load(datafile)
datafile.close()
n = len(data)
maxsum = 0
start = time.time()

if(len(data) == 0):
    t = 0 
else:
    biggest_sum = data[0]
    curr_sum = 0
    for element in data:
        curr_sum = curr_sum + element
        if(curr_sum > biggest_sum):
            biggest_sum = curr_sum
        if curr_sum < 0:
            curr_sum = 0




t = time.time()-start
print(n, t, biggest_sum)