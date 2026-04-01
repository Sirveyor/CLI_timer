# c:/Users/Covert/DEV/CLI_timer/main.py

"""
CLI Timer - A command-line timer with desktop notifications

Supports both relative durations (5m, 1h30m, 90s) and absolute times (3:30 PM, 15:30).
Displays desktop popup notifications when timers expire.
"""

import argparse
import sys
from typing import Optional

# Local imports (will be implemented in later steps)
from time_parser import parse_time_input
from timer_core import Timer
from notifications import show_notification


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="timer",
        description="CLI timer with desktop notifications",
        epilog="Examples:\n"
        "  timer 5m                   # 5 minute timer\n"
        "  timer 1h30m                # 1 hour 30 minute timer\n"
        "  timer 90s                  # 90 second timer\n"
        "  timer 15:30                # Timer until 3:30 PM (24h format)\n"
        '  timer "3:30 PM"            # Timer until 3:30 PM (12h format)\n'
        '  timer 10m "Take a break!"  # Custom notification message',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "time",
        help='Time specification: relative (5m, 1h30m, 90s) or absolute (15:30, "3:30 PM")',
    )

    parser.add_argument(
        "message",
        nargs="?",
        default="Timer finished!",
        help='Custom notification message (default: "Timer finished!")',
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show verbose output during timer execution",
    )

    parser.add_argument(
        "--silent",
        "-s",
        action="store_true",
        help="Run timer silently (no progress updates)",
    )

    return parser


def main() -> int:
    """Main entry point for the CLI timer application."""
    parser = create_parser()
    args = parser.parse_args()

    # Validate arguments
    if args.verbose and args.silent:
        print("Error: --verbose and --silent cannot be used together", file=sys.stderr)
        return 1

    try:
        # Parse time input (to be implemented)
        duration_seconds = parse_time_input(args.time)

        if args.verbose:
            print(f"Starting timer for {duration_seconds} seconds...")
            print(f"Notification message: {args.message}")

        # Create and start timer (to be implemented)
        timer = Timer(
            duration_seconds=duration_seconds,
            message=args.message,
            verbose=args.verbose,
            silent=args.silent,
        )

        # Run the timer
        timer.start()

        return 0

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nTimer cancelled by user.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
