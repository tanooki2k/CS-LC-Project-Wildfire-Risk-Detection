from typing import List
from Grapher.MultiAxesGraph import MultiAxesGraph
from DataBases.DataManagerCSV import DataManagerCSV
from Tools.DatetimeFunctions import convert_to_date, convert_to_hours, subtract_date


def read_dataset(path: str, is_digital: List[bool], is_verbose: bool = False):
    with open(path) as file:
        fieldnames = [key.replace("\n", "") for key in file.readline().split(",")]

    print("Reading dataset...")
    collector = DataManagerCSV(
        path=path,
        fieldnames=fieldnames,
    )

    raw_data = collector.read()
    if is_verbose:
        print(*raw_data, sep="\n")

    if not raw_data:
        raise ValueError("No data has been found!")

    print("Processing data")
    first_date = convert_to_date(raw_data[0][fieldnames[0]])
    data = [
        {
            key: bool(float(val)) if is_digital[i] else int(float(val)) if is_digital[i] is not None else convert_to_hours(subtract_date(val, first_date))
            for i, (key, val) in enumerate(d.items())
        }
        for d in raw_data
    ]
    if is_verbose: print(*data, sep="\n")

    print("Initialising graph...")
    graph = MultiAxesGraph(
        fieldnames=fieldnames,
        data=data,
    )

    print("Plotting graph...")
    graph.show(can_save=True, path="Output")

    print("Graph successfully generated!")
    print("Look for it in the `Output` directory!")
