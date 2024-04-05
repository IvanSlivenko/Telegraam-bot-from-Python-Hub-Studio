from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from database.models import Produkt
async def orm_product(session: AsyncSession, data: dict):
    оbj = Produkt(
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        image=data["image"],
    )
    session.add(оbj)
    await session.commit()

async def orm_get_products(session: AsyncSession):
    query = select(Produkt)
    result = await session.execute(query)
    return result.scalar().all()

async def orm_get_product(session: AsyncSession, product_id: int):
    query = select(Produkt).where(Produkt.id == product_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_update_product(session: AsyncSession, product_id: int, data):
    query = update(Produkt).where(Produkt.id == product_id).values(
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        image=data["image"],)
    await session.execute(query)
    await session.commit()


async def orm_delete_product(session: AsyncSession, product_id: int):
    query = delete(Produkt).where(Produkt.id == product_id)
    await session.execute(query)
    await session.commit()
