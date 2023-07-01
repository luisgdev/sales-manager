""" Command Line Interface """

from time import strftime
from typing import Optional

import inquirer
import typer

from sama import __app_name__, __version__, model, view
from sama.constants import ArgsHelp, CommandHelp
from sama.model import Product, Sale

app = typer.Typer()


@app.callback(invoke_without_command=True)
def main(
    _: Optional[bool] = typer.Option(
        None,
        "-v",
        "--version",
    )
) -> None:
    """
    Simple inventory and sales manager. \f
    :return: None
    """
    view.rich_print(f"{__app_name__} {__version__}")


@app.command(name="report", help=CommandHelp.REPORT)
def report() -> None:
    """
    Show a report of previous sales, inventory and profit. \f
    :return: None
    """


@app.command(name="restock", help=CommandHelp.RESTOCK)
def restock() -> None:
    """
    Update the inventory. \f
    :return: None
    """


@app.command(name="stock", help=CommandHelp.INVENTORY)
def list_products() -> None:
    """
    List products in stock. \f
    :return: None
    """
    products = model.get_all_products()
    if products:
        view.show_products(products=products)


@app.command(name="sales", help=CommandHelp.SALES)
def list_sales() -> None:
    """
    List sales. \f
    :return: None
    """
    sales = model.get_all_sales()
    if sales:
        view.show_sales(sales=sales)


@app.command(name="sell", help=CommandHelp.SELL)
def sell_product() -> None:
    """
    Sell a product. \f
    :return: None
    """
    view.print_markdown("# Register a sale")
    products = model.get_all_products()
    sale_form = [
        inquirer.List(name="product", message=ArgsHelp.PRODUCT, choices=products),
        inquirer.Text(name="price", message=ArgsHelp.PRICE),
        inquirer.Text(name="qty", message=ArgsHelp.QTY),
    ]
    date_form = [
        inquirer.List(name="value", message=ArgsHelp.DATE, choices=("TODAY", "OTHER"))
    ]
    date_set = [
        inquirer.Text(name="value", message=ArgsHelp.DATE),
    ]
    sale_info = inquirer.prompt(questions=sale_form)
    date_info = inquirer.prompt(questions=date_form)
    if date_info["value"] == "TODAY":
        date = strftime("%Y-%m-%d")
    else:
        date = inquirer.prompt(questions=date_set)["value"]
    model.update_product(
        id_=sale_info["product"].id,
        qty=int(sale_info["product"].qty) - int(sale_info["qty"]),
    )
    model.add_sale(
        Sale(
            date=date,
            product_id=sale_info["product"].id,
            sell_price=float(sale_info["price"]),
            cost=float(sale_info["product"].cost),
            qty=int(sale_info["qty"]),
        )
    )


@app.command(name="add", help=CommandHelp.ADD)
def add_product() -> None:
    """
    Add a product to inventory. \f
    :return: None
    """
    view.print_markdown("# Add a product")
    product_form = [
        inquirer.Text(name="name", message=ArgsHelp.NAME),
        inquirer.Text(name="tag", message=ArgsHelp.TAG),
        inquirer.Text(name="cost", message=ArgsHelp.COST),
        inquirer.Text(name="price", message=ArgsHelp.PRICE),
        inquirer.Text(name="qty", message=ArgsHelp.QTY),
    ]
    confirm_form = [
        inquirer.List(
            name="save",
            message="Confirm to save this information.",
            choices=("YES", "NO"),
        )
    ]
    product_info = inquirer.prompt(questions=product_form)
    confirmation = inquirer.prompt(questions=confirm_form)
    if confirmation["save"] == "YES":
        view.rich_print(model.add_product(product=Product(**product_info)))
    if confirmation["save"] == "NO":
        view.rich_print("No action applied!")
