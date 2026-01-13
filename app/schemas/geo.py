from typing import Annotated
from pydantic import Field

Latitude = Annotated[float, Field(ge=-90, le=90, allow_inf_nan=False)]
Longitude = Annotated[float, Field(ge=-180, le=180, allow_inf_nan=False)]
DistanceKm = Annotated[float, Field(gt=0, le=20000, allow_inf_nan=False)]
