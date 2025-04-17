
from fastapi import APIRouter, Path, Query

from models import PixelQueryResponse,ImageStatsResponse
router = APIRouter()



@router.get("/images/{image_name}/query", response_model=PixelQueryResponse)
def query_pixel(
    image_name: str = Path(..., description="Name of the image"),
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    # dummy return
    return PixelQueryResponse(imageName=image_name, pixelValue=42.5)


@router.get("/images/{image_name}/stats", response_model=ImageStatsResponse)
def get_image_stats(image_name: str):
    # dummy return
    return ImageStatsResponse(
        imageName=image_name,
        maximum_pixel_value=255.0,
        minimum_pixel_value=0.0,
        mean_pixel_value=128.6
    )