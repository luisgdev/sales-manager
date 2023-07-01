""" Views module """
from typing import Any, List

from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

from sama import model
from sama.model import Product, Sale

console = Console()


def show_products(products: List[Product]) -> None:
    """
    Show a table with the product list.
    :param products: List of Product object.
    :return: None
    """
    if not products:
        rich_print("No products in database!")
    table = Table(show_header=True, box=box.ROUNDED, title="Inventory")
    cols = ("QTY", "NAME", "COST", "PRICE")
    for col in cols:
        table.add_column(col)
    for item in products:
        table.add_row(str(item.qty), item.name, str(item.cost), str(item.price))
    rich_print(table)


def show_sales(sales: List[Sale]) -> None:
    """
    Show a table with the sales list.
    :param sales: List of Sale object.
    :return: None
    """
    if not sales:
        rich_print("No sales in database!")
    table = Table(show_header=True, box=box.ROUNDED, title="Sales")
    cols = ("DATE", "QTY", "NAME", "PRICE", "PROFIT")
    for col in cols:
        table.add_column(col)
    for item in sales:
        product = model.get_product(id_=item.product_id)
        table.add_row(
            str(item.date),
            str(item.qty),
            product.name,
            str(item.sell_price),
            str(float(item.sell_price) - product.cost),
        )
    rich_print(table)


def print_markdown(text: str) -> None:
    """
    Print a text in markdown mode.
    :param text: String with the text to be printed.
    :return: None
    """
    console.print(Markdown(text))


def rich_print(text: Any) -> None:
    """
    Print a text in rich mode.
    :param text: Object to be printed.
    :return: None
    """
    console.print(text)


if __name__ == "__main__":
    pass
