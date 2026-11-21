
from decimal import Decimal

from sqlalchemy import select

from app.database import SessionLocal
from app.models.product import Category, Product


def seed_database():
    db = SessionLocal()

    try:
        # Create categories if they do not exist
        categories_data = [
            {
                "name": "Electronics",
                "description": "Electronic devices and accessories"
            },
            {
                "name": "Computers",
                "description": "Laptops and computer accessories"
            },
            {
                "name": "Accessories",
                "description": "Useful electronic accessories"
            }
        ]

        categories = {}

        for item in categories_data:
            category = db.scalar(
                select(Category).where(Category.name == item["name"])
            )

            if category is None:
                category = Category(**item)
                db.add(category)
                db.flush()

            categories[item["name"]] = category

        # Create products if they do not exist
        products_data = [
            {
                "name": "Laptop Pro 15",
                "description": "High performance laptop for professionals",
                "price": Decimal("1250.00"),
                "stock": 15,
                "category_id": categories["Computers"].id
            },
            {
                "name": "Wireless Mouse",
                "description": "Ergonomic wireless mouse",
                "price": Decimal("25.50"),
                "stock": 50,
                "category_id": categories["Accessories"].id
            },
            {
                "name": "Smartphone X",
                "description": "Modern smartphone with advanced features",
                "price": Decimal("899.99"),
                "stock": 20,
                "category_id": categories["Electronics"].id
            },
            {
                "name": "Mechanical Keyboard",
                "description": "Mechanical keyboard for daily use",
                "price": Decimal("75.00"),
                "stock": 30,
                "category_id": categories["Accessories"].id
            },
            {
                "name": "Gaming Laptop",
                "description": "Laptop designed for gaming",
                "price": Decimal("1800.00"),
                "stock": 8,
                "category_id": categories["Computers"].id
            }
        ]

        for item in products_data:
            existing_product = db.scalar(
                select(Product).where(Product.name == item["name"])
            )

            if existing_product is None:
                db.add(Product(**item))

        db.commit()

        print("Database seeded successfully!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
