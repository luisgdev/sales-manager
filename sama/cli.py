""" Command Line Interface """

from time import strftime
from typing import Optional

import inquirer
import typer

from sama import __app_name__, __version__, model, view
from sama.constants import ArgsHelp, CommandHelp, Prompt
from sama.model import Product, Sale

app = typer.Typer(no_args_is_help=True)
stock_app = typer.Typer()
store_app = typer.Typer()
app.add_typer(stock_app, name="item", help=CommandHelp.STOCK, no_args_is_help=True)
app.add_typer(store_app, name="sale", help=CommandHelp.STORE, no_args_is_help=True)

confirm_form = [
    inquirer.List(
        name="save",
        message=Prompt.CONFIRM,
        choices=("YES", "NO"),
    )
]


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


@app.command(name="reports", help=CommandHelp.REPORT)
def report() -> None:
    """
    Show a report of previous sales, inventory and profit. \f  # TODO
    :return: None
    """


@store_app.command(name="list", help=CommandHelp.LIST_SALES)
def list_sales() -> None:
    """
    List sales. \f
    :return: None
    """
    sales = model.get_all_sales()
    if sales:
        view.show_sales(sales=sales)
    else:
        view.rich_print("[green]There is no sale record.")


@store_app.command(name="add", help=CommandHelp.ADD_SALE)
def create_sale() -> None:
    """
    Sell a product. \f
    :return: None
    """
    date = strftime("%Y-%m-%d")
    view.print_markdown("# Register a sale")
    choices = model.get_all_products()
    choices = list(filter(lambda x: x.qty > 0, choices))
    form = inquirer.prompt(
        questions=[
            inquirer.List(name="product", message=ArgsHelp.ITEM, choices=choices),
            inquirer.Text(name="price", message=ArgsHelp.PRICE),
            inquirer.Text(name="qty", message=ArgsHelp.QTY),
            inquirer.Text(name="date", message=ArgsHelp.DATE.format(date)),
        ]
    )
    date = date if not form["date"] else form["date"]
    product = form["product"]
    sale = Sale(
        date=date,
        product_id=product.id,
        product_name=product.name,
        sell_price=float(form["price"]),
        cost=float(product.cost),
        qty=int(form["qty"]),
    )
    view.rich_print("[green]The following sale will be created.")
    view.show_full_sale(sale)
    confirmation = inquirer.prompt(questions=confirm_form)
    if confirmation["save"] == "YES":
        product.qty = product.qty - sale.qty
        model.update_product(product)
        model.add_sale(sale)
    if confirmation["save"] == "NO":
        view.rich_print(Prompt.NO_CHANGE)


@store_app.command(name="update", help=CommandHelp.UPDATE_SALE)
def update_sale() -> None:
    """
    Update an existing sale record. \f  # TODO
    :return: None
    """
    view.print_markdown("# Update a sale record")
    choices = model.get_all_sales()
    view.show_sales(sales=choices)
    form = inquirer.prompt(
        questions=[
            inquirer.List(name="record", message=ArgsHelp.SALE, choices=choices),
        ]
    )
    record = form["record"]
    view.rich_print("Type new values of enter to leave as is.")
    new_value = inquirer.prompt(
        questions=[
            inquirer.Text(
                name="price", message=ArgsHelp.PRICE + f"({record.sell_price})"
            ),
            inquirer.Text(name="qty", message=ArgsHelp.QTY + f"({record.qty})"),
            inquirer.Text(name="date", message=f"Date ({record.date})"),
        ]
    )
    if not any(
        (
            new_value["date"],
            new_value["price"],
            new_value["qty"],
        )
    ):
        view.rich_print(Prompt.NO_CHANGE)
        return
    record.sell_price = (
        record.sell_price if not new_value["price"] else new_value["price"]
    )
    record.qty = record.qty if not new_value["qty"] else new_value["qty"]
    record.date = record.date if not new_value["date"] else new_value["date"]
    view.show_full_sale(record)
    confirmation = inquirer.prompt(questions=confirm_form)
    if confirmation["save"] == "YES":
        model.update_sale(record)
    if confirmation["save"] == "NO":
        view.rich_print(Prompt.NO_CHANGE)


