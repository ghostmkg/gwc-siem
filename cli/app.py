"""
GWC-SIEM CLI Application
Command-line tool for log processing and analysis
"""

import argparse
import sys
from typing import Optional


def main(args: Optional[list] = None):
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="GWC-SIEM Command Line Interface", prog="gwc-siem"
    )

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    parser.add_argument("--file", type=str, help="Log file to process")

    parser.add_argument(
        "--kind", type=str, choices=["auth", "nginx", "apache"], help="Type of log file"
    )

    parser.add_argument("--output", type=str, help="Output file for results")

    if args is None:
        args = sys.argv[1:]

    parsed_args = parser.parse_args(args)

    if parsed_args.file and parsed_args.kind:
        print(f"Processing {parsed_args.kind} log file: {parsed_args.file}")
        # TODO: Implement actual log processing
        return 0
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
