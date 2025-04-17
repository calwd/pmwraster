"""
This module contains the raster processing querying dependencies for the application.
"""
import logging
import os
from pathlib import Path

import rasterio

from app.api.models import BoundingBox, RasterInformation


class RasterQueryManager:
    """
    RasterManager is a class that manages raster processing queries.
    """

    raster_collection: dict[str, RasterInformation]
    raster_directory: Path

    def __init__(self, raster_directory: Path, logger: logging.Logger = None):
        """
        Initialize the RasterManager with a directory pointing to the raster files.

        Args:
            raster_directory (str): The path to directory containing raster files.
        """

        self.raster_collection = {}
        self.raster_directory = raster_directory

        raster_list = os.listdir(raster_directory)

        for raster_file in raster_list:
            if raster_file.endswith(".tif"):

                raster_name = raster_file.split(".")[0]
                raster_path = os.path.join(raster_directory, raster_file)

                try:
                    raster_info = create_raster_statistics(raster_path, raster_name)
                    self.raster_collection[raster_name] = raster_info
                except Exception as e:
                    if logger is not None:
                        logger.error(f"Error processing raster {raster_file}: {e}")

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
        self, raster_name: str, longitude: float, latitude: float
    ) -> float | int:
        """
        Get the pixel value for a given raster name and coordinates.

        Args:
            raster_name (str): The name of the raster.
            longitude (float): The longitude of the pixel.
            latitude (float): The latitude of the pixel.
        Returns:
            float | int: The pixel value.
        """

        if raster_name not in self.raster_collection:
            raise ValueError(
                f"Raster {raster_name} not found in the collection for this API"
            )

        # Open the raster
        with rasterio.open(
            os.path.join(self.raster_directory, f"{raster_name}.tif")
        ) as src:
            # Convert coordinates to row/column indices
            row, col = src.index(latitude, longitude)

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
    with rasterio.open(raster_file) as src:
        # Get bounds
        bounds = src.bounds
        min_lon, min_lat, max_lon, max_lat = (
            bounds.left,
            bounds.bottom,
            bounds.right,
            bounds.top,
        )

        # Read the first band (index 1 for rasterio)
        band1 = src.read(1, masked=True)  # masked=True handles nodata

        # Get statistics
        min_val = band1.min()
        mean_val = band1.mean()
        max_val = band1.max()

        # Create RasterInformation object
        raster_info = RasterInformation(
            image_name=raster_name,
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

        return raster_info
