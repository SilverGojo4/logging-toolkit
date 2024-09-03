"""
Tests for the setup_logging function in the logging-toolkit.
"""

# Importing necessary modules and functions
import os
import sys

import pytest

# Define the base directory path and extend sys.path to include necessary directories
BASE_PATH = "/Users/silver/Logging-Toolkit"
sys.path.append(os.path.join(BASE_PATH, "src/python"))

# pylint: disable=wrong-import-position, import-error
from setup_logging import setup_logging


# Define the test function for setup_logging
def test_setup_logging():
    """
    Tests the setup_logging function for correct logger configuration and file output.
    """
    # Use test configuration files
    general_config_path = os.path.join(BASE_PATH, "src/python/general_logging.json")
    error_config_path = os.path.join(BASE_PATH, "src/python/error_logging.json")

    # Dynamically adjust the output log paths
    general_log_path = os.path.join(BASE_PATH, "logs/general.log")
    error_log_path = os.path.join(BASE_PATH, "logs/error.log")

    # Execute the setup_logging function to configure general_logger and error_logger
    general_logger = setup_logging(
        config_file=general_config_path,
        logger_name="general_logger",
        handler_name="general",
        output_log_path=general_log_path,
    )
    error_logger = setup_logging(
        config_file=error_config_path,
        logger_name="error_logger",
        handler_name="error",
        output_log_path=error_log_path,
    )

    # Test if general_logger is correctly configured
    assert general_logger is not None
    general_logger.debug("This is a DEBUG message.")
    general_logger.info("This is an INFO message.")
    general_logger.warning("This is a WARNING message.")
    general_logger.error("This is an ERROR message.")
    general_logger.critical("This is a CRITICAL message.")

    # Test if error_logger is correctly configured
    assert error_logger is not None
    error_logger.debug("This is a DEBUG message.")
    error_logger.info("This is an INFO message.")
    error_logger.warning("This is a WARNING message.")
    error_logger.error("This is an ERROR message.")
    error_logger.critical("This is a CRITICAL message.")

    # Check if log files are generated
    assert os.path.exists(general_log_path), f"File log not found: {general_log_path}"
    assert os.path.exists(error_log_path), f"Error log not found: {error_log_path}"

    # Clean up log files (optional)
    if os.path.exists(general_log_path):
        os.remove(general_log_path)
    if os.path.exists(error_log_path):
        os.remove(error_log_path)


# Run the test if this script is executed as the main program
if __name__ == "__main__":
    pytest.main()
