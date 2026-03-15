from pathlib import Path
from datetime import datetime
from typing import Tuple
from matplotlib.pyplot import plot, show, savefig
from Grapher.Graphing import MatplotlibGraph


class AnalogGraph(MatplotlibGraph):
    x, y = [], []

    def __init__(self, fieldnames: Tuple[str, str], data=None) -> None:
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

        new_x, new_y = record
        self.x.append(new_x)
        self.y.append(new_y)

    def plot(self) -> None:
        plot(self.x, self.y)

    def show(self, record=None, can_save: bool = False) -> None:
        if record is not None:
            self.new_record(record)

        self.plot()

        if can_save:
            output_dir = Path("..") / "Output"
            output_dir.mkdir(parents=True, exist_ok=True)

            self.save(output_dir)
        show()

    @staticmethod
    def save(path):
        now = datetime.now()
        formatted = now.strftime("%Y%m%d_%H%M%S")

        output_path = path / formatted
        savefig(output_path)


if __name__ == '__main__':
    from Tools.FloatRange import float_range
    from queue import Queue
    from math import sin

    data_queue = Queue()

    t = [num for num in float_range(-10, 10, 0.001)]
    func_x = lambda x: sin(x)
    func_y = lambda y: y ** 2

    x_col = [func_x(i) for i in t]
    y_col = [func_y(j) for j in t]

    for i in range(len(t)):
        new_queue = Queue()
        new_queue.put(x_col[i])
        new_queue.put(y_col[i])

        data_queue.put(new_queue)

    graph = AnalogGraph(data=data_queue, fieldnames=("x", "y"))
    graph.show(can_save=True)
