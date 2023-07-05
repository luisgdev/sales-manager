""" Views module """
from typing import Any, List

from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

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


def show_full_product(item: Product) -> None:
    """
    Show full product info.
    :param item: Product object.
    :return: None
    """
    table = Table(show_header=True, box=box.ROUNDED)
    cols = ("ID", "QTY", "NAME", "TAG", "COST", "PRICE")
    for col in cols:
        table.add_column(col)
    table.add_row(
        str(item.id),
        str(item.qty),
        item.name,
        item.tag,
        str(item.cost),
        str(item.price),
    )
    rich_print(table)


def show_sales(sales: List[Sale]) -> None:
    """
    Show a table with the sales list.
    :param sales: List of Sale object.
    :return: None
    """
    earnings: float = 0
    if not sales:
        rich_print("No sales in database!")
    table = Table(show_header=True, box=box.ROUNDED, title="Sales")
    cols = ("ID", "DATE", "PRODUCT NAME", "QTY", "COST", "PRICE", "PROFIT")
    for col in cols:
        table.add_column(col)
    for item in sales:
        profit = (float(item.sell_price) - item.cost) * item.qty
        table.add_row(
            str(item.id),
            str(item.date),
            item.product_name,
            str(item.qty),
            str(item.cost),
            str(item.sell_price),
            f"{profit:.2f}",
        )
        earnings += profit
    rich_print(table)
    rich_print(f" * Total earned: [green]{earnings:.2f}")


def show_full_sale(entry: Sale) -> None:
    """
    Show a table with the sale record.
    :param entry: Sale object.
    :return: None
    """
    table = Table(show_header=True, box=box.ROUNDED)
    cols = ("ID", "DATE", "PRODUCT", "QTY", "COST", "PRICE")
    for col in cols:
        table.add_column(col)
    table.add_row(
        str(entry.id),
        entry.date,
        entry.product_name,
        str(entry.qty),
        str(entry.cost),
        str(entry.sell_price),
    )
    rich_print(table)


def print_markdown(text: str) -> None:
    """
    Print a text in markdown mode.
    :param text: String with the text to be printed.
    :return: None
    """
    rich_print(Markdown(text))


def rich_print(text: Any) -> None:
    """
    Print a text in rich mode.
    :param text: Object to be printed.
    :return: None
    """
    console.print(text)


if __name__ == "__main__":
    pass
