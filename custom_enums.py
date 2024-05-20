from enum import Enum


class ItemCategory(Enum):
    ELECTRONICS = "electronics"
    CLOTHES = "clothes"
    BOOKS = "books"
    SPORT = "sport"
    FOOD = "food"
    OTHER = "other"


class OrderStatus(Enum):
    PROCESSING = "processing"
    PAYED = "payed"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
    FINISHED = "finished"
    CANCELED = "canceled"
