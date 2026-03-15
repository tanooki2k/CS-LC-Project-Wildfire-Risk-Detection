import time
from typing import List, Dict, Tuple
from DataManagerCSV import DataManagerCSV
from AnalogGraph import AnalogGraph
from DigitalGraph import DigitalGraph
from data_convertor import convert_data
from random import randint


class DataCollector:
    def __init__(self, filename: str, fieldnames: List[str], pairs_fieldnames: List[Tuple[str, str]]):
        self.__start_time = time.time()

        self.__filename = filename
        self.__fieldnames = fieldnames
        self.__database = DataManagerCSV(filename, fieldnames)

        raw_data = self.__database.read()
        data = convert_data(raw_data, pairs_fieldnames)
        self.__grapher = [
            AnalogGraph(fieldnames=pairs_fieldnames[0], data=data[0]),
            DigitalGraph(fieldnames=pairs_fieldnames[1], data=data[1])
        ]

    def read(self):
        return self.__database.read()

    def plot(self, period: float) -> None:
        delta = time.time() - self.__start_time
        if delta >= period:
            for g in self.__grapher:
                g.show()
            self.__start_time = time.time()

    def new_record(self, *record: Dict[str, str]) -> None:
        self.__database.write(*record, validate=False)

        for r in record:
            for g in self.__grapher:
                new_record = [r[k] for k in g.fieldnames]
                g.new_record(new_record)


if __name__ == "__main__":
    numbers_data = DataCollector("data", ["t", "x", "y"], [("t", "x"), ("t", "y")])
    length = len(numbers_data.read())
    numbers_data.plot(0)

    new_data = [
        {"t": length + i, "x": 2 * (length + i + 1) + 1, "y": 2 * (length + i + 1) + randint(-10, 10)} for i in range(randint(5, 20))
    ]
    numbers_data.new_record(*new_data)
    numbers_data.plot(0)
