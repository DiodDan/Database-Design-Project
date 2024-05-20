from datetime import datetime, timezone

from sqlalchemy import (
    FLOAT,
    INTEGER,
    TIMESTAMP,
    Boolean,
    Column,
    Enum,
    ForeignKey,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base

from custom_enums import ItemCategory, OrderStatus
from settings import settings

Base = declarative_base()
ENGINE = create_engine(settings.PG_DSN)


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Customer(Base):
    __tablename__: str = "customers"
    id: int = Column(  # type: ignore
        "id",
        INTEGER,
        primary_key=True,
        unique=True,
        autoincrement=True,
    )
    name: str = Column("name", String, nullable=False)
    surname: str = Column("surname", String, nullable=False)
    login: str = Column("login", String, nullable=False)
    password: str = Column("password", String, nullable=False)
    age: int = Column("age", INTEGER, nullable=False)
    verified: bool = Column("verified", Boolean, default=False)
    created_at: datetime = Column("created_at", TIMESTAMP, default=utc_now)
    cart_price: float = Column("cart_price", FLOAT, default=0.0)

    def __str__(self) -> str:
        return f"{'*' * 10}\n{self.name=}\n{self.surname=}\n{self.login=}\n{self.age=}\n{str(self.created_at)=}\n{'*' * 10}\n"


class Seller(Base):
    __tablename__: str = "sellers"
    id: int = Column(  # type: ignore
        "id",
        INTEGER,
        primary_key=True,
        unique=True,
        autoincrement=True,
    )
    title: str = Column("name", String, nullable=False)
    login: str = Column("login", String, nullable=False)
    password: str = Column("password", String, nullable=False)
    rate: float = Column("rate", FLOAT, nullable=False)
    created_at: datetime = Column("created_at", TIMESTAMP, default=utc_now)
    address: str = Column("address", String, nullable=False)
    card_number: str = Column("card_number", String, nullable=False)
    total_sales: float = Column("total_sales", FLOAT, default=0.0)

    def __str__(self) -> str:
        return f"{'*' * 10}\n{self.title=}\n{self.login=}\n{self.rate=}\n{str(self.created_at)=}\n{self.address=}\n{self.card_number=}\n{self.total_sales=}\n{'*' * 10}\n"


class Address(Base):
    __tablename__: str = "addresses"
    id: int = Column(  # type: ignore
        "id",
        INTEGER,
        primary_key=True,
        unique=True,
        autoincrement=True,
    )
    customer_id: int = Column("customer_id", ForeignKey("customers.id"), nullable=False)
    address: str = Column("address", String, nullable=False)


class PaymentMethod(Base):
    __tablename__: str = "payment_methods"

    customer_id: int = Column(
        "customer_id", ForeignKey("customers.id"), nullable=False, primary_key=True
    )
    card_number: str = Column("card_number", String, nullable=False, primary_key=True)
    cvc: int = Column("cvc", INTEGER, nullable=False)
    card_holder: str = Column("card_holder", String, nullable=False)
    valid_until: str = Column("valid_until", String, nullable=False)


class Item(Base):
    __tablename__: str = "items"
    id: int = Column(  # type: ignore
        "id",
        INTEGER,
        primary_key=True,
        unique=True,
        autoincrement=True,
    )
    title: str = Column("title", String, nullable=False)
    category: ItemCategory = Column("category", Enum(ItemCategory), nullable=False)
    rate: float = Column("rate", FLOAT, nullable=False)
    description: str = Column("description", String, nullable=False)
    seller_id: int = Column("seller_id", ForeignKey("sellers.id"), nullable=False)
    cost: float = Column("cost", FLOAT, nullable=False)
    created_at: datetime = Column("created_at", TIMESTAMP, default=utc_now)


    def __str__(self) -> str:
        return f"{'*' * 10}\n{self.title=}\n{self.category=}\n{self.rate=}\n{self.description=}\n{self.seller_id=}\n{self.cost=}\n{str(self.created_at)=}\n{'*' * 10}\n"

class CustomerItemCart(Base):
    __tablename__: str = "customer_item_cart"
    customer_id: int = Column(
        "customer_id", ForeignKey("customers.id"), nullable=False, primary_key=True
    )
    item_id: int = Column(
        "item_id", ForeignKey("items.id"), nullable=False, primary_key=True
    )
    amount: int = Column("quantity", INTEGER, nullable=False)


class CustomerItemWish(Base):
    __tablename__: str = "customer_item_wish"
    customer_id: int = Column(
        "customer_id", ForeignKey("customers.id"), nullable=False, primary_key=True
    )
    item_id: int = Column(
        "item_id", ForeignKey("items.id"), nullable=False, primary_key=True
    )


class Rate(Base):
    __tablename__: str = "rates"
    customer_id: int = Column(
        "customer_id", ForeignKey("customers.id"), nullable=False, primary_key=True
    )
    item_id: int = Column(
        "item_id", ForeignKey("sellers.id"), nullable=False, primary_key=True
    )
    rate: float = Column("rate", FLOAT, nullable=False)
    body: str = Column("body", String, nullable=False)


class Order(Base):
    __tablename__: str = "orders"
    id: int = Column(  # type: ignore
        "id",
        INTEGER,
        primary_key=True,
        unique=True,
        autoincrement=True,
    )
    customer_id: int = Column("customer_id", ForeignKey("customers.id"), nullable=False)
    delivery_address: str = Column("delivery_address", String, nullable=False)
    status: OrderStatus = Column("status", Enum(OrderStatus), nullable=False)
    total_cost: float = Column("total_cost", FLOAT, nullable=False)
    created_at: datetime = Column("created_at", TIMESTAMP, default=utc_now)
    comment: str = Column("comment", String, nullable=False)


class OrderItem(Base):
    __tablename__: str = "order_items"
    order_id: int = Column(
        "order_id", ForeignKey("orders.id"), nullable=False, primary_key=True
    )
    item_id: int = Column(
        "item_id", ForeignKey("items.id"), nullable=False, primary_key=True
    )
    amount: int = Column("amount", INTEGER, nullable=False)


class Warehouse(Base):
    __tablename__: str = "warehouses"
    id: int = Column(  # type: ignore
        "id",
        INTEGER,
        primary_key=True,
        unique=True,
        autoincrement=True,
    )
    title: str = Column("title", String, nullable=False)
    address: str = Column("address", String, nullable=False)


class WarehouseItem(Base):
    __tablename__: str = "warehouse_items"
    warehouse_id: int = Column(
        "warehouse_id", ForeignKey("warehouses.id"), nullable=False, primary_key=True
    )
    item_id: int = Column(
        "item_id", ForeignKey("items.id"), nullable=False, primary_key=True
    )
    amount: int = Column("amount", INTEGER, nullable=False)
