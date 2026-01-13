from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.address import Address
from app.schemas.address import AddressCreate, AddressUpdate

def create_address(db: Session, payload: AddressCreate) -> Address:
    label = payload.label
    if label is None:
        label = f"({payload.latitude:.6f}, {payload.longitude:.6f})"
    obj = Address(label=label, latitude=payload.latitude, longitude=payload.longitude)
    db.add(obj)
    db.commit()
    return obj

def get_address(db: Session, address_id: int) -> Address | None:
    return db.get(Address, address_id)

def list_addresses(db: Session) -> list[Address]:
    return list(db.scalars(select(Address).order_by(Address.id)).all())

def update_address(db: Session, address_id: int, payload: AddressUpdate) -> Address | None:
    obj = db.get(Address, address_id)
    if not obj:
        return None
    if payload.label is not None:
        obj.label = payload.label
    if payload.latitude is not None:
        obj.latitude = payload.latitude
    if payload.longitude is not None:
        obj.longitude = payload.longitude
    db.add(obj)
    db.commit()
    return obj

def delete_address(db: Session, address_id: int) -> bool:
    obj = db.get(Address, address_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
