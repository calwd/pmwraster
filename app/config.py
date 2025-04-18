"""
This module contains the application configuration
"""

import logging
import os
from pathlib import Path


class AppConfig:
    """
    This class holds the application configuration settings as well as a logger instance. The included logger is
    will need to be separated from this class in the future, but was included here for simplicity
    Attributes:
        raster_data_folder (Path): The path to the folder containing raster data.
        logger (logging.Logger): The logger instance for the application.
    """
    raster_data_folder: Path
    logger: logging.Logger
    application_name: str


def create_app_config() -> AppConfig:
    """
    Create the application configuration.
    Returns:
        AppConfig: The application configuration.
    """
    output_config = AppConfig()

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    base_app_directory = os.getenv("BASE_APP_DIRECTORY")

    if base_app_directory is None:
        raise EnvironmentError("BASE_APP_DIRECTORY environment variable not set")
    raster_library_directory = os.path.join(base_app_directory, "raster_data")

    base_app_name = os.getenv("BASE_APP_NAME")
    if base_app_name is None:
        base_app_name = "Raster Query Application"

    output_config.application_name = base_app_name
    output_config.logger = logging.getLogger(base_app_name)
    output_config.raster_data_folder = Path(raster_library_directory)


    return output_config


app_config = create_app_config()
