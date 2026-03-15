from statistics import median
from threading import Thread
from typing import List, Tuple
from queue import Queue
import datetime
import time
import re
import serial
import mb_detect


class SerialReader:
    raw_data = Queue()
    processed_data = Queue()

    def __init__(self, period: float, epsilon: float, fieldnames: List[Tuple[str, bool]], expr: str, verbose: bool = False):
        port = mb_detect.find()

        if port:
            self.serial = serial.Serial(port, 115200)
        else:
            raise ValueError("Serial port not found!")
        self.period = period
        self.epsilon = epsilon
        self.expr = expr
        self.__is_digital = [d for _, d in fieldnames]
        self.__fieldnames = [k for k, _ in fieldnames]
        self.__verb = verbose


    def process_data(self) -> None:
        while True:
            raw_record = self.raw_data.get()
            if raw_record:
                arrays = list(zip(*raw_record))

                now = datetime.datetime.now()
                formatted = now.strftime("%Y-%m-%d %H:%M:%S")
                if len(arrays) == len(self.__fieldnames) - 1:
                    process_record = [formatted] + [bool(median(col)) if self.__is_digital[i+1] else int(median(col)) for i, col in enumerate(arrays)]
                    final_record =  {key: value for key, value in zip(self.__fieldnames, process_record)}
                    self.processed_data.put(final_record)
                    data_str = ", ".join([f"{f}: {final_record[f]}" for f in self.__fieldnames])
                    print(f"Received record: {data_str}")


    def read(self, func):
        data_thread = Thread(target=self.process_data, daemon=True)
        database_thread = Thread(target=func, daemon=True)

        data_thread.start()
        database_thread.start()

        start_time = time.time()
        raw_record = []

        while True:
            line = self.serial.readline().decode(errors="ignore").strip()
            delta = (time.time() - start_time) % self.period
            if delta < self.epsilon or delta > self.period - self.epsilon:
                if re.search(self.expr, line):
                    data = [bool(int(num)) if self.__is_digital[i + 1] else int(num) for i, num in enumerate(line.split(","))]
                    raw_record.append(data)
            else:
                if raw_record:
                    if self.__verb: print(f"Raw Input read: {raw_record}")
                    print(f"Raw data length: {len(raw_record)}")
                    self.raw_data.put(raw_record)
                    raw_record = []


if __name__ == "__main__":
    serial = SerialReader(10, 4, [("utc", False), ("temp", False), ("moist", True)], r"^[0-9]+,[0-9]+$")
    serial.read(lambda : None)
