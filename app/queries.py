import os
from functools import lru_cache
from pathlib import Path

import rasterio  # type: ignore
from pyproj import Transformer

from app.config import AppConfig
from app.config import app_config as config
from app.models import BoundingBox, RasterInformation


class RasterQueryManager:
    """
    RasterManager is a class that manages raster processing queries for the API.
    It provides methods to check if coordinates are within the bounding box of a raster image,
    get raster statistics, and get pixel values from a raster image.
    """

    raster_collection: dict[str, RasterInformation]
    raster_directory: Path
    app_config: AppConfig

    def __init__(self, input_config: AppConfig):
        """
        Initialize the RasterManager with a directory pointing to the raster files.

        Args:
            input_config (AppConfig): The config object for the application
        """

        self.raster_collection = {}
        self.app_config = input_config
        self.raster_directory = self.app_config.raster_data_folder

        raster_list = os.listdir(self.raster_directory)

        for raster_file in raster_list:
            if raster_file.endswith(".tif"):

                raster_name = raster_file.split(".")[0]
                raster_path = os.path.join(self.raster_directory, raster_file)

                try:
                    raster_info = create_raster_statistics(raster_path, raster_name)
                    self.raster_collection[raster_name] = raster_info
                except Exception as e:
                    if self.app_config.logger is not None:
                        self.app_config.logger.error(
                            f"Error processing raster {raster_file}: {e}"
                        )

    def check_coordinates(
        self, raster_name: str, longitude: float, latitude: float
    ) -> bool:
        """
        Check if the given coordinates are within the bounding box of the raster.
        :param raster_name:
        :param longitude:
        :param latitude:
        :return:
        """

        output_bool = True  # this is the default value indicating that the coordinates are within the bounding box
        if raster_name not in self.raster_collection:
            return False

        raster_info = self.raster_collection[raster_name]

        # Check if the coordinates are within the bounding box
        if (
            longitude < raster_info.bounding_box.min_longitude
            or longitude > raster_info.bounding_box.max_longitude
            or latitude < raster_info.bounding_box.min_latitude
            or latitude > raster_info.bounding_box.max_latitude
        ):
            output_bool = False

        return output_bool

    def convert_lat_lon_coordinates(
        self, longitude: float, latitude: float, image_information: RasterInformation
    ) -> tuple[float, float]:
        """
        Convert the given latitude and longitude to new coordinates based on the raster's EPSG code.
        :param longitude:
        :param latitude:
        :param image_information: RasterInformation object containing image metadata
        :return: tuple of new coordinates (x, y)
        """

        if image_information.image_epsg is not None:
            if image_information.image_epsg == 4326:
                # No conversion needed, already in EPSG:4326
                return longitude, latitude

        transformer = Transformer.from_crs(
            "EPSG:4326", image_information.image_epsg, always_xy=True
        )

        x, y = transformer.transform(longitude, latitude)
        # Placeholder for actual conversion logic
        return x, y

    def get_raster_statistics(self, raster_name: str) -> RasterInformation:
        """
        Get raster statistics for a given raster name.

        Args:
            raster_name (str): The name of the raster.
        Returns:
            RasterInformation: The raster statistics.
        """

        if raster_name not in self.raster_collection:
            raise ValueError(
                f"Raster {raster_name} not found in the collection for this API"
            )

        return self.raster_collection[raster_name]

    def get_raster_pixel_value(
        self, raster_name: str, x_coordinate: float, y_coordinate: float
    ) -> float | int:
        """
        Get the pixel value for a given raster name and coordinates.

        Args:
            raster_name (str): The name of the raster.
            x_coordinate (float): The longitude of the pixel.
            y_coordinate (float): The latitude of the pixel.
        Returns:
            float | int: The pixel value.
        """

        with rasterio.open(
            os.path.join(self.raster_directory, f"{raster_name}.tif")
        ) as src:
            # Convert coordinates to row/column indices
            row, col = src.index(x_coordinate, y_coordinate)

            # Read the pixel value
            pixel_value = src.read(1)[row, col]
        return pixel_value


def create_raster_statistics(raster_file: str, raster_name: str) -> RasterInformation:
    """
    Create raster statistics for a given raster file.

    Args:
        raster_file (str): The path to the raster file.
        raster_name (str): The name of the raster file (without extension or path).
    Returns:
        RasterInformation: The raster statistics.
    """

    # Open the raster

    try:
        with rasterio.open(raster_file) as src:
            # Get bounds
            bounds = src.bounds
            min_lon, min_lat, max_lon, max_lat = (
                bounds.left,
                bounds.bottom,
                bounds.right,
                bounds.top,
            )

            # get the EPSG code
            epsg_code = src.crs.to_epsg()

            # Read the first band (index 1 for rasterio)
            band1 = src.read(1, masked=True)  # masked=True handles nodata

            # Get statistics
            min_val = band1.min()
            mean_val = band1.mean()
            max_val = band1.max()

            # Create RasterInformation object
            raster_info = RasterInformation(
                image_name=raster_name,
                image_epsg=None,
                maximum_pixel_value=max_val,
                minimum_pixel_value=min_val,
                mean_pixel_value=mean_val,
                bounding_box=BoundingBox(
                    min_longitude=min_lon,
                    min_latitude=min_lat,
                    max_longitude=max_lon,
                    max_latitude=max_lat,
                ),
            )

            # Set the EPSG code
            if epsg_code is not None:
                raster_info.image_epsg = epsg_code

    except Exception as e:
        raise ValueError(f"Error processing raster {raster_file}: {e}")

    return raster_info


@lru_cache()
def get_raster_query_manager() -> RasterQueryManager:
    """
    Get the RasterQueryManager instance. This function is structured/cached like this in order to
    meet the requirements of the FastAPI dependency injection system
    :return: RasterQueryManager instance
    """

    return RasterQueryManager(input_config=config)
