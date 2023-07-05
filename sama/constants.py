""" Constants module """

from enum import Enum

DB_FILENAME: str = "sama.db"
DB_FOLDER: str = ".sama"


class CommandHelp(str, Enum):
    """
    Short description of commands to show on help section.
    """

    STOCK: str = "Manage inventory. List, Add, Update and Delete items."
    STORE: str = "Manage sales. List, Add, Update and Delete sale records."
    REPORT: str = "Show report of sales."

    ADD_SALE: str = "Add a sale record."
    UPDATE_SALE: str = "Update a sale record."
    DELETE_SALE: str = "Delete a sale record."

    ADD_ITEM: str = "Add an item."
    UPDATE_ITEM: str = "Update an item."
    DELETE_ITEM: str = "Delete an item."

    LIST_ITEMS: str = "List items in stock."
    LIST_SALES: str = "List sale records."


class ArgsHelp(str, Enum):
    """
    Short description of arguments required for commands.
    """

    NAME: str = "Name"
    TAG: str = "Tag"
    COST: str = "Cost"
    PRICE: str = "Price"
    QTY: str = "Quantity"
    DATE: str = "Date. E.g: {}"
    ITEM: str = "Select item"
    SALE: str = "Select record"


class Prompt(str, Enum):
    """
    Prompt to user.
    """

    CONFIRM: str = "Confirm to apply changes"
    NO_CHANGE: str = "[green]No change applied!"
