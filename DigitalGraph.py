from random import randint
from typing import List, Tuple, Any
from matplotlib.pyplot import plot, show
from Graphing import MatplotlibGraph


class DigitalGraph(MatplotlibGraph):
    x, y = [], []

    def __init__(self, data: List[Tuple[Any, Any]] = None) -> None:
        for elem in data:
            if len(elem) != 2:
                raise ValueError("All elements must be pairs `(x, y)`")

        first_elem = data[0]
        for elem in data:
            if elem == first_elem:
                self.x.append(elem[0])
                self.y.append(elem[1])
            else:
                self.new_record(elem)

    def new_record(self, queue_record) -> None:
        record = []
        while not queue_record.empty():
            elem = queue_record.get()
            record.append(elem)

        if len(record) != 2:
            raise ValueError("Argument list `record` must have length 2")

        new_x, new_y = record
        if self.y[-1] == new_y:
            self.x.append(new_x)
            self.y.append(new_y)
        else:
            for _ in range(2):
                self.x.append(new_x)
            self.y.append(self.y[-1])
            self.y.append(new_y)

    def plot(self) -> None:
        plot(self.x, self.y)

    def show(self, record= None) -> None:
        if record is None:
            self.plot()
            show()
        else:
            self.new_record(record)
            show()


if __name__ == '__main__':
    n = 10
    x = [i for i in range(n + 1)]
    y = [randint(0, 1) for _ in range(n + 1)]

    graph = DigitalGraph(list(zip(x, y)))
    graph.show()
