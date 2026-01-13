from pydantic import BaseModel
from app.schemas.geo import DistanceKm, Latitude, Longitude

class NearbyQuery(BaseModel):
    latitude: Latitude
    longitude: Longitude
    distance_km: DistanceKm
