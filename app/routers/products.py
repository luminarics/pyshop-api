from typing import Annotated
from fastapi import HTTPException
from typing import List
from fastapi import APIRouter, Depends, status, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.database import get_session
from app.models.product import ProductCreate, ProductRead, ProductUpdate

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/products/", response_model=List[ProductRead])
async def list_products(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
):
    result = await session.execute(
        select(Product).order_by(Product.id).offset(offset).limit(limit)
    )
    return result.scalars().all()


@router.post(
    "/products/", response_model=ProductRead, status_code=status.HTTP_201_CREATED
)
async def create_product(
    token: Annotated[str, Depends(oauth2_scheme)],
    product_data: ProductCreate,
    session: AsyncSession = Depends(get_session),
):
    product = Product(**product_data.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


@router.put("/products/{product_id}", response_model=ProductRead)
async def update_product(
    token: Annotated[str, Depends(oauth2_scheme)],
    product_id: int,
    payload: ProductUpdate,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in payload.model_dump().items():
        setattr(product, key, value)

    await session.commit()
    await session.refresh(product)
    return product


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    token: Annotated[str, Depends(oauth2_scheme)],
    product_id: int,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await session.delete(product)
    await session.commit()
    return
