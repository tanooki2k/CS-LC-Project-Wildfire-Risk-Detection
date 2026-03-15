from queue import Queue
from typing import Dict, List, Tuple


def convert_data(d: List[Dict[str, str]], p: List[Tuple[str, str]]) -> List[Queue]:
    subdata = [Queue() for _ in range(len(p))]

    for dic in d:
        sub_queues = [Queue() for _ in range(len(p))]

        for key, val in dic.items():
            for index, pair in enumerate(p):
                if key in pair:
                    sub_queues[index].put(float(val))

        for index, sb in enumerate(sub_queues):
            subdata[index].put(sb)
    return subdata


def show_data(d, p):
    for i in range(len(p)):
        print(p[i])

        while not d[i].empty():
            pair_queue = d[i].get()

            while not pair_queue.empty():
                elem = pair_queue.get()
                print(elem, end=" ")
            print()
        print()


if __name__ == "__main__":
    data = [{'t': '1', 'x': '1', 'y': '2'}, {'t': '2', 'x': '3', 'y': '4'}, {'t': '3', 'x': '5', 'y': '6'},
            {'t': '4', 'x': '7', 'y': '8'}, {'t': '5', 'x': '9', 'y': '10'}, {'t': '6', 'x': '11', 'y': '12'},
            {'t': '7', 'x': '13', 'y': '14'}, {'t': '8', 'x': '15', 'y': '16'}, {'t': '9', 'x': '17', 'y': '18'},
            {'t': '10', 'x': '19', 'y': '20'}, {'t': '11', 'x': '23', 'y': '18'}]
    pairs = [("t", "x"), ("t", "y"), ("x", "y")]

    sb_data = convert_data(data, pairs)
    show_data(sb_data, pairs)
    print("Loop ended!")
