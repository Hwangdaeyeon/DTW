# https://gist.github.com/bistaumanga/6023705

from math import *
import numpy as np
import sys

def DTW2(exdata, data, A, B, window = sys.maxsize, d = lambda x,y: abs(x-y)): # 한정값과 비교한 데이터의 배열을 입력으로 줌
    naljibreak = True
    A, B = np.array(A), np.array(B)                           
    M, N = len(A), len(B)
    cost = sys.maxsize * np.ones((M, N))                     

    cost[0, 0] = d(A[0], B[0])                                 
    for i in range(1, M):
        cost[i, 0] = cost[i-1, 0] + d(A[i], B[0])             

    for j in range(1, N):
        cost[0, j] = cost[0, j-1] + d(A[0], B[j])              

    if (cost[M-1, 0]+cost[0, N-1]) > exdata :                    # 분기한정 기법으로 한정값을 1열 마지막 해 값 + 1행 마지막 열 값으로 설정
        cost = False                                             # 다음 비교할 한정값이 이전 한정값보다 크면 비교를 진행하지 않는다
        return cost, exdata
    else :
        exdata = cost[M-1, 0]+cost[0, N-1]                       # 한정값이 더 작으면 한정값 교체
        for i in range(1, M):                                       # 2번째 열부터 주변 값들중 가장 작은 값과 행의 값과 열의 값의 차에 절대값을 더해준다
            for j in range(max(1, i - window), min(N, i + window + 1)):
                choices = cost[i - 1, j - 1], cost[i, j-1], cost[i-1, j]
                cost[i, j] = min(choices) + d(A[i], B[j])
                if cost[i, j] > min(data):                          # 백트래킹 기술 = 진행중 하나의 허밍과 데이터 사이의 비교값을 저장한 배열중 가장
                    naljibreak = False                               # 작은것 보다 크면 그 비교문 종료
                    break
            if(naljibreak == False):
                break
    
        if(naljibreak == False):
            cost = False
            return cost, exdata
        else:
            return cost[-1, -1], exdata                                         # 2차원 배열의 가장 끝의 값을 반환한다.(끝값이 DTW거리)

def DTW(A, B, window = sys.maxsize, d = lambda x,y: abs(x-y)):  # lamda는 두 수를 입력을 받고 두 수의 파의 절대값 저장(window는 배열의 행과 열의 크기를 말하는 것 같다)
    A, B = np.array(A), np.array(B)                             # np.array를 통해 입력받은 리스트로 배열을 만들어 준다
    M, N = len(A), len(B)
    cost = sys.maxsize * np.ones((M, N))                        # 배열을 초기화해준다.

    cost[0, 0] = d(A[0], B[0])                                  # 2차원 배열의 첫번째 값은 열과 행의 첫번째 값들의 차에 절대값
    for i in range(1, M):
        cost[i, 0] = cost[i-1, 0] + d(A[i], B[0])               # 1번째 열의 값을 전열의 값에 지정해준 자리의 열과 행에 차의 절대값을 더해준다

    for j in range(1, N):
        cost[0, j] = cost[0, j-1] + d(A[0], B[j])               # 첫번째 행도 열과 마찬가지
    #for i in range(1, N):
    for i in range(1, M):                                       # 2번째 열부터 주변 값들중 가장 작은 값과 행의 값과 열의 값의 차에 절대값을 더해준다
        for j in range(max(1, i - window), min(N, i + window + 1)):
            choices = cost[i - 1, j - 1], cost[i, j-1], cost[i-1, j]
            cost[i, j] = min(choices) + d(A[i], B[j])
    excost = cost[M-1,0] + cost[0, N-1]                         # 한정값 excost를 리턴
    return cost[-1, -1], excost