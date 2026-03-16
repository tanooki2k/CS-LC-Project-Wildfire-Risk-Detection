#!/usr/bin/env python3

import argparse
from argparse import Namespace
from Tools.SerialReader import SerialReader
from DataBases.DataManagerCSV import DataManagerCSV, process_data
from Grapher.MultiAxesGraph import MultiAxesGraph
from Tools.DataSetReader import read_dataset


def main():
    parser = argparse.ArgumentParser(
        description="Program that calculates the Wildfire risk."
    )

    parser.add_argument(
        "-m", "--mode",
        choices=["realtime", "simulation"],
        default="realtime",
        required=False,
        help="Select the mode (realtime or simulation)"
    )

    parser.add_argument(
        "-tu", "--time_units",
        choices=["hours", "minutes", "seconds"],
        default="seconds",
        required=False,
        help="Select the time units for interval and savefig (hours, minutes or seconds) (default: hours)"
    )

    parser.add_argument(
        "-d", "--dataset",
        type=str,
        help="Dataset file used in simulation mode"
    )

    parser.add_argument(
        "-i", "--interval",
        type=float,
        default=30,
        help="Sampling interval in hours (default: 24)"
    )

    parser.add_argument(
        "-s", "--savefig",
        type=float,
        required=False,
        help="Saving graph image in hours (default: 24)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    if args.mode == "simulation" and args.dataset is None:
        parser.error("--dataset is required when mode is 'simulation'")

    if args.verbose:
        print("Verbose mode enabled")
        print(f"Current mode is {args.mode}")

    if args.mode == "realtime":
        start_realtime_mode(args)
    else:
        start_simulation_mode(args)


def seconds_convertor(val: int, unit: str) -> float:
    if unit == "seconds":
        return val
    elif unit == "minutes":
        return val * 60
    else:
        return val * 3600


def start_realtime_mode(args: Namespace):
    fieldnames = ["utc", "temperature", "moisture", "risk"]
    is_digital = [None, False, True, False]

    serial_period = seconds_convertor(args.interval, args.time_units)
    graph_period = None
    if args.savefig:
        graph_period = seconds_convertor(args.savefig, args.time_units)

    if args.verbose:
        print(f"Generating one record per {serial_period} seconds")
        if graph_period:
            print(f"Generating one image per {graph_period} seconds")
        else:
            print("No graphs will be printed")

    try:
        serial_reader = SerialReader(serial_period=serial_period, graph_period=graph_period, fieldnames=list(zip(fieldnames, is_digital)),
                                     expr=r"^[0-9]+,[0-9]+$", verbose=args.verbose)
    except ValueError:
        print("The embedded system (micro:bit) has not been connected.")
    else:
        print("The program has been initialised as RealTime mode. Press CTRL+C to quit.")
        if args.verbose:    print("Database is being initialised...")
        database = DataManagerCSV(path="data.csv", fieldnames=fieldnames, verbose=args.verbose)

        print("Reading database previous records...")
        read_data = database.read()
        data = None
        if len(read_data):
            print("Processing data...")
            data = process_data(read_data=read_data, is_digital=is_digital)

        if args.verbose:    print("Grapher is being initialised...")
        grapher = MultiAxesGraph(fieldnames=fieldnames, data=data, verbose=args.verbose, title="Real Time data")

        serial_reader.attach(observer=database)
        serial_reader.attach(observer=grapher)

        serial_reader.attach_graph(graph_observer=grapher)

        # grapher.show(can_save=True, path="Output")
        serial_reader.read()


def start_simulation_mode(args: Namespace):
    print("The program has been initialised as Simulation mode.")
    print(f"Reading data from: {args.dataset}")
    try:
        read_dataset(path=args.dataset, is_digital=[None, False, True, False], verbose=args.verbose)
    except FileNotFoundError:
        print("Your file has not been found, please, make sure that it exists!")
    except ValueError:
        print("Your file is empty, please, fill anything!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
    print("Program finished!")
