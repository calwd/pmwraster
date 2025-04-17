from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.api.dependencies import get_raster_query_manager
from app.api.models import PixelQueryResponse, RasterInformation
from app.raster.raster import RasterQueryManager

router = APIRouter()


@router.get("/images/{image_name}/query", response_model=PixelQueryResponse)
def query_pixel(
    image_name: str = Path(..., description="Name of the image"),
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    manager: RasterQueryManager = Depends(get_raster_query_manager),
):
    # dummy return

    if image_name not in manager.raster_collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found in the raster collection for this API",
        )

    can_query = manager.check_coordinates(image_name, lon, lat)

    if can_query is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coordinates are outside the bounding box of the raster",
        )

    try:
        pixel_value = manager.get_raster_pixel_value(image_name, lat, lon)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return PixelQueryResponse(image_name=image_name, pixel_value=pixel_value)


@router.get("/images/{image_name}/stats", response_model=RasterInformation)
def get_image_stats(
    image_name: str, manager: RasterQueryManager = Depends(get_raster_query_manager)
):

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