@store_app.command(name="delete", help=CommandHelp.DELETE_SALE)
def delete() -> None:
    """
    Delete an existing sale record. \f
    :return: None
    """
    choices = model.get_all_sales()
    view.show_sales(sales=choices)
    form = inquirer.prompt(
        questions=[
            inquirer.List(name="record", message=ArgsHelp.SALE, choices=choices),
        ]
    )
    view.rich_print("[red]The following record will be deleted.")
    view.show_full_sale(form["record"])
    confirmation = inquirer.prompt(questions=confirm_form)
    if confirmation["save"] == "YES":
        model.delete_sale(sale=form["record"])
    if confirmation["save"] == "NO":
        view.rich_print(Prompt.NO_CHANGE)


@stock_app.command(name="list", help=CommandHelp.LIST_ITEMS)
def list_products() -> None:
    """
    List products in stock. \f
    :return: None
    """
    products = model.get_all_products()
    if products:
        view.show_products(products=products)
    else:
        view.rich_print("[green]There is no product in stock")


@stock_app.command(name="add", help=CommandHelp.ADD_ITEM)
def create_product() -> None:
    """
    Add a product to inventory. \f
    :return: None
    """
    view.print_markdown("# Add a product")
    form = inquirer.prompt(
        questions=[
            inquirer.Text(name="name", message=ArgsHelp.NAME),
            inquirer.Text(name="tag", message=ArgsHelp.TAG),
            inquirer.Text(name="cost", message=ArgsHelp.COST),
            inquirer.Text(name="price", message=ArgsHelp.PRICE),
            inquirer.Text(name="qty", message=ArgsHelp.QTY),
        ]
    )
    product = Product(**form)
    view.rich_print("[green]The following product will be created.")
    view.show_full_product(product)
    confirmation = inquirer.prompt(questions=confirm_form)
    if confirmation["save"] == "YES":
        view.rich_print(model.add_product(product=Product(**form)))
    if confirmation["save"] == "NO":
        view.rich_print(Prompt.NO_CHANGE)


@stock_app.command(name="update", help=CommandHelp.UPDATE_ITEM)
def update_product() -> None:
    """
    Update an existing product. \f
    :return: None
    """
    view.print_markdown("# Update a product")
    choices = model.get_all_products()
    view.show_products(products=choices)
    form = inquirer.prompt(
        questions=[
            inquirer.List(name="product", message=ArgsHelp.ITEM, choices=choices),
        ]
    )
    product = form["product"]
    view.rich_print("Type new values OR enter to leave as is.")
    new_value = inquirer.prompt(
        questions=[
            inquirer.Text(name="name", message=ArgsHelp.NAME + f" ({product.name})"),
            inquirer.Text(name="tag", message=ArgsHelp.TAG + f" ({product.tag})"),
            inquirer.Text(name="cost", message=ArgsHelp.COST + f" ({product.cost})"),
            inquirer.Text(name="price", message=ArgsHelp.PRICE + f" ({product.price})"),
            inquirer.Text(name="qty", message=ArgsHelp.QTY + f" ({product.qty})"),
        ]
    )
    if not any(
        (
            new_value["name"],
            new_value["tag"],
            new_value["cost"],
            new_value["price"],
            new_value["qty"],
        )
    ):
        view.rich_print(Prompt.NO_CHANGE)
        return
    product.name = product.name if not new_value["name"] else new_value["name"]
    product.tag = product.tag if not new_value["tag"] else new_value["tag"]
    product.cost = product.cost if not new_value["cost"] else new_value["cost"]
    product.price = product.price if not new_value["price"] else new_value["price"]
    product.qty = product.qty if not new_value["qty"] else new_value["qty"]
    view.show_full_product(product)
    confirmation = inquirer.prompt(questions=confirm_form)
    if confirmation["save"] == "YES":
        model.update_product(product)
    if confirmation["save"] == "NO":
        view.rich_print(Prompt.NO_CHANGE)


@stock_app.command(name="delete", help=CommandHelp.DELETE_ITEM)
def delete_product() -> None:
    """
    Delete an existing product. \f
    :return: None
    """
    view.print_markdown("# Delete a product")
    choices = model.get_all_products()
    view.show_products(products=choices)
    form = inquirer.prompt(
        questions=[
            inquirer.List(name="product", message=ArgsHelp.ITEM, choices=choices),
        ]
    )
    view.rich_print("[red]The following product will be deleted.")
    view.show_full_product(form["product"])
    confirmation = inquirer.prompt(questions=confirm_form)
    if confirmation["save"] == "YES":
        model.delete_product(form["product"])
    if confirmation["save"] == "NO":
        view.rich_print(Prompt.NO_CHANGE)
