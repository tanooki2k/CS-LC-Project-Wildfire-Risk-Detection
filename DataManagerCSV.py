import os.path
from typing import List, Tuple, Dict, Union
from csv import DictWriter, DictReader
from FileManager import FileManager


class DataManagerCSV(FileManager):
    def __init__(self, path: str, fieldnames: List[str]):
        self.__path = path
        self.__fieldnames = fieldnames
        
        if not os.path.exists(path):
            self.create()
        else:
            fieldnames_stored = self.read_fieldnames()
            if fieldnames_stored != self.__fieldnames:
                raise ValueError(f"The fieldnames provided does not match with the CSV fieldnames!")
            
    def __repr__(self):
        return f"<DataManagerCSV path: `{self.__path}`, fieldnames:`{self.__fieldnames}`>"
    
    def create(self):
        with open(self.__path, "w") as csv_file:
            reader = DictWriter(csv_file, fieldnames=self.__fieldnames)
            reader.writeheader()
    
    def read(self):
        with open(self.__path) as csv_file:
            reader = DictReader(csv_file)
            data = list(reader)
        return data
    
    def read_fieldnames(self):
        with open(self.__path) as csv_file:
            reader = DictReader(csv_file)
            fieldnames = list(next(reader).keys())
        return fieldnames
    
    def write(self, *records: Dict[str, str], validate: bool = True) -> Union[None, List[Tuple[int, int]]]:
        valid_data = []

        with open(self.__path, "a") as csv_file:
            writer = DictWriter(csv_file, fieldnames=self.__fieldnames)
            
            for r in records:
                if list(r.keys()) == self.__fieldnames:
                    if validate: valid_data.append(list(r.values()))
                    writer.writerow(r)

            if validate: return valid_data
            return None
    
    def delete(self):
        pass
    

if __name__ == "__main__":
    database = DataManagerCSV("data", ["name", "age"])

    record = {"name": "Mateo", "age": 21}
    database.write(record)
    print(database.read())
    print(database)
