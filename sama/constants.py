""" Constants module """

from enum import Enum

DB_FILENAME: str = "sama.db"
DB_FOLDER: str = ".sama"


class CommandHelp(str, Enum):
    """
    Short description of commands to show on help section.
    """

    INVENTORY: str = "Show a list of products in stock."
    SALES: str = "Show a list of sales."
    SELL: str = "Record a sale."
    ADD: str = "Add a product to the inventory."
    REPORT: str = "Show report of sales."
    RESTOCK: str = "Update inventory."


class ArgsHelp(str, Enum):
    """
    Short description of arguments required for commands.
    """

    NAME: str = "Name the item"
    TAG: str = "Tag or category"
    COST: str = "Cost of item"
    PRICE: str = "Sell price"
    QTY: str = "Quantity"
    DATE: str = "Date. E.g: YYYY-MM-DD"
    PRODUCT: str = "Select product"
