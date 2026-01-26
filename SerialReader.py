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


    def process_data(self) -> None:
        while True:
            raw_record = self.raw_data.get()
            arrays = list(zip(*raw_record))
            process_record = [median(col) for col in arrays]
            self.processed_data.put()


    def read(self):
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
                    self.raw_data.put(raw_record)
                    print(raw_record)
                    raw_record = []


if __name__ == "__main__":
    serial = SerialReader(5, 1.5, r"^[0-9]+,[0-9]+$")
    serial.read()
