"""
This module contains the data models (via pydantic) used in the application
"""

from pydantic import BaseModel


class PixelQueryResponse(BaseModel):
    """
    Response model for pixel query.
    """

    imageName: str
    pixelValue: float | int


class BoundingBox(BaseModel):
    """
    Bounding box coordinates for an image.
    """

    min_longitude: float
    min_latitude: float
    max_longitude: float
    max_latitude: float


class ImageStatsResponse(BaseModel):
    """
    Response model for image statistics.
    """

    imageName: str
    maximum_pixel_value: float | int
    minimum_pixel_value: float | int
    mean_pixel_value: float | int
    bounding_box: BoundingBox
