"""
Utility code for xapi-db-load.
"""
import json
import logging
import os
from datetime import datetime

from aspects.xapi_db_load.backends import clickhouse_lake as clickhouse
from aspects.xapi_db_load.backends import csv
from aspects.xapi_db_load.backends import ralph_lrs as ralph

timing = logging.getLogger("timing")


class ConfigurationError(Exception):
    """
    Exception raised by backends when a configuration file is invalid.
    """


def get_backend_from_config(config):
    """
    Return an instantiated backend from the given config dict.
    """
    backend = config["backend"]
    if backend == "clickhouse":
        lake = clickhouse.XAPILakeClickhouse(config)
    elif backend == "ralph_clickhouse":
        lake = ralph.XAPILRSRalphClickhouse(config)
    elif backend == "csv_file":
        lake = csv.XAPILakeCSV(config)
    else:
        raise NotImplementedError(f"Unknown backend {backend}.")

    return lake


def setup_timing(log_dir):
    """
    Set up the timing logger.

    This should probably take an optional logging config file eventually.
    """
    formatter = logging.Formatter('%(message)s')

    if log_dir:
        timing_log_name = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_timing.log")
        print(f"Logging timing data to {timing_log_name}")
        handler = logging.FileHandler(timing_log_name)
    else:
        print("No log dir provided, logging timing data to stdout.")
        handler = logging.StreamHandler()

    handler.setFormatter(formatter)
    timing.addHandler(handler)
    timing.setLevel(logging.INFO)


class LogTimer:
    """
    Class to time and log our various operations.
    """

    start_time = None

    def __init__(self, timer_type, timer_key):
        self.timer_type = timer_type
        self.timer_key = timer_key

    def __enter__(self):
        self.start_time = datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        log_duration(
            self.timer_type,
            self.timer_key,
            (datetime.now() - self.start_time).total_seconds()
        )


def log_duration(timer_type, timer_key, duration):
    """
    Log timing data to the configured logger.

    timer_type: Top level type of the timer ("query", "batch_load", "setup"...)
    timer_key: Specific timer ("Count of Users", "Batch 100", "init"...)
    duration: Timing in fractional seconds (1.20, 12.345, 0.03)
    """
    stmt = {'time': datetime.now().isoformat(), 'timer': timer_type, 'key': timer_key, 'duration': duration}
    timing.info(json.dumps(stmt))
