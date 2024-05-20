from sqlalchemy.orm import Session
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
    customer = session.query(Customer).filter(Customer.name == customer_to_create.name).first()

    if customer is None:
        session.add(customer_to_create)
        session.commit()
        return session.query(Customer).filter(Customer.name == customer_to_create.name).first()
    return customer


def create_seller(seller_to_create: Seller, session: Session) -> Seller:
    """Creates a seller if it does not exist.(by name)"""
    seller = session.query(Seller).filter(Seller.title == seller_to_create.title).first()

    if seller is None:
        session.add(seller_to_create)
        session.commit()
        return session.query(Seller).filter(Seller.title == seller_to_create.title).first()
    return seller


with Session(ENGINE) as session:
    customer = Customer(name="John", surname="Doe", login="johndoe", password="123", age=25)
    seller = Seller(title="Seller", login="seller", password="123", rate=4.5, address="address", card_number="1234")

    print(create_customer(customer_to_create=customer, session=session))
    print(create_seller(seller_to_create=seller, session=session))
