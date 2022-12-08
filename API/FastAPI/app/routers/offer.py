from fastapi import Response, status, HTTPException, Depends, APIRouter
from fastapi_pagination import Page, add_pagination, paginate
from .. import models, schemas, oauth2
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(prefix="/offers-list", tags=["OffersList"])


@router.get("/", response_model=Page[schemas.OfferListOut])
def get_offers_list(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    offset: int = 0,
    search: Optional[str] = "",
):
    offers_list = (
        db.query(models.OfferList)
        .filter(models.OfferList.product_name.contains(search))
        .limit(limit)
        .offset(offset)
        .all()
    )
    return paginate(offers_list)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.OfferListOut
)
def create_offer_product(
    offer_product: schemas.OfferListCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    amount = offer_product.qty * offer_product.price
    new_offer_product = models.OfferList(
        owner_id=current_user.id, amount=amount, **offer_product.dict()
    )

    db.add(new_offer_product)
    db.commit()
    db.refresh(new_offer_product)
    return new_offer_product


@router.get("/{id}", response_model=List[schemas.OfferListOut])
def get_offer(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    offer_product = (
        db.query(models.OfferList).filter(models.OfferList.offer_id == id).all()
    )

    if not offer_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Offer Product with id: {id} not found.",
        )

    return offer_product


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_offer_product(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    offer_product_query = db.query(models.OfferList).filter(models.OfferList.id == id)
    offer_product = offer_product_query.first()

    if offer_product == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Offer Product with id: {id} does not exist.",
        )

    if offer_product.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action.",
        )

    offer_product_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.OfferListOut)
def update_offer_product(
    id: int,
    updated_offer_product: schemas.OfferListCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    offer_product_query = db.query(models.OfferList).filter(models.OfferList.id == id)
    offer_product = offer_product_query.first()

    new_update = updated_offer_product.dict()
    new_update["amount"] = updated_offer_product.qty * updated_offer_product.price

    if offer_product == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Offer Product with id: {id} does not exist.",
        )

    if offer_product.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action.",
        )

    offer_product_query.update(new_update)
    db.commit()
    return offer_product_query.first()

add_pagination(router)
