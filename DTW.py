from Source import *
import os
from multiprocessing import Process
import multiprocessing
import time

start_time = time.time()

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

def count(Humming):
    five_data = {}                   # i번째 허밍데이터 100개의 뮤직데이터를 비교해 최소값 5개가 들어갈 딕셔너리
    Total_data = []                  # i번째 허밍데이터와 100개의 뮤직데이터를 비교한 값이 들어갈 리스트
    a = open(Humming, 'r')            
    Alines = a.readlines()
    A_data = []
    for line in Alines:              # 리스트를 만들어 i번째 허밍데이터를 읽어 리스트에 입력
        line = line.strip()
        A_data.append(int(line))
    for j in range(0, 100) :         # 뮤직데이터 개수 만큼 반복
        Sub_data = []                # i번째 허밍데이터 하나의 뮤직데이터를 비교한 값이 들어갈 리스트
        b = open(Music[j], 'r')      
        Blines = b.readlines()
        B_data = []
        for line in Blines:          # 리스트를 만들어 j번째 뮤직데이터를 읽어 리스트에 입력
            line = line.strip()
            B_data.append(int(line))
        lenA = len(A_data) 
        lenB = len(B_data)
        if lenA > lenB :             # 뮤직데이터의 길이가 허밍데이터보다 짧은 것이 있으므로 if문으로 조정
            Endline = lenA - lenB    # 뮤직데이터의 길이가 허밍데이터보다 짧으면 반복횟수를 허밍데이터 - 뮤직데이터로 설정
            A, B = np.array(A_data[0:lenB]), np.array(B_data)
            cost, excost = DTW(A, B, 7)
            #print(cost)
            Sub_data.append(int(cost))
            for i in range(10, 100, 10) : # 10개씩 이동하면서 비교
                if (A_data[i-10] == A_data[i]) and (A_data[lenB+i-10] == A_data[lenB+i]) : # 뮤직 데이터가 같은 값이 연속되는 것이 많이 있기 때문에 전에 비교한 뮤직테이터의 
                    continue                                                               # 첫번째 값과 지급 비교할 첫번째 값, 마지막값과 마지막값이 같으면 다음 반복으로 이동
                else:
                    A, B = np.array(A_data[i:lenB + i]), np.array(B_data) # 허밍데이터가 더 큼으로 허밍데이터의 크기를 뮤직데이터의 크기로 조정
                    cost, excost = DTW2(excost, Sub_data, A, B, 7)         # 백트래킹과 분기 한정법을 적용한 DTW2이용
                    if (cost != False):
                        #print(cost)
                        Sub_data.append(int(cost))
        else :                       # 뮤직데이터의 길이가 허밍데이터보다 길면 반복횟수를 뮤직데이터 - 허밍데이터로 설정
            Endline = lenB - lenA
            A, B = np.array(A_data), np.array(B_data[0:lenA])
            cost, excost = DTW(A, B, 7)
            #print(cost)
            Sub_data.append(int(cost))
            for i in range(10, 100, 10) : # 비교(10씩 증가)
                if (B_data[i-10] == B_data[i]) and (B_data[lenA+i-10] == B_data[lenA+i]) :
                    continue
                else:
                    A, B = np.array(A_data), np.array(B_data[i:lenA + i]) # 뮤직데이터가 더 큼으로 뮤직데이터의 크기를 허밍데이터의 크기로 조정
                    cost, excost = DTW2(excost, Sub_data, A, B, 7)              # 허밍데이터와 허밍데이터의 크기만큼 자른 뮤직데이터를 DTW소스에 입력
                    if (cost != False):                         # 백트래킹과 분기 한정법을 적용한 DTW2이용
                        #print(cost)
                        Sub_data.append(int(cost))       # 앞서만든 리스트에 비교값들을 추가
        b.close
        Total_data.append(int(min(Sub_data)))      # i번째 허밍데이터와 j번째 뮤직데이터를 비교한 값들중 최소값을 리스트에 추가
    print('['+Humming+']', "와 가장 유사한 5곡은 ⏬")
    for i in range(0, 5) :
        mindata = Total_data.index(min(Total_data))
        five_data[Music[mindata]] = int(min(Total_data)) # i번째 허밍데이터와 100개의 뮤직데이터를 비교한 값중 가장 작은 5가지를 저장
        Total_data.remove(min(Total_data))
    for name, dtwcost in five_data.items():   # i번째 허밍데이터와 100개의 뮤직데이터를 비교한 값중 가장 작은 5가지를 출력
        print(name, dtwcost)
    a.close
if __name__ == '__main__':
    pool = multiprocessing.Pool(processes = 4) # 멀티프로세싱을 이용해 허밍데이터를 입력으로 4개의 코어를 사용
    pool.map(count, Hum)
    pool.close()
    pool.join()

print("--------- %s seconds----------" % (time.time() - start_time))