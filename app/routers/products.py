from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
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