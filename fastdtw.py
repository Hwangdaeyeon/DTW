from Source import *
from multiprocessing import Process
import multiprocessing
import os
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean


Hum = []
Music = []
humpath_dir = "C:/Users/PC/Desktop/humming_data"
musicpath_dir = "C:/Users/PC/Desktop/music_data"
humfile_list = os.listdir(humpath_dir)
musicfile_list = os.listdir(musicpath_dir)
for file in humfile_list:
    Hum.append("C:/Users/PC/Desktop/humming_data/" + file)
for file in musicfile_list:
    Music.append("C:/Users/PC/Desktop/music_data/" + file)
 

def count(Mu_data) :
    a = open(Hum[0], 'r')
    Alines = a.readlines()
    A_data = []
    for line in Alines:
        line = line.strip()
        A_data.append(int(line))
    #for j in range(0, len(Music)) : 
    b = open(Mu_data, 'r')
    Blines = b.readlines()
    B_data = []
    for line in Blines:
        line = line.strip()
        B_data.append(int(line))
    lenA = len(A_data)
    lenB = len(B_data)
    C_data = []
    if lenA > lenB :
        Endline = lenA - lenB
        A, B = np.array(A_data[0:lenB]), np.array(B_data)
        distance = fastdtw(A, B)
        print(distance[0])
        C_data.append(int(distance[0]))
        for i in range(0, 20, 10) :
            if (A_data[i-10] == A_data[i]) and (A_data[lenB+i-10] == A_data[lenB+i]) : 
                continue
            else:
                A, B = np.array(A_data[i:lenB + i]), np.array(B_data)
                distance = fastdtw(A, B)
                print(distance[0])
                C_data.append(int(distance[0]))
    else : 
        Endline = lenB - lenA
        A, B = np.array(A_data), np.array(B_data[0:lenA])
        distance = fastdtw(A, B)
        print(distance[0])
        C_data.append(int(distance[0]))
        for i in range(0, 20, 10) :
            if (B_data[i-10] == B_data[i]) and (B_data[lenA+i-10] == B_data[lenA+i]) : 
                continue
            else:
                A, B = np.array(A_data), np.array(B_data[i:lenA + i])
                distance = fastdtw(A, B)
                print(distance[0])
                C_data.append(int(distance[0]))
    return min(C_data)
#    b.close
#    D_data[Music[0]] = min(C_data)
#    print(D_data)

if __name__ == '__main__':
    procs = []
    five_data = {}
    pool = multiprocessing.Pool(processes = 16)
    x = pool.map(count, Music)
    procs.append(x)
    print(procs)
    pool.close()
    pool.join()
    for i in range(0, 5) :
        a = min(procs[0])
        b = procs[0].index(min(procs[0]))
        five_data[Music[b]] = a
        procs[0].remove(a)
    print('['+Hum[0]+']',"가장 비슷한 5곡은")
    for name, dtwcost in five_data.items():  
        print(name, dtwcost)
