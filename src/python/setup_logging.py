"""
Module for configuring and setting up logging.
"""

import json
import logging
import logging.config
import os
from typing import Optional


def setup_logging(
    config_file: str = "file_logging_config.json",
    logger_name: str = __name__,
    handler_name: str = "file",
    output_log_path: Optional[str] = None,
) -> logging.Logger:
    """
    Load and apply logging configuration from a JSON configuration file.

    Parameters
    ----------
    config_file: `str`
        Path to the logging configuration file.
    logger_name: `str`
        Name of the logger.
    handler_name: `str`
        Name of the handler.
    output_log_path: `Optional[str]`
        Path to the output log file.

    Returns
    ----------
    logger: `logging.Logger`
        The configured logger.
    """

    # Set up temporary logging configuration with formatted output
    logging.basicConfig(
        level=logging.WARNING,
        format="%(levelname)-8s: %(message)s",
    )

    # Create a temporary logger object for logging errors during the setup process
    temp_logger = logging.getLogger("temporary_logger")

    try:
        # Attempt to open and read the JSON configuration file
        with open(config_file, "r", encoding="utf-8") as file:
            # Load the JSON file content into a dictionary
            config_dict = json.load(file)

            # Dynamically adjust the handler's file path (if output_log_path is provided)
            if output_log_path:
                config_dict["handlers"][handler_name]["filename"] = output_log_path

            # Attempt to retrieve the log file path from the specified handler in the configuration
            log_path = (
                config_dict.get("handlers", {})
                .get(handler_name, {})
                .get("filename", None)
            )

            # Check if a log path is specified
            if log_path:

                # Extract the directory part of the log file path
                log_dir = os.path.dirname(log_path)

                # Check if the directory does not exist
                if not os.path.exists(log_dir):

                    # Create the directory and any necessary parent directories if they don't exist
                    os.makedirs(log_dir, exist_ok=True)

            # If all steps are successful, apply the logging configuration read from the JSON file
            logging.config.dictConfig(config_dict)

            # Retrieve and return the configured logger object
            logger = logging.getLogger(logger_name)
            return logger

    # Catch errors that might occur during file opening or reading
    except (PermissionError, FileNotFoundError, json.JSONDecodeError) as file_error:
        # Use the temporary logger to log the error message for debugging and troubleshooting
        temp_logger.error("File error occurred: %s", file_error)
        raise

    # Catch errors that might occur during the configuration process
    except (ValueError, KeyError) as config_error:
        # Use the temporary logger to log the error message
        temp_logger.error("Configuration error occurred: %s", config_error)
        raise

    # Catch any other unforeseen exceptions
    except Exception as unexpected_error:
        # Use the temporary logger to log the error message
        temp_logger.error("Unexpected error occurred: %s", unexpected_error)
        raise
