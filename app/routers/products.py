from http.client import HTTPException
from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel import  select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.database import get_session

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[Product])
async def list_products(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Product))
    return result.scalars().all()

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: Product, session: AsyncSession = Depends(get_session)):
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product

@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_id: int, 
    payload: Product, 
    session: AsyncSession = Depends(get_session)
):
     result = await session.execute(select(Product).where(Product.id == product_id))
     product = result.scalars().first()
     if not product:
            raise HTTPException(status_code=404, detail="Product not found")
     product.name = payload.name
     product.price = payload.price
     await session.commit()
     await session.refresh(product)
     return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await session.delete(product)
    await session.commit()
    return