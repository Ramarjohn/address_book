from sqlalchemy.orm import Session
from sqlalchemy import select
import requests

from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate

def reverse_geocode(latitude: float, longitude: float) -> dict | None:
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "lat": latitude,
        "lon": longitude,
        "format": "json",
        "addressdetails": 1
    }
    headers = {
        "User-Agent": "address-book-app/1.0",
        "Accept": "application/json"
    }
    try:
        print("Reverse geocoding:", params )
        print("URL:", url)
        response = requests.get(url, params=params, headers=headers)
        print(response)
        response.raise_for_status()
        data = response.json()
        if data:
            address = data.get("address", {})
            return {
                "postal_code": address.get("postcode"),
                "country": address.get("country"),
                "state": address.get("state"),
                "city": address.get("city") or address.get("town") or address.get("village"),
                "district": address.get("county"),
                "street": address.get("road") or address.get("pedestrian") or address.get("path")
            }
    except Exception:
        pass
    return None

def create_address(db: Session, payload: AddressCreate) -> Address:
    label = payload.label
    if label is None:
        label = f"({payload.latitude:.6f}, {payload.longitude:.6f})"
    
    geo_data = reverse_geocode(payload.latitude, payload.longitude)
    print(geo_data)
    obj = Address(
        label=label,
        latitude=payload.latitude,
        longitude=payload.longitude,
        postal_code=geo_data.get("postal_code") if geo_data else None,
        country=geo_data.get("country") if geo_data else None,
        state=geo_data.get("state") if geo_data else None,
        city=geo_data.get("city") if geo_data else None,
        district=geo_data.get("district") if geo_data else None,
        street=geo_data.get("street") if geo_data else None
    )
    db.add(obj)
    db.commit()
    return obj

def get_address(db: Session, postal_code: str) -> Address | None:
    return db.scalar(select(Address).where(Address.postal_code == postal_code))

def list_addresses(db: Session) -> list[Address]:
    return list(db.scalars(select(Address).order_by(Address.id)).all())

def update_address(db: Session, postal_code: str, payload: AddressUpdate) -> Address | None:
    obj = db.scalar(select(Address).where(Address.postal_code == postal_code))
    if not obj:
        return None
    if payload.label is not None:
        obj.label = payload.label
    if payload.latitude is not None:
        obj.latitude = payload.latitude
    if payload.longitude is not None:
        obj.longitude = payload.longitude
    if payload.postal_code is not None:
        obj.postal_code = payload.postal_code
    if payload.country is not None:
        obj.country = payload.country
    if payload.state is not None:
        obj.state = payload.state
    if payload.city is not None:
        obj.city = payload.city
    if payload.district is not None:
        obj.district = payload.district
    if payload.street is not None:
        obj.street = payload.street
    db.add(obj)
    db.commit()
    return obj

def delete_address(db: Session, postal_code: str) -> bool:
    obj = db.scalar(select(Address).where(Address.postal_code == postal_code))
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
