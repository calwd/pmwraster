from functools import lru_cache
from pathlib import Path

from app.api.core.config import app_config
from app.raster.raster import RasterQueryManager


@lru_cache()
def get_raster_query_manager() -> RasterQueryManager:
    return RasterQueryManager(raster_directory=Path(app_config.raster_data_folder))
