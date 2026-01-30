import time
from typing import List, Dict, Tuple
from DataManagerCSV import DataManagerCSV
from AnalogGraph import AnalogGraph
from DigitalGraph import DigitalGraph
from random import randint


class DataCollector:
    def __init__(self, filename: str, fieldnames: List[str], pairs_fieldnames: List[Tuple[str, str]], data_type = None):
        if data_type is None or data_type.lower() not in ["digital", "analog"]:
            raise ValueError("Data type must be 'digital' or 'analog'")

        self.__start_time = time.time()

        self.__filename = filename
        self.__fieldnames = fieldnames
        self.__database = DataManagerCSV(filename, fieldnames)
        self.__grapher = []

        raw_data = self.__database.read()
        print(raw_data)
        data = self.__converter(raw_data)
        if data_type == "digital":
            self.__grapher = DigitalGraph(data) if data else DigitalGraph()
        elif data_type == "analog":
            self.__grapher = AnalogGraph(data) if data else AnalogGraph()

    def read(self):
        return self.__database.read()

    def plot(self, period: float) -> None:
        delta = time.time() - self.__start_time
        if delta >= period:
            self.__grapher.show()
            self.__start_time = time.time()

    def new_record(self, *record: Dict[str, str]) -> None:
        valid_records = self.__database.write(*record, validate=True)

        for r in valid_records:
            self.__grapher.new_record(r)

    @staticmethod
    def __converter(data) -> Dict[str, str]:
        pass

if __name__ == "__main__":
    numbers_data = DataCollector("data", ["t", "x", "y"], [("t", "x"), ("t", "y"), ("x", "y")], "analog")
    length = len(numbers_data.read())
    numbers_data.plot(0)

    new_data = [
        {"t": length + i, "x": 2 * (length + i + 1) + 1, "y": 2 * (length + i + 1) + randint(-10, 10)} for i in range(randint(5, 20))
    ]
    numbers_data.new_record(*new_data)
    numbers_data.plot(0)
