

import time
from notifications import show_notification


class Timer:
    def __init__(
        self,
        duration_seconds: int,
        message: str,
        verbose: bool = False,
        silent: bool = False
        ):
        self.duration_seconds = duration_seconds
        self.message = message
        self.verbose = verbose
        self.silent = silent

    def start(self):
        """Start the timer and run it until completion or interruption"""
        start_time = time.time()

        try:
            while True:
                elapsed = time.time() - start_time
                remaining = self.duration_seconds - elapsed
                if remaining <= 0:
                    break

                # Show progress if verbose
                if self.verbose and not self.silent:
                    self._display_progress(remaining)

                # Sleep for appropriate interval
                sleep_duration = min(1.0, remaining) # Sleep 1 second or remaing time
                time.sleep(sleep_duration)

        except KeyboardInterrupt:
            if not self.silent:
                print(f"\nTimer cancelled after {elapsed:.2f} seconds.")
            raise # Re-raise to be handled by main()

        # Timer completed successfully
        if not self.silent:
            print(f"\nTimer completed! {self.duration_seconds} seconds.")

        # Show desktop notification
        show_notification(self.message)

    def _display_progress(self, remaining_seconds):
        """Display the remaining time in a human-readable format"""
        minutes, seconds = divmod(int(remaining_seconds), 60)
        hours, minutes = divmod(minutes, 60)

        if hours > 0:
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            time_str = f"{minutes:02d}:{seconds:02d}"

        # Use \r to overwrite the same line
        print(f"\rTime remaining: {time_str}", end="", flush=True)
