from typing import List, Dict
from DataManagerCSV import DataManagerCSV
from AnalogGraph import AnalogGraph
from DigitalGraph import DigitalGraph
from random import randint


class DataCollector:
    __converter = lambda _, dicts, value_fieldnames: [tuple([int(val) for key, val in elem.items() if key in value_fieldnames]) for elem in dicts]

    def __init__(self, filename: str, fieldnames: List[str], data_type = None):
        if data_type is None or data_type.lower() not in ["digital", "analog"]:
            raise ValueError("Data type must be 'digital' or 'analog'")

        self.__filename = filename
        self.__fieldnames = fieldnames
        self.__database = DataManagerCSV(filename, fieldnames)
        self.__grapher = []

        raw_data = self.__database.read()
        data = self.__converter(raw_data)
        if data_type == "digital":
            self.__grapher = DigitalGraph(data) if data else DigitalGraph()
        elif data_type == "analog":
            self.__grapher = AnalogGraph(data) if data else AnalogGraph()

    def read(self):
        return self.__database.read()

    def plot(self) -> None: 
        self.__grapher.show()

    def new_record(self, *record: Dict[str, str]) -> None:
        valid_records = self.__database.write(*record, validate=True)

        for r in valid_records:
            self.__grapher.new_record(r)


if __name__ == "__main__":
    numbers_data = DataCollector("data", ["x", "y"], "analog")
    length = len(numbers_data.read())
    numbers_data.plot()

    new_data = [
        {"x": 2 * (length + i + 1) + 1, "y": 2 * (length + i + 1) + randint(-10, 10)} for i in range(randint(5, 20))
    ]
    numbers_data.new_record(*new_data)
    numbers_data.plot()
