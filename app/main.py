import logging
import os
import sys

import sentry_sdk
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.models.models import Base, Product as ProductModel
from app.models.pydantic_models import Product, ProductCreate
from app.rabbit.rabbit import send_message
from app.redis.redis import set_cache
from app.crud.crud import get_product, get_all_products, create_product

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'crud')))
load_dotenv()

SENTRY_DSN = os.getenv("SENTRY_DSN")
sentry_sdk.init(
    dsn=SENTRY_DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()

app = FastAPI()

app.add_middleware(SentryAsgiMiddleware)


async def get_db():
    async with SessionLocal() as session:
        yield session


@app.on_event("startup")
async def startup():
    logging.info("Starting up the application")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    logging.info("Shutting down the application")
    await engine.dispose()


@app.get("/")
async def read_root():
    return {"Hello": "Product Service"}


@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/products/")
async def read_all_products(db: AsyncSession = Depends(get_db)):
    return await get_all_products(db)


@app.get("/cause-error/")
async def cause_error():
    raise ValueError("This is a test error for Sentry")


@app.post("/products/", response_model=Product)
async def create_product_endpoint(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_product = ProductModel(**product.dict())
        created_product = await create_product(db, db_product)

        # Commit the transaction to persist changes
        await db.commit()

        # Fetch the product within the same session context
        async with db.begin():
            db.refresh(created_product)

        # Example: Sending a message and caching the product
        await send_message(f"Product {created_product.name} created")
        await set_cache(f"product_{created_product.id}", created_product)

        return created_product
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0


@app.exception_handler(Exception)
async def sentry_exception_handler(request: Request, exc: Exception):
    sentry_sdk.capture_exception(exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred"},
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
