import argparse
from typing import Tuple

import json_config_manager as manager


def add_arguments_subparser(subparser: argparse.ArgumentParser, command_name: str) -> None:
    if command_name == "json":
        subparser.add_argument("-f", type=str, required=True, help="Path of config.json")
    else:
        subparser.add_argument('-s', type=float, required=True, help='Parameter service rate')
        subparser.add_argument('-a', type=float, required=True, help='Parameter arrival rate')
        subparser.add_argument('-u', type=int, nargs=2, required=True, help='Range of users')
        subparser.add_argument('-t', type=int, required=True, help='Maximum time to run the simulation')


def create_parser() -> None:
    global_parser = argparse.ArgumentParser(prog="main", description="Simulate a M/M/1 Queue System")
    subparsers = global_parser.add_subparsers(title="modes of execution", dest="mode")

    json_parser = subparsers.add_parser("json", help="Json Parser mode: main.py json -f <json_file_path>")
    add_arguments_subparser(json_parser, "json")

    run_parser = subparsers.add_parser(
        "run", help="Default mode: main.py run -s <service_rate> -a <arrival_rate> -t <time> -u <user_range>")
    add_arguments_subparser(run_parser, "run")

    return global_parser


def parse_arguments(parser: argparse.ArgumentParser) -> Tuple[float, float, range, int]:
    args = parser.parse_args()

    if args.mode == "json":
        service_rate, arrival_rate, user_range, user_request_time = manager.read_json(args.c)
    else:
        service_rate = args.s
        arrival_rate = args.a
        user_range = range(args.u[0], args.u[1] + 1)
        user_request_time = args.t

    return service_rate, arrival_rate, user_range, user_request_time
