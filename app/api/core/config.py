class AppConfig:
    raster_data_folder: str


def create_app_config() -> AppConfig:
    """
    Create the application configuration.
    Returns:
        AppConfig: The application configuration.
    """
    output_config = AppConfig()
    output_config.raster_data_folder = (
        "/home/matthew/Documents/projects/perennial-raster/app/raster/data"
    )
    return output_config


app_config = create_app_config()
