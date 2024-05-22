# Database Design Documentation
#### Created by Danila Prigulsky, Ivan Rudnev, Egor Silakov
## Table of Contents
1. [Database Structure Summary](#Database-Structure-Summary)
2. [Database Creation Description](#Database-Creation-Description)
3. [Database Schema](#Database-Schema)
4. [Entity Relationship Diagram](#Entity-Relationship-Diagram)
5. [Database Normalization](#Database-Normalization)
6. [Running the Database](#Running-the-Database)


# Database Structure Summary
Marketplace was chosen as the business for which the database is being designed. The database consists of several tables, each representing a different entity. 

1. ### [Customers](#Customers): Stores information about the customers.

2. ### [Addresses](#Addresses): Stores the addresses of the customers.

3. ### [Payment Methods](#Payment-Methods): Stores the payment methods of the customers.

4. ### [Sellers](#Sellers): Stores information about the sellers.

5. ### [Orders](#Orders): Stores information about the orders.

6. ### [Items](#Items): Stores information about the items.

7. ### [Customer Item Cart](#Customer-Item-Cart): Stores information about the items in the customer's cart.

8. ### [Customer Item Wish](#Customer-Item-Wish): Stores information about the items in the customer's wish list.

9. ### [Rates](#Rates): Stores the ratings and comments given by customers to items.

10. ### [Order Item](#Order-Item): Stores information about the connection between items and order.

11. ### [Warehouses](#Warehouses): Stores information about the warehouses.

12. ### [Warehouse Items](#Warehouse-Items): Stores information about the items in a warehouse.

Each table has a primary key, which uniquely identifies each record in the table. There are also several foreign key relationships between the tables, which establish links between related data across tables. For example, the `customer_id` in the `Addresses` table is a foreign key that references the `id` in the `Customers` table. This means that each address is associated with a specific customer.

This database is designed to support a variety of operations for an e-commerce platform, including customer management, order processing, item management, and warehouse management.

# Database Creation Description

- ## Customers
  [Back to summary](#Database-Structure-Summary)
    ```postgresql
    CREATE TABLE "customers" (
        "id" integer PRIMARY KEY,
        "name" varchar,
        "surname" varchar,
        "login" varchar,
        "password" varchar,
        "age" int,
        "verified" boolean,
        "created_at" timestamp,
        "cart_price" float
    );
    ```
    ### We Started from creating table `customers` it contains information about customers. Then we decided that we want to store delivery addresses and payment methods of customers. As one customer can have more than one addresses and payment method we created two more tables `addresses` and `payment_methods` which are connected to `customers` table by foreign keys.

- ## Addresses
  [Back to summary](#Database-Structure-Summary)
    ```postgresql
    CREATE TABLE "addresses" (
        "id" integer PRIMARY KEY,
        "customer_id" integer,
        "address" varchar
    );
    ```
    ### Table `addresses` contains information about delivery address of customers. It is connected to `customers` table by foreign key `customer_id`.

- ## Payment Methods
  [Back to summary](#Database-Structure-Summary)
    ```postgresql
    CREATE TABLE "payment_methods" (
        "customer_id" integer,
        "card_number" varchar,
        "cvc" int,
        "card_holder" varchar,
        "valid_until" varchar,
        PRIMARY KEY ("customer_id", "card_number")
    );
    ```
    ### Table `payment_methods` contains information about payment methods of customers. It is connected to `customers` table by foreign key `customer_id` & `card_number`.

- ## Sellers
  [Back to summary](#Database-Structure-Summary)
    ```postgresql
    CREATE TABLE "sellers" (
        "id" integer PRIMARY KEY,
        "title" varchar,
        "login" varchar,
        "password" varchar,
        "rate" float,
        "created_at" timestamp,
        "address" varchar,
        "card_number" varchar,
        "total_sales" float
    );
    ```
    ### Then we implemented Table `sellers` that contains information about sellers. It is connected to `items` table by foreign key `id`. We decided to separate sellers from customers because they have very different roles in the system and set of properties.

- ## Items
    [Back to summary](#Database-Structure-Summary)
    ```postgresql
    CREATE TABLE "items" (
        "id" integer PRIMARY KEY,
        "title" varchar,
        "category" enum,
        "rate" float,
        "description" text,
        "seller_id" integer,
        "cost" float,
        "created_at" timestamp
    );
    ```
    ### Table `items` contains information about items that are present in the store. It is connected to `sellers` table by foreign key `seller_id`.

- ## Customer Item Cart
    [Back to summary](#Database-Structure-Summary)
    ```postgresql
    CREATE TABLE "customer_item_cart" (
        "customer_id" integer,
        "item_id" integer,
        "amount" int,
        PRIMARY KEY ("customer_id", "item_id")
    );
    ```
    ### Table `customer_item_cart` contains information about items that are present in the cart of customers. It is connected to `customers` and `items` tables by foreign keys `customer_id` and `item_id`. By adding item to cart we connect customer with item. Primary key constraint is added to `customer_id` and `item_id` to avoid duplication of product in one cart. 
  
- ## Customer Item Wish
  [Back to summary](#Database-Structure-Summary)
    ```postgresql
    CREATE TABLE "customer_item_wish" (
        "customer_id" integer,
        "item_id" integer,
        PRIMARY KEY ("customer_id", "item_id")
    );
    ```
  ### Table `customer_item_wish` contains information about items that are present in the wish list of customers. It works the same way as `customer_item_cart` table.

- ## Rates
  [Back to summary](#Database-Structure-Summary)
    ```postgresql
    CREATE TABLE "rates" (
        "customer_id" integer,
        "item_id" integer,
        "rate" float,
        "body" text,
        PRIMARY KEY ("customer_id", "item_id")
    );
    ```
    ### Table `rates` contains information about rates given by customers to items. It is connected to `customers` and `items` tables by foreign keys `customer_id` and `item_id`.

- ## Orders
  [Back to summary](#Database-Structure-Summary)
    ```postgresql
    CREATE TABLE "orders" (
        "id" integer PRIMARY KEY,
        "customer_id" integer,
        "delivery_address" varchar,
        "status" enum,
        "total_cost" float,
        "created_at" timestamp,
        "comment" text
    );
    ```
    ### Table `oders` contains information about orders. It is connected to `customers` table by foreign key `customer_id`.

- ## Order Item
  [Back to summary](#Database-Structure-Summary)
    ```postgresql
    CREATE TABLE "order_item" (
        "order_id" integer,
        "item_id" integer,
        "amount" int,
        PRIMARY KEY ("order_id", "item_id")
    );
    ```
  ### Table `order_item` contains information about items that are present in the order. It is connected to `Orders` and `Items` tables by foreign keys `order_id` and `item_id`. We made it a separate table because one order can contain multiple items.

- ## Warehouses
  [Back to summary](#Database-Structure-Summary)
    ```postgresql
    CREATE TABLE "warehouses" (
        "id" integer PRIMARY KEY,
        "title" varchar,
        "address" varchar
    );
    ```
    ### Table `warehouses` contains information about warehouses. This table was made in purpose to store different items in different warehouses.

- ## Warehouse Items
  [Back to summary](#Database-Structure-Summary)
    ```postgresql
    CREATE TABLE "warehouse_items" (
        "warehouse_id" integer,
        "item_id" integer,
        "amount" int,
        PRIMARY KEY ("warehouse_id", "item_id")
    );
    ```
    ### Table `warehouse_items` contains information about items that are present in the warehouse. It is connected to `warehouses` and `items` tables by foreign keys `warehouse_id` and `item_id`. We made it a separate table because one warehouse can contain multiple items.

# Database Schema
### Full-fledged scheme of the database on which the working prototype was created in the future.
![img.png](./assets/images/Schema.png)
### Here is the schema of the database that was created for the prototype. It is autogenerated from working instance of postgres database.
![postgres@localhost.png](./assets/images/postgres@localhost.png)
# Entity Relationship Diagram
### This digram shows the relationship between entities using Chen's notation.
![img.png](./assets/images/ERD.png)

# Database Normalization
During the design of the database, we followed these steps:
## 1. First Normal Form (1NF):
### Atomic Value:
#### Each cell in the table must contain only a single value, and that value must be atomic, i.e., it cannot be divided further.
### Unique Column Names:
#### Each column in a table must have a unique name. This ensures clarity and avoids ambiguity.
### No Repeating Groups:
#### No Repeating Groups: Each column should have a single value corresponding to each row. Avoid repeating groups or arrays in a single column.
## 2. Second Normal Form (2NF):
### Meets 1NF:
#### The table must be in first normal form.
### No Partial Dependencies:
#### Each non-prime attribute (i.e., not part of any candidate key) must be fully functionally dependent on the entire primary key, not just part of it. This means that every attribute in the table must be functionally dependent on the primary key.
## 3. Third Normal Form (3NF):
###  Meets 2NF:
#### The table must already be in second normal form.
### No Transitive Dependencies:
#### There should be no transitive dependencies. This means that no non-prime attribute should be dependent on another non-prime attribute. Every non-prime attribute must be directly dependent on the primary key.
## In summary:
### 1NF:
#### Make sure every cell has a single value, columns have unique names, and avoid repeating groups.
### 2NF:
#### Ensure it meets 1NF and there are no partial dependencies, meaning every attribute is fully dependent on the primary key.
### 3NF:
#### Ensure it meets 2NF and there are no transitive dependencies, meaning every non-prime attribute is directly dependent on the primary key.


# Running the Database
### To run the database you need to run postgres database on your local machine. You can do it by running the following command in the terminal:
  ```sh
    docker-compose up
  ```
### After that you can try it out using `db_test.py` just run it and it will create the database and fill it with some data.(P. S. to run `db_test.py` you need to have python 3.12 installed on your machine and also you need to install dependencies of the project by running `pip install poetry` and after that `poetry install` in the terminal)

### If you want to check the database stats you can go on <link>http://localhost:54321 there will be pgadmin page login and password are `admin@de.com` and `admin` respectively. After that you will need to add server click on add then specify host as postgres_db, port as 5432, username as postgres, password as postgres. Then you can see the database and its tables by clicking on `your server` -> `databases` -> `public` -> `tables`.