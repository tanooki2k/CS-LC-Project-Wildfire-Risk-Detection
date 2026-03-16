#!/usr/bin/env python3

import argparse
from serial.serialutil import SerialException
from Tools.SerialReader import SerialReader
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
        "-d", "--dataset",
        type=str,
        help="Dataset file used in simulation mode"
    )

    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=24,
        help="Sampling interval in hours (default: 24)"
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


    print(f"Sampling interval: {args.interval} hours")

    if args.mode == "realtime":
        try:
            serial_reader = SerialReader(10, 4, [("utc", False), ("temp", False), ("moist", True)], r"^[0-9]+,[0-9]+$", args.verbose)
        except ValueError:
            print("The embedded system (micro:bit) has not been connected.")
        else:
            print("The program has been initialised as RealTime mode. Press CTRL+C to quit.")
            serial_reader.read(lambda: None)
    else:
        print("The program has been initialised as Simulation mode.")
        print(f"Reading data from: {args.dataset}")
        try:
            read_dataset(args.dataset, [None, False, True, False], args.verbose)
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
