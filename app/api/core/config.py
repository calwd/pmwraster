"""
This module contains the application configuration
"""

import os


class AppConfig:
    raster_data_folder: str


def create_app_config() -> AppConfig:
    """
    Create the application configuration.
    Returns:
        AppConfig: The application configuration.
    """
    output_config = AppConfig()

    base_app_directory = os.getenv("BASE_APP_DIRECTORY")

    if base_app_directory is None:
        raise EnvironmentError("BASE_APP_DIRECTORY environment variable not set")

    raster_library_directory = os.path.join(base_app_directory, "raster", "data")
    output_config.raster_data_folder = raster_library_directory
    return output_config


app_config = create_app_config()
