import os
from typing import Tuple
from datetime import datetime
from random import randint
from matplotlib.pyplot import plot, show, savefig
from Grapher.Graphing import MatplotlibGraph


class DigitalGraph(MatplotlibGraph):
    x, y = [], []

    def __init__(self, fieldnames: Tuple[str, str], data = None) -> None:
        self.fieldnames = fieldnames

        while data is not None and not data.empty():
            row = data.get()
            record = []
            while not row.empty():
                elem = row.get()
                record.append(elem)

            if len(record) != 2:
                raise ValueError("All elements must be pairs `(x, y)`")

            self.new_record(record)

    def new_record(self, record) -> None:
        if len(record) != 2:
            raise ValueError("Argument list `record` must have length 2")

        if len(self.x) == len(self.y) == 0:
            self.x.append(record[0])
            self.y.append(record[1])
            return

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

    def show(self, record=None, can_save: bool = False) -> None:
        if record is not None:
            self.new_record(record)

        self.plot()

        if can_save:
            output_path = os.path.join("..", "Output")
            self.save(output_path)
        show()

    @staticmethod
    def save(path, ext="png"):
        now = datetime.now()
        formatted = now.strftime("%Y%m%d_%H%M%S")

        output_path = os.path.join(path, formatted + ext)
        savefig(output_path)


if __name__ == '__main__':
    from queue import Queue

    data_queue = Queue()

    n = 10
    x_col = [i for i in range(n + 1)]
    y_col = [bool(randint(0, 1)) for _ in range(n + 1)]

    for i in range(n + 1):
        new_queue = Queue()
        new_queue.put(x_col[i])
        new_queue.put(y_col[i])

        data_queue.put(new_queue)

    graph = DigitalGraph(data=data_queue, fieldnames=("x", "y"))
    graph.show(can_save=True)
