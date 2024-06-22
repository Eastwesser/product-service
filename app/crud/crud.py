from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.models.models import Product


async def get_product(db: Session, product_id: int):
    result = await db.execute(select(Product).filter(Product.id == product_id))
    return result.scalars().first()


async def get_all_products(db: Session):
    result = await db.execute(select(Product))
    return result.scalars().all()


async def create_product(db: Session, product: Product):
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product
