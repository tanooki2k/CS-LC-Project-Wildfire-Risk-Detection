from statistics import median
from threading import Thread
from typing import List
from queue import Queue
import time
import re
import serial
import mb_detect



class SerialReader:
    raw_data = Queue()
    processed_data = Queue()

    def __init__(self, period: float, epsilon: float, fieldnames: List[str], expr: str):
        port = mb_detect.find()

        if port:
            self.serial = serial.Serial(port, 115200)
        else:
            raise ValueError("Serial port not found!")
        self.period = period
        self.epsilon = epsilon
        self.expr = expr
        self.__fieldnames = fieldnames


    def process_data(self) -> None:
        while True:
            raw_record = self.raw_data.get()
            if raw_record:
                arrays = list(zip(*raw_record))

                if len(arrays) == len(self.__fieldnames) - 1:
                    process_record = [time.time()] + [median(col) for col in arrays]
                    final_record =  {key: value for key, value in zip(self.__fieldnames, process_record)}
                    self.processed_data.put(final_record)
                    print(final_record)


    def read(self, func):
        data_thread = Thread(target=self.process_data, daemon=True)
        database_thread = Thread(target=self.process_data, daemon=True)

        data_thread.start()
        database_thread.start()

        start_time = time.time()
        raw_record = []

        while True:
            line = self.serial.readline().decode().strip()
            delta = (time.time() - start_time) % self.period
            if delta < self.epsilon or delta > self.period - self.epsilon:
                if re.search(self.expr, line):
                    data = [float(num) for num in line.split(",")]
                    raw_record.append(data)
            else:
                if raw_record:
                    print(raw_record)
                    self.raw_data.put(raw_record)
                    raw_record = []


if __name__ == "__main__":
    serial = SerialReader(10, 4, ["utc", "temperature", "moisture"], r"^[0-9]+,[0-9]+$")
    serial.read(lambda : None)
