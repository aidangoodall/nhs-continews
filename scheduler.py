import schedule
import time
from typing import Callable
import threading

class Scheduler:
    def __init__(self):
        self.running = False
        self.thread = None

    def start_scheduler(self, fetch_function: Callable, frequency_minutes: int):
        """
        Start the scheduler to fetch data from API at specified intervals.

        Parameters:
        - fetch_function: The function to call for fetching data
        - frequency_minutes: How often to fetch data (in minutes)
        """
        if not isinstance(frequency_minutes, int) or frequency_minutes < 1 or frequency_minutes > 120:
            raise ValueError("Frequency must be an integer between 1 and 120 minutes")

        print(f"Scheduling data fetch every {frequency_minutes} minutes")
        schedule.every(frequency_minutes).minutes.do(fetch_function)

        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler)
        self.thread.start()

    def _run_scheduler(self):
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def stop_scheduler(self):
        """Stop the scheduler."""
        self.running = False
        if self.thread:
            self.thread.join()
        schedule.clear()
        print("Scheduler stopped.")

if __name__ == "__main__":
    # Example usage
    def dummy_fetch_function():
        print("Fetching data from Fitbit API...")
    
    scheduler = Scheduler()
    try:
        scheduler.start_scheduler(dummy_fetch_function, 1)
        # Simulate running for a while
        time.sleep(30)
        scheduler.stop_scheduler()
    except KeyboardInterrupt:
        scheduler.stop_scheduler()
        print("\nScheduler stopped due to keyboard interrupt.")

"""
TODO:
- Add function to set total schedule duration
- Test it in seconds
- What additions do we need to make to the requeiremnts doc?
"""