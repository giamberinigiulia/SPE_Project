"""
SPE Project Argument Parser Module.

This module provides functionality for parsing command-line arguments to configure the system settings.
It supports two modes of execution:
1. JSON mode: Reads configuration from a JSON file.
2. Run mode: Accepts configuration parameters directly from the command line.

Classes:
- `Config`: A dataclass that encapsulates system configuration parameters.

Functions:
- `create_parser()`: Creates and returns an ArgumentParser instance with subparsers for different modes.
- `_add_arguments_subparser(subparser, command_name)`: Adds specific arguments to a subparser based on the mode.
- `parse_arguments(parser)`: Parses the command-line arguments and returns a `Config` object.

Usage:
Import this module to parse arguments and retrieve system configuration.

Example:
    parser = create_parser()
    config = parse_arguments(parser)
"""

from argparse import ArgumentParser
from dataclasses import dataclass

import spe.json_config_manager as manager

# maybe is possible to move this class in another module
@dataclass
class Config:
    service_rate: float
    arrival_rate: float
    user_range: range
    user_request_time: int
    number_of_servers: int


def create_parser() -> ArgumentParser:
    global_parser = ArgumentParser(prog="main", description="Simulate a M/M/1 Queue System")
    subparsers = global_parser.add_subparsers(title="modes of execution", dest="mode")

    json_parser = subparsers.add_parser("json", help="Json Parser mode: main.py json -f <json_file_path>")
    _add_arguments_subparser(json_parser, "json")

    run_parser = subparsers.add_parser(
        "run", help="Default mode: main.py run -s <service_rate> -a <arrival_rate> -t <time> -u <user_range> -k <number_of_servers>")
    _add_arguments_subparser(run_parser, "run")

    return global_parser


def _add_arguments_subparser(subparser: ArgumentParser, command_name: str) -> None:
    if command_name == "json":
        subparser.add_argument("-f", type=str, required=True, help="Path of config.json")
    else:
        subparser.add_argument('-s', type=float, required=True, help='Parameter service rate')
        subparser.add_argument('-a', type=float, required=True, help='Parameter arrival rate')
        subparser.add_argument('-u', type=int, nargs=2, required=True, help='Range of users')
        subparser.add_argument('-t', type=int, required=True, help='Maximum time to run the simulation')
        subparser.add_argument('-k', type=int, required=True, help='Number of servers')


def parse_arguments(parser: ArgumentParser) -> Config:
    args = parser.parse_args()

    if args.mode == "json":
        service_rate, arrival_rate, user_range, user_request_time = manager.read_json(args.c)
    else:
        service_rate = args.s
        arrival_rate = args.a
        user_range = range(args.u[0], args.u[1] + 1)
        user_request_time = args.t
        number_of_servers = args.k

    return Config(service_rate, arrival_rate, user_range, user_request_time, number_of_servers)
