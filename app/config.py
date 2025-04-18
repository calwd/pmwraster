"""
This module contains the application configuration
"""

import logging
import os
from pathlib import Path


class AppConfig:
    raster_data_folder: Path
    logger: logging.Logger


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
    output_config.raster_data_folder = Path(raster_library_directory)

    base_app_name = os.getenv("BASE_APP_NAME")

    if base_app_name is None:
        base_app_name = "Raster Query Application"

    output_config.logger = logging.getLogger(base_app_name)

    return output_config


app_config = create_app_config()
