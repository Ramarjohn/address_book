from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.db.session import get_db
from app.schemas.address import AddressCreate, AddressOut, AddressUpdate
from app.services.address_service import (
    create_address, delete_address, get_address, list_addresses, update_address
)
from app.services.distance import haversine_km
from app.schemas.nearby import NearbyQuery

router = APIRouter()
log = get_logger(__name__)

@router.post("/addresses", response_model=AddressOut, status_code=201)
def create(payload: AddressCreate, db: Session = Depends(get_db)):
    log.info("Creating address label=%s", payload.label)
    return create_address(db, payload)

@router.get("/addresses", response_model=list[AddressOut])
def list_all(db: Session = Depends(get_db)):
    return list_addresses(db)

@router.get("/addresses/{address_id}", response_model=AddressOut)
def get_one(address_id: int, db: Session = Depends(get_db)):
    obj = get_address(db, address_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Address not found")
    return obj

@router.put("/addresses/{address_id}", response_model=AddressOut)
def update_one(address_id: int, payload: AddressUpdate, db: Session = Depends(get_db)):
    log.info("Updating address id=%s", address_id)
    obj = update_address(db, address_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Address not found")
    return obj

@router.delete("/addresses/{address_id}", status_code=204)
def delete_one(address_id: int, db: Session = Depends(get_db)):
    log.info("Deleting address id=%s", address_id)
    ok = delete_address(db, address_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Address not found")
    return None

@router.get("/addresses/nearby", response_model=list[AddressOut])
def nearby(
    q: NearbyQuery = Depends(),
    db: Session = Depends(get_db),
):
    all_rows = list_addresses(db)
    result = []
    for row in all_rows:
        d = haversine_km(q.latitude, q.longitude, row.latitude, row.longitude)
        if d <= q.distance_km:
            result.append(row)
    log.info(
        "Nearby query lat=%s lon=%s km=%s -> %s results",
        q.latitude,
        q.longitude,
        q.distance_km,
        len(result),
    )
    return result
