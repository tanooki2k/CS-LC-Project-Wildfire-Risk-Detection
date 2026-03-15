import os.path
from typing import List, Tuple, Dict, Union, Any
from csv import DictWriter, DictReader
from DataBases.FileManager import FileManager


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
    
    def write(self, *records: Dict[str, Any], validate: bool = True) -> Union[None, List[Tuple[int, int]]]:
        valid_data = []

        with open(self.__path, "a") as csv_file:
            writer = DictWriter(csv_file, fieldnames=self.__fieldnames)
            
            for r in records:
                if list(r.keys()) == self.__fieldnames:
                    if validate:
                        new_record = [r[k] for k in self.__fieldnames]
                        valid_data.append(new_record)
                    writer.writerow(r)

            if validate: return valid_data
            return None
    
    def delete(self):
        pass
    

if __name__ == "__main__":
    from datetime import datetime
    from random import randint

    database = DataManagerCSV("test", ["timestamp", "temperature", "moisture", "risk"])

    now = datetime.now()
    formatted = now.strftime("%Y-%m-%d %H:%M:%S")

    record = {"timestamp": formatted, "temperature": randint(10, 40), "moisture": randint(0, 1), "risk": randint(0, 100)}
    database.write(record)
    print(database.read())
    print(database)
