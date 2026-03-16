from statistics import median
from threading import Thread
from typing import List, Tuple, Dict, Any
from queue import Queue
import datetime
import time
import re
import serial
import mb_detect
from Model.wildfire_risk import calculate_wildfire_risk
from Tools.ObserverDesignPattern import Subject, Observer, GraphObserver


class SerialReader(Subject):
    raw_data = Queue()
    _observers: List[Observer] = []
    _graph_observers: List[GraphObserver] = []

    def __init__(self, serial_period: float, fieldnames: List[Tuple[str, bool]], expr: str, verbose: bool = False, graph_period: float = None):
        port = mb_detect.find()

        if port:
            self.serial = serial.Serial(port, 115200)
        else:
            raise ValueError("Serial port not found!")
        self.serial_period = serial_period
        self.graph_period = graph_period
        self.expr = expr
        self.__is_digital = [d for _, d in fieldnames]
        self.__fieldnames = [k for k, _ in fieldnames]
        self.__verbose = verbose

    def attach(self, observer: Observer):
        if self.__verbose: print("SerialReader has attached a new observer!")
        self._observers.append(observer)

    def notify(self, new_record: Dict[str, Any]):
        if self.__verbose: print("Updating with the new record!")
        for observer in self._observers:
            observer.update(new_record)

    def attach_graph(self, graph_observer: GraphObserver):
        if self.__verbose: print("SerialReader has attached a new graph observer!")
        self._graph_observers.append(graph_observer)

    def notify_graph(self):
        if self.__verbose: print("Saving current image!")
        for graph_observer in self._graph_observers:
            graph_observer.show(can_save=True, path="Output")

    def process_raw_data(self) -> None:
        start_time = time.time()

        while True:
            raw_record = self.raw_data.get()
            if raw_record:
                arrays = list(zip(*raw_record))

                now = datetime.datetime.now()
                formatted = now.strftime("%Y-%m-%d %H:%M:%S")
                if len(arrays) == len(self.__fieldnames) - 2:
                    process_record = [formatted] + [bool(median(col)) if self.__is_digital[i+1] else int(median(col)) for i, col in enumerate(arrays)]
                    risk_level, risk_perc = calculate_wildfire_risk(temp=process_record[1], moist=process_record[2])
                    process_record.append(int(risk_perc))

                    final_record =  {key: value for key, value in zip(self.__fieldnames, process_record)}
                    data_str = ", ".join([f"{f}: {final_record[f]}" for f in self.__fieldnames])
                    print(f"Received record: {data_str}")
                    print(f"There is a {risk_level} wildfire risk ({int(risk_perc)}%)")
                    self.notify(final_record)

            if self.graph_period is None:
                continue
            delta = time.time() - start_time
            if delta > self.graph_period:
                self.notify_graph()
                start_time = time.time()


    def read(self):
        data_thread = Thread(target=self.process_raw_data, daemon=True)
        data_thread.start()

        start_time = time.time()
        raw_record = []

        while True:
            line = self.serial.readline().decode(errors="ignore").strip()
            delta = (time.time() - start_time) % self.serial_period
            if delta < self.serial_epsilon or delta > self.serial_period - self.serial_epsilon:
                if re.search(self.expr, line):
                    data = [bool(int(num)) if self.__is_digital[i + 1] else int(num) for i, num in enumerate(line.split(","))]
                    raw_record.append(data)
            else:
                if raw_record:
                    if self.__verbose:
                        print(f"Raw Input read: {raw_record}")
                        print(f"Raw data length: {len(raw_record)}")
                    self.raw_data.put(raw_record)
                    raw_record = []


if __name__ == "__main__":
    serial = SerialReader(10, [("utc", False), ("temp", False), ("moist", True), ("risk", False)], r"^[0-9]+,[0-9]+$")
    serial.read()
