from typing import List, Tuple, Any
from matplotlib.pyplot import plot, show
from Graphing import MatplotlibGraph
from Tools.FloatRange import float_range


class AnalogGraph(MatplotlibGraph):
    x, y = [], []

    def __init__(self, data: List[Tuple[Any, Any]] = None) -> None:
        for elem in data:
            if len(elem) != 2:
                raise ValueError("All elements must be pairs `(x, y)`")

        for record in data:
            self.new_record(record)

    def new_record(self, queue_record) -> None:
        record = []
        while not queue_record.empty():
            elem = queue_record.get()
            record.append(elem)

        if len(record) != 2:
            raise ValueError("Argument list `record` must have length 2")

        new_x, new_y = record
        self.x.append(new_x)
        self.y.append(new_y)

    def plot(self) -> None:
        plot(self.x, self.y)

    def show(self, record= None) -> None:
        if record is None:
            self.plot()
            show()
        else:
            self.new_record(record)
            self.plot()
            show()


if __name__ == '__main__':
    from math import sin

    t = [num for num in float_range(-10, 10, 0.001)]
    func_x = lambda x: sin(x)
    func_y = lambda y: y ** 2

    x = [func_x(i) for i in t]
    y = [func_y(j) for j in t]

    graph = AnalogGraph(list(zip(x, y)))
    graph.show()
