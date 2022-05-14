from queue import Queue


MAX_N = 10 ** 3
MAX_VAL = 10 ** 9

C = []  # Матрица "пропускных способностей"
F = []  # Матрица "текущего потока в графе"
P = []  # Матрица "стоимости (расстояний)"

push = []      # Поток в вершину [v] из начальной точки
mark = []      # Отметки на вершинах, в которых побывали
pred = []      # Откуда пришли в вершину [v] (предок)
dist = []      # Расстояние до вершины [v] из начальной точки

N = 0
M = 0
s = 0
t = 0  # Кол-во вершин, ребер, начальная и конечные точки

max_flow = 0
min_cost = 0


class PQueue(Queue):
    def front(self):
        return self.queue[0]

    def peek(self):
        return self.queue[len(self.queue)]


def create_array(arr, size=1):
    for i in range(MAX_N):
        arr.append(0)
        if size > 1:
            arr[i] = []
            create_array(arr[i], size=size-1)


def setup():
    global C, F, P, push, mark, pred, dist
    create_array(C, 2)
    create_array(F, 2)
    create_array(P, 2)

    create_array(push)
    create_array(mark)
    create_array(pred)
    create_array(dist)


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


def edge_cost(u, v):
    if C[u][v] - F[u][v] > 0:
        return P[u][v]
    else:
        return MAX_VAL


def check_cycles():
    for u in range(1, N):
        for v in range(N):
            if dist[v] > dist[u] + edge_cost(u, v):
                return u
    return MAX_VAL


def init():
    for i in range(N):
        mark[i] = 0
        push[i] = 0
        pred[i] = 0
        dist[i] = MAX_VAL


# Алгоритм Поиска в ширину
def bf(start):
    init()
    Q = PQueue()
    pred[start] = start
    dist[start] = 0
    Q.put(start)
    Q.put(MAX_N)
    series = 0

    while not Q.empty():
        while Q.front() == MAX_N:
            Q.get()
            series += 1
            if series > N:
                return check_cycles()
            else:
                Q.put(MAX_N)
        u = Q.front()
        Q.get()
        for v in range(N):
            if dist[v] > dist[u] + edge_cost(u, v):
                dist[v] = dist[u] + edge_cost(u, v)
                pred[v] = u
                Q.put(v)


# Алгоритм Беллмана-Форда
def bfs(start, target):
    init()
    Q = PQueue()
    mark[start] = 1
    pred[start] = start
    push[start] = MAX_VAL

    Q.put(start)
    while mark[target] == 0 and not Q.empty():
        u = Q.front()
        Q.get()
        for v in range(N):
            if mark[target] == 0 and (C[u][v] - F[u][v] > 0):
                push[v] = min(push[u], C[u][v] - F[u][v])
                mark[v] = 1
                pred[v] = u
                Q.put(v)
    return mark[target]


# Алгоритм Форда-Фалкерсона
def max_flow_ff():
    global max_flow, F

    flow = 0
    flag = bfs(s, t)
    while flag != 0:
        add = push[t]
        v = t
        u = pred[v]
        while v != s:
            F[u][v] += add
            F[v][u] -= add
            v = u
            u = pred[v]
        flow += add
        flag = bfs(s, t)
    max_flow = flow


# Алгоритм вычисления Максимального поток минимальной стоимости
def min_cost_flow():
    global min_cost, F, P

    max_flow_ff()
    for u in range(N):
        for v in range(N):
            if F[u][v] > 0:
                min_cost += F[u][v] * P[u][v]


if __name__ == '__main__':
    setup()
    file_read()
    min_cost_flow()

    print('FLOW: ' + str(max_flow))
    print('PRICE: ' + str(min_cost))
