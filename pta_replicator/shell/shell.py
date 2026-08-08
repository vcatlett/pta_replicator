import argparse
from pathlib import Path

from rich.console import Console
from rich.table import Table

from pta_replicator import version
from pta_replicator.util.config import Config
from pta_replicator.util.envtools import get_package_version

config = Config()


def newlines(n=1):
    for i in range(n):
        print("\n")


def welcome_banner():
    newlines(2)
    session_table = make_session_table()
    package_table = make_package_table()
    console = Console()
    console.print(session_table)
    newlines(2)
    console.print(package_table)


def make_session_table():
    # Init table
    table = Table(title=f"PTA Replicator {version()} Session Configuration")

    # Header of table
    table.add_column("Key", justify="right", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    # Rows of table
    table.add_row("Username", config.USERNAME)
    table.add_row("Host", config.HOSTNAME)
    table.add_row("Data", config.env["DATA_15YR_ROOT"])

    return table


def make_package_table():
    # Init table
    table = Table(title=f"Packages in current environment")

    # Header of table
    table.add_column("Package", justify="center", style="cyan", no_wrap=True)
    table.add_column("Version", justify="center", style="green")

    # Rows of table
    table.add_row("Enterprise", get_package_version("enterprise-pulsar"))
    table.add_row("Discovery", get_package_version("discovery"))
    table.add_row("PINT", get_package_version("pint-pulsar"))

    return table


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            f"""
            PTA Replicator Launcher
            All CLI arguments other than those defined below are passed through to iPython.
            See $ ipython --help for more details
            """
        )
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        help="Set logging verbosity",
        type=int,
        default=2,
        choices=[0, 1, 2, 3],
    )
    parser.add_argument("--log", help="Specify log path", type=Path)
    parser.add_argument(
        "-q",
        "--quiet",
        help="Silence DEBUG- and INFO-level logs to stderr",
        action="store_true",
    )
    return parser.parse_known_args()


def main():
    # args, remaining_args = parse_args()
    # init_logging(verbosity=args.verbosity, path=args.log, quiet=args.quiet)
    welcome_banner()


if __name__ == "__main__":
    main()
