size = 0
source = 0
target = 0
residual_flow = {}
flows = {}
price = {}
labels = {}
weight_flows = 0


def setup():
    global size
    counter = 1
    while counter <= size:
        line_counter = 1
        while line_counter <= size:
            flows[(counter, line_counter)] = 0
            residual_flow[(counter, line_counter)] = 0
            line_counter += 1
        counter += 1


def file_read(filename):
    global size, source, target, residual_flow, price, flow
    with open(filename, 'r') as reader:
        first_line = reader.readline().split(' ')
        size = int(first_line[0])
        edge_count = int(first_line[1])
        source = int(first_line[2])
        target = int(first_line[3])
        setup()
        for i in range(edge_count):
            line = reader.readline().split(' ')
            u = int(line[0])
            v = int(line[1])
            c = int(line[2])
            p = int(line[3])
            residual_flow[(u, v)] = c
            price[(u, v)] = p
            price[(v, u)] = -p


def get_input(filename):
    global size, source, target, residual_flow
    # file_read('input.txt')
    with open(filename, 'r') as reader:
        size = int(reader.readline())
        counter = 1
        while counter <= size:
            split_line = reader.readline().split()
            line_counter = 1
            while line_counter <= len(split_line):
                residual_flow[(counter, line_counter)] = int(split_line[line_counter - 1])
                flows[(counter, line_counter)] = 0
                line_counter += 1
            counter += 1
        source = int(reader.readline())
        target = int(reader.readline())


def get_output(filename):
    with open(filename, 'w') as writer:
        result = ''
        counter = 1
        for el in flows.items():
            if counter <= size:
                result += (str(el[1]) + ' ')
                counter += 1
            if counter == size + 1:
                result += '\n'
                counter = 1
        result += str(weight_flows)
        writer.write(result)


def decide():
    global labels
    global weight_flows

    labels[source] = (float('inf'), 0)
    current = source
    while True:
        st_way = set()
        for val in range(1, size + 1):
            if val not in labels and residual_flow[current, val] > 0:
                st_way.add(val)
        maximum = (0, 0)
        if len(st_way) != 0:
            for val in st_way:
                if residual_flow[(current, val)] > maximum[0]:
                    maximum = (residual_flow[(current, val)], val)
            labels[maximum[1]] = (maximum[0], current)
            if maximum[1] == target:
                minimum = maximum[0]
                u = maximum[1]
                while u != source:
                    u = labels[u][1]
                    if labels[u][0] < minimum:
                        minimum = labels[u][0]
                weight_flows += minimum
                next_value = maximum[1]
                while next_value != source:
                    residual_flow[labels[next_value][1], next_value] -= minimum
                    residual_flow[next_value, labels[next_value][1]] += minimum
                    flows[labels[next_value][1], next_value] += minimum
                    next_value = labels[next_value][1]
                labels.clear()
                labels[source] = (float('inf'), 0)
                current = source
            else:
                current = maximum[1]
        else:
            if current == source:
                break
            current = labels[current][1]


def min_cost_flow():
    global flows
    min_cost = 0
    for u in range(size):
        for v in range(size):
            if flows[u, v] > 0:
                min_cost += flows[u, v] * P[u][v]


if __name__ == '__main__':
    file_read('input.txt')
    decide()
    get_output('out.txt')
