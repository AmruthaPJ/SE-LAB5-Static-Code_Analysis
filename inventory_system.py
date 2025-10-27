"""
Simple inventory management system script.

This module provides basic functions to manage an in-memory stock
database, including adding, removing, and querying items.
It also supports saving to and loading from a JSON file.
"""

import json
from datetime import datetime

# Global variable
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """
    Adds a specified quantity of an item to the stock.

    Args:
        item (str): The name of the item to add.
        qty (int): The quantity to add.
        logs (list, optional): A list to append log messages to.
    """
    # Fix (W0102): Dangerous default value [] as argument
    if logs is None:
        logs = []

    # Added input validation (per lab suggestion)
    if not isinstance(item, str) or item == "default":
        # Fix (E501): Line too long
        print(f"Error: Invalid item name '{item}'. "
              "Must be a non-default string.")
        return
    # FIX: Prevent negative quantities
    if not isinstance(qty, int) or qty < 0:
        # Fix (E501): Line too long
        print(f"Error: Invalid quantity '{qty}' for {item}. "
              "Must be a non-negative integer.")
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    # Fix (C0209): Formatting with % instead of f-string
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item, qty):
    """
    Removes a specified quantity of an item from the stock.
    Will not allow stock to go below zero.

    Args:
        item (str): The name of the item to remove.
        qty (int): The quantity to remove.
    """
    # Added input validation (per lab suggestion)
    if not isinstance(item, str):
        print(f"Error: Invalid item name '{item}'. Must be a string.")
        return
    # FIX: Prevent negative quantities
    if not isinstance(qty, int) or qty < 0:
        print(f"Error: Invalid quantity '{qty}' for {item}. "
              "Must be a non-negative integer.")
        return

    # FIX: Rewritten logic to prevent negative stock and be safer
    current_qty = stock_data.get(item, 0)

    if item not in stock_data:
        print(f"Warning: Cannot remove {item}, "
              "not found in stock.")
    elif qty > current_qty:
        print(f"Warning: Cannot remove {qty} of {item}. "
              f"Only {current_qty} in stock.")
    else:
        stock_data[item] -= qty
        if stock_data[item] == 0:
            del stock_data[item]


def get_quantity(item):
    """
    Gets the current quantity of a specific item.

    Args:
        item (str): The name of the item to query.

    Returns:
        int: The quantity of the item, or 0 if not found.
    """
    # Fix: Original code would crash if item doesn't exist.
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """
    Loads the stock data from a JSON file.

    Args:
        file (str): The name of the file to load from.
    """
    # Fix (W0603): Suppress 'Using global statement' warning
    # This is an accepted part of this simple script's design.
    # pylint: disable=global-statement
    global stock_data
    try:
        # Fix (R1732): Using open without 'with'
        # Fix (W1514): Using open without specifying encoding
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)

        # FIX: Sanitize loaded data to remove negative/invalid values
        # We must create a copy of the keys to iterate over
        # as we may be deleting items from the dictionary.
        items_to_check = list(stock_data.keys())
        for item in items_to_check:
            value = stock_data[item]
            if not isinstance(value, int) or value < 0:
                print(f"Warning: Found and removed invalid data for '{item}' "
                      f"({value}) from inventory file.")
                del stock_data[item]

    except FileNotFoundError:
        print(f"Warning: {file} not found. Starting with empty inventory.")
        stock_data = {}
    except json.JSONDecodeError:
        # Fix (E501): Line too long
        print(f"Error: Could not decode {file}. "
              "Starting with empty inventory.")
        stock_data = {}


def save_data(file="inventory.json"):
    """
    Saves the current stock data to a JSON file.

    Args:
        file (str): The name of the file to save to.
    """
    # Fix (R1732): Using open without 'with'
    # Fix (W1514): Using open without specifying encoding
    with open(file, "w", encoding="utf-8") as f:
        # Use json.dump for writing to file, added indent for readability
        json.dump(stock_data, f, indent=4)


def print_data():
    """Prints a formatted report of all items and their quantities."""
    print("--- Items Report ---")
    # Use .items() for a cleaner loop
    for item, quantity in stock_data.items():
        print(f"{item} -> {quantity}")
    print("----------------------")


def check_low_items(threshold=5):
    """
    Returns a list of items below a given stock threshold.

    Args:
        threshold (int): The stock level to check against.

    Returns:
        list: A list of item names below the threshold.
    """
    result = []
    # Use .items() for a cleaner loop
    for item, quantity in stock_data.items():
        if quantity < threshold:
            result.append(item)
    return result


def main():
    """Main function to run the inventory operations."""

    # 1. LOAD first to get the data from the last run
    # This will now also sanitize the data.
    load_data()

    # 2. Make your changes to the loaded data
    # Fix (C0103): All function calls updated to snake_case naming
    add_item("apple", 10)
    # This call will now print an error and do nothing,
    # as per our new validation in add_item()
    add_item("banana", -2)
    add_item(123, "ten")  # Invalid types, will now be caught by validation
    remove_item("apple", 3)
    remove_item("orange", 1)  # Will now be caught by new logic
    # Fix (E261): Added two spaces before inline comment
    remove_item("apple", 1000)  # Test: Will now print a warning

    # 3. Print the results
    print(f"Apple stock: {get_quantity('apple')}")
    # Fix (E261, E501): Moved long comment to its own line
    # Added to demo get_quantity fix for non-existent items
    print(f"Orange stock: {get_quantity('orange')}")
    print(f"Low items: {check_low_items()}")

    # 4. SAVE the new, updated data at the end
    save_data()

    # 5. Print the final report from the saved data
    print_data()

    # Fix (B307, W0123): Removed dangerous eval()
    print("--- Script Finished ---")


# Standard Python practice to run main()
if __name__ == "__main__":
    main()
