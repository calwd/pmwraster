"""
This module contains the data models (via pydantic) used in the application
"""

from pydantic import BaseModel


class PixelQueryResponse(BaseModel):
    """
    Response model for pixel query.

    Attributes:
        image_name (str): The name of the image.
        pixel_value (float | int): The pixel value at the specified coordinates.
    """

    image_name: str
    pixel_value: float | int


class BoundingBox(BaseModel):
    """
    Bounding box coordinates for an image.

    Attributes:
        min_longitude (float): The minimum longitude of the bounding box.
        min_latitude (float): The minimum latitude of the bounding box.
        max_longitude (float): The maximum longitude of the bounding box.
        max_latitude (float): The maximum latitude of the bounding box.
    """

    min_longitude: float
    min_latitude: float
    max_longitude: float
    max_latitude: float


class RasterInformation(BaseModel):
    """
    Response model for image statistics.

    This model contains the image name, EPSG code, pixel values, and bounding box.

    Attributes:
        image_name (str): The name of the image.
        image_epsg (int | None): The EPSG code of the image.
        maximum_pixel_value (float | int): The maximum pixel value in the image.
        minimum_pixel_value (float | int): The minimum pixel value in the image.
        mean_pixel_value (float | int): The mean pixel value in the image.
        bounding_box (BoundingBox): The bounding box coordinates of the image.
    """

    image_name: str
    image_epsg: int | None
    maximum_pixel_value: float | int
    minimum_pixel_value: float | int
    mean_pixel_value: float | int
    bounding_box: BoundingBox
