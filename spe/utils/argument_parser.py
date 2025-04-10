"""This module provides functionality for parsing command-line arguments to configure the system settings."""
from argparse import ArgumentParser
from dataclasses import dataclass


@dataclass
class Config:
    service_rate: float
    arrival_rate: float
    user_range: range
    user_request_time: int
    number_of_servers: int


def create_parser() -> ArgumentParser:
    """
    Create and configure the command line argument parser.

    Returns:
        ArgumentParser: Configured parser object
    """
    global_parser = ArgumentParser(prog="main", description="Simulate a M/M/c Queue System")
    subparsers = global_parser.add_subparsers(title="modes of execution", dest="mode")
    run_parser = subparsers.add_parser(
        "run", help="Default mode: main.py run -s <service_rate> -a <arrival_rate> -t <time> -u <user_range> -k <number_of_servers>")
    _add_arguments_to_run_parser(run_parser)

    return global_parser


def _add_arguments_to_run_parser(subparser: ArgumentParser) -> None:
    subparser.add_argument('-s', type=float, required=True, help='Parameter service rate')
    subparser.add_argument('-a', type=float, required=True, help='Parameter arrival rate')
    subparser.add_argument('-u', type=int, nargs=2, required=True, help='Range of users')
    subparser.add_argument('-t', type=int, required=True, help='Maximum time to run the simulation')
    subparser.add_argument('-k', type=int, required=True, help='Number of servers')


def parse_arguments(parser: ArgumentParser) -> Config:
    """
    Parse command-line arguments and create a configuration object.

    Args:
        parser: Configured argument parser

    Returns:
        Config: Configuration object with parsed values
    """
    args = parser.parse_args()

    return Config(service_rate=args.s, arrival_rate=args.a, user_range=range(args.u[0], args.u[1] + 1), user_request_time=args.t, number_of_servers=args.k)
