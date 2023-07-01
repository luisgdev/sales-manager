""" Database controller module """

from pathlib import Path
from pprint import pformat
from typing import List, Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select

from sama.constants import DB_FILENAME, DB_FOLDER

DB_DIRECTORY: Path = Path(Path.home(), DB_FOLDER)
DB_DIRECTORY.mkdir(exist_ok=True, parents=True)
DB_PATH: str = str(Path(DB_DIRECTORY, DB_FILENAME))

sqlite_url = f"sqlite:///{DB_PATH}"
engine = create_engine(sqlite_url, echo=False)


class Product(SQLModel, table=True):
    """Product class."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    tag: Optional[str]
    cost: float
    price: float
    qty: int

    def __str__(self):
        """
        Representation modification.
        :return:
        """
        return f"{self.name} ({self.qty})"


class Sale(SQLModel, table=True):
    """Sale class."""

    id: Optional[int] = Field(default=None, primary_key=True)
    date: str
    product_id: int
    sell_price: float
    cost: float
    qty: int


def _verify_db() -> None:
    """Create DB if it hasn't been created yet."""
    if not Path(DB_PATH).exists():
        SQLModel.metadata.create_all(engine)


def add_product(product: Product) -> str:
    """Add product to db."""
    try:
        with Session(engine) as session:
            session.add(product)
            session.commit()
        return "Product has been saved!"
    except Exception as ex:
        return f"Error: {pformat(ex)}"


def add_sale(sale: Sale) -> str:
    """Add sale to db."""
    try:
        with Session(engine) as session:
            session.add(sale)
            session.commit()
        return "Product has been saved!"
    except Exception as ex:
        return f"Error: {pformat(ex)}"


def get_product(id_: int) -> Optional[Product]:
    """Return a product by id."""
    try:
        with Session(engine) as session:
            statement = select(Product).where(Product.id == id_)
            return session.exec(statement).one()
    except Exception as ex:
        print(f"Error: {pformat(ex)}")
        return None


def update_product(
    id_: int,
    qty: Optional[int] = None,
    name: Optional[str] = None,
    cost: Optional[float] = None,
    price: Optional[float] = None,
    tag: Optional[str] = None,
) -> Optional[Product]:
    """Update a product property."""  # TODO
    try:
        with Session(engine) as session:
            statement = select(Product).where(Product.id == id_)
            product = session.exec(statement).one()
            if qty:
                product.qty = qty
            if name:
                product.name = name
            if cost:
                product.cost = cost
            if price:
                product.price = price
            if tag:
                product.tag = tag
            session.add(product)
            session.commit()
    except Exception as ex:
        print(f"Error: {pformat(ex)}")
        return None


def get_all_products() -> Optional[List[Product]]:
    """Return all products from db."""
    try:
        with Session(engine) as session:
            statement = select(Product)
            results = session.exec(statement)
            return results.all()
    except Exception as ex:
        print(f"Error: {pformat(ex)}")
        return None


def get_all_sales() -> Optional[List[Sale]]:
    """Return all products from db."""
    try:
        with Session(engine) as session:
            statement = select(Sale)
            results = session.exec(statement)
            return results.all()
    except Exception as ex:
        print(f"Error: {pformat(ex)}")
        return None


if __name__ == "__main__":
    _verify_db()
