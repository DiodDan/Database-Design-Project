from sqlalchemy.orm import Session

from custom_enums import ItemCategory
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
from db_creation import create_db

create_db()


def create_customer(customer_to_create: Customer, session: Session) -> Customer:
    """Creates a customer if it does not exist.(by name)"""
    customer = (
        session.query(Customer).filter(Customer.name == customer_to_create.name).first()
    )

    if customer is None:
        session.add(customer_to_create)
        session.commit()
        return (
            session.query(Customer)
            .filter(Customer.name == customer_to_create.name)
            .first()
        )
    return customer


def create_seller(seller_to_create: Seller, session: Session) -> Seller:
    """Creates a seller if it does not exist.(by name)"""
    seller = (
        session.query(Seller).filter(Seller.title == seller_to_create.title).first()
    )

    if seller is None:
        session.add(seller_to_create)
        session.commit()
        return (
            session.query(Seller).filter(Seller.title == seller_to_create.title).first()
        )
    return seller


def create_item(item_to_create: Item, session: Session) -> Item:
    """Creates an item if it does not exist.(by name)"""
    item = session.query(Item).filter(Item.title == item_to_create.title).first()

    if item is None:
        session.add(item_to_create)
        session.commit()
        return session.query(Item).filter(Item.title == item_to_create.title).first()
    return item


with Session(ENGINE) as session:
    customer = Customer(
        name="John", surname="Doe", login="johndoe", password="123", age=25
    )
    seller = Seller(
        title="Seller",
        login="seller",
        password="123",
        rate=4.5,
        address="address",
        card_number="1234",
    )
    seller = create_seller(seller_to_create=seller, session=session)
    items = [
        Item(
            title="Item1",
            category=ItemCategory.FOOD,
            rate=4.3,
            cost=100,
            seller_id=seller.id,
            description="desc of item1",
        ),
        Item(
            title="Item2",
            category=ItemCategory.OTHER,
            rate=4.2,
            cost=140,
            seller_id=seller.id,
            description="desc of item2",
        ),
        Item(
            title="Item3",
            category=ItemCategory.ELECTRONICS,
            rate=4.5,
            cost=200,
            seller_id=seller.id,
            description="desc of item3",
        ),
    ]
    print(*[create_item(item_to_create=item, session=session) for item in items], sep="\n")

    print(create_customer(customer_to_create=customer, session=session))
    print(seller)
