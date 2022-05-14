from flow_decider import *


def file_read():
    global N, M, s, t, C, P
    with open('input.txt', 'r') as reader:
        first_line = reader.readline().split(' ')
        N = int(first_line[0])
        M = int(first_line[1])
        s = int(first_line[2])
        t = int(first_line[3])
        for i in range(M):
            line = reader.readline().split(' ')
            u = int(line[0])
            v = int(line[1])
            c = int(line[2])
            p = int(line[3])
            C[u][v] = c
            P[u][v] = p
            P[v][u] = -p


