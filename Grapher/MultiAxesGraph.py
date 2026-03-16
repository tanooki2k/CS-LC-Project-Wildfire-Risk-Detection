from typing import Dict, List, Any
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
from Grapher.Graphing import MatplotlibGraph


class MultiAxesGraph(MatplotlibGraph):
    time, temp, moist, risk = [], [], [], []
    __TIME_TAG = "Time (hours)"
    __TEMP_TAG = "Temperature (°C)"
    __RISK_TAG = "Risk (0% - 100%)"
    __min_temp_ax, __max_temp_ax = 10, 40

    def __init__(self, fieldnames: List[str], data: List[Dict[str, Any]] = None) -> None:
        if len(fieldnames) != 4:
            raise AttributeError(f"Fieldnames must have 4 element, just {len(fieldnames)} has been provided.")

        self.fig, self.ax1 = plt.subplots()
        self.ax2 = self.ax1.twinx()
        self.fieldnames = fieldnames

        self.ax1.set_ylim(self.__min_temp_ax - 2.5, self.__max_temp_ax + 2.5)
        self.ax2.set_ylim(-2.5, 102.5)

        self.ax1.set_xlabel(self.__TIME_TAG)
        self.ax1.set_ylabel(self.__TEMP_TAG)
        self.ax2.set_ylabel(self.__RISK_TAG)

        for record in data:
            self.new_record(record)

    def adjust_temp_axis(self, new_temp):
        if new_temp > self.__max_temp_ax:
            self.__max_temp_ax = new_temp
        elif new_temp < self.__min_temp_ax:
            self.__min_temp_ax = new_temp

    def new_record(self, record):
        if len(record) != 4:
            raise ValueError("Argument list `record` must have length 4")

        new_time, new_temp, new_moist, new_risk = record.values()
        self.adjust_temp_axis(new_temp)

        self.time.append(new_time)
        self.temp.append(new_temp)
        self.moist.append(new_moist)
        self.risk.append(new_risk)

    def plot(self):
        self.ax1.set_ylim(self.__min_temp_ax - 2.5, self.__max_temp_ax + 2.5)

        temp_line, = self.ax1.plot(self.time, self.temp, label=self.__TEMP_TAG, color="orange")
        risk_line, = self.ax2.plot(self.time, self.risk, label=self.__RISK_TAG, color="blue")

        time_true, time_false, temp_true, temp_false = [], [], [], []
        for i, m in enumerate(self.moist):
            if m:
                time_true.append(self.time[i])
                temp_true.append(self.temp[i])
            else:
                time_false.append(self.time[i])
                temp_false.append(self.temp[i])

        moist_false = self.ax1.scatter(
            time_false,
            temp_false,
            color="red",
            marker="x",
            label="Moisture = False"
        )

        moist_true = self.ax1.scatter(
            time_true,
            temp_true,
            color="green",
            marker="o",
            label="Moisture = True"
        )

        lines = [temp_line, risk_line, moist_false, moist_true]
        labels = [l.get_label() for l in lines]
        self.ax1.legend(lines, labels, loc="upper right")

    def show(self, record=None, can_save: bool = False, path:str =""):
        if record is not None:
            self.new_record(record)

        self.plot()

        if can_save:
            output_dir = Path(path)
            if not path:
                output_dir = Path("..") / "Output"
                output_dir.mkdir(parents=True, exist_ok=True)

            self.save(output_dir)
        else:
            plt.show()
        plt.close()

    @staticmethod
    def save(path):
        now = datetime.now()
        formatted = now.strftime("%Y%m%d_%H%M%S")

        output_path = path / formatted
        plt.savefig(output_path)


if __name__ == "__main__":
    import math

    hours = list(range(24))

    temperature = [20 + 8 * math.sin(i * 2 * math.pi / 23) for i in hours]
    risk = [50 + 30 * math.sin(i * 2 * math.pi / 23 + 0.8) for i in hours]

    moisture = [
        False, False, True, True, False, False,
        True, False, False, True, True, False,
        False, False, True, False, False, False,
        True, True, False, False, False, True
    ]

    raw_data = list(zip(hours, temperature, moisture, risk))

    field = ["utc", "temperature", "moisture", "risk"]
    dict_data = [{field[j]: raw_data[i][j] for j in range(len(field))} for i in hours]
    print(dict_data)

    graph = MultiAxesGraph(fieldnames=field, data=dict_data)
    graph.show(can_save=True)
