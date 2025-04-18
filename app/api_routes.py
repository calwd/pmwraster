"""
This module defines the API routes for querying raster images.
"""
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from .models import PixelQueryResponse, RasterInformation
from .queries import RasterQueryManager, get_raster_query_manager

router = APIRouter()


@router.get("/images/{image_name}/query", response_model=PixelQueryResponse)
def query_pixel(
    image_name: str = Path(..., description="Name of the image"),
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    manager: RasterQueryManager = Depends(get_raster_query_manager),
):
    """
    API Endpoint to query a pixel value from a raster image using latitude and longitude coordinates.
    :param image_name: the name of the image to query
    :param lat: the latitude of the pixel to query
    :param lon: the longitude of the pixel to query
    :param manager: (RasterQueryManager): The raster query manager instance. Uses FastAPI dependency injection pattern

    :return:
    """

    if image_name not in manager.raster_collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found in the raster collection for this API",
        )

    raster_info = manager.raster_collection[image_name]

    x_coord, y_coord = manager.convert_lat_lon_coordinates(lon, lat, raster_info)

    can_query = manager.check_coordinates(image_name, x_coord, y_coord)

    if can_query is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coordinates are outside the bounding box of the raster",
        )

    try:
        pixel_value = manager.get_raster_pixel_value(
            image_name, x_coordinate=x_coord, y_coordinate=y_coord
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return PixelQueryResponse(image_name=image_name, pixel_value=pixel_value)


@router.get("/images/{image_name}/stats", response_model=RasterInformation)
def get_image_stats(
    image_name: str, manager: RasterQueryManager = Depends(get_raster_query_manager)
):
    """
    API Endpoint to GET raster statistics for a given image name.
    :param image_name: The name of the image to get statistics for.
    :param manager: The raster query manager instance. Uses FastAPI dependency injection pattern
    :return:
    """

    if image_name not in manager.raster_collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found in the raster collection for this API",
        )
    try:
        raster_info = manager.get_raster_statistics(image_name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    return raster_info
