from models import (
    Customer,
    Seller,
    Address,
    PaymentMethod,
    Item,
    CustomerItemCart,
    CustomerItemWish,
    Rate,
    Order,
    OrderItem,
    Warehouse,
    WarehouseItem,
    Base,
    ENGINE,
)


def create_db():
    Base.metadata.create_all(ENGINE)
