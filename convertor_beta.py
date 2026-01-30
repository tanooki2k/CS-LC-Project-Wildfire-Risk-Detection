from queue import Queue

data = [{'t': '1', 'x': '1', 'y': '2'}, {'t': '2', 'x': '3', 'y': '4'}, {'t': '3', 'x': '5', 'y': '6'},
        {'t': '4', 'x': '7', 'y': '8'}, {'t': '5', 'x': '9', 'y': '10'}, {'t': '6', 'x': '11', 'y': '12'},
        {'t': '7', 'x': '13', 'y': '14'}, {'t': '8', 'x': '15', 'y': '16'}, {'t': '9', 'x': '17', 'y': '18'},
        {'t': '10', 'x': '19', 'y': '20'}, {'t': '11', 'x': '23', 'y': '18'}]
pairs = [("t", "x"), ("t", "y"), ("x", "y")]

subdata = [Queue() for _ in range(len(pairs))]

for dic in data:
    subqueues = [Queue() for _ in range(len(pairs))]

    for key, val in dic.items():
        for index, pair in enumerate(pairs):
            if key in pair:
                subqueues[index].put(int(val))

    for index, sb in enumerate(subqueues):
        subdata[index].put(sb)

if __name__ == "__main__":
    for index in range(len(pairs)):
        print(pairs[index])

        for _ in range(len(data)):
            t = subdata[index].get()

            for _ in range(2):
                elem = t.get()
                print(elem, end=" ")
            print()
        print()

print("Loop eneded!")
