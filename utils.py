import json
import os
from datetime import datetime
import hashlib


# Default inventory file name
INVENTORY_FILE = 'inventory.json'


def hash_password(password):
    """Hash a password using SHA-256 with salt"""
    # Create a salt using the current time and password
    salt = "inventory_salt_2025"  # Fixed salt - in production use random salt
    salted_password = password + salt
    return hashlib.sha256(salted_password.encode()).hexdigest()


def verify_password(password, hashed_password):
    """Verify a password against its hash"""
    return hash_password(password) == hashed_password


def load_inventory():
    """
    Load inventory data from the JSON file.
    If the file doesn't exist, create an empty one.
    """
    # Check if the inventory file exists
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                # Convert string keys back to integers (if needed)
                return {int(k): v for k, v in data.items()}
            except json.JSONDecodeError:
                # If there's an error decoding the JSON, return empty dict
                return {}
    else:
        # Create the file with an empty inventory if it doesn't exist
        save_inventory({})
        return {}


def save_inventory(inventory):
    """
    Save inventory data to the JSON file.

    Args:
        inventory (dict): Dictionary containing all inventory items
    """
    with open(INVENTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(inventory, f, indent=2)


def add_product(name, category, quantity, price):
    """
    Add a new product to the inventory.

    Args:
        name (str): Name of the product
        category (str): Category of the product
        quantity (int): Quantity of the product
        price (float): Price of the product

    Returns:
        tuple: (success (bool), message (str))
    """
    # Validate inputs
    if not name.strip():
        return False, "Product name cannot be empty"

    if not category.strip():
        return False, "Category cannot be empty"

    try:
        quantity = int(quantity)
        if quantity < 0:
            return False, "Quantity cannot be negative"
    except ValueError:
        return False, "Quantity must be a valid number"

    try:
        price = float(price)
        if price < 0:
            return False, "Price cannot be negative"
    except ValueError:
        return False, "Price must be a valid number"

    # Load current inventory
    inventory = load_inventory()

    # Find a new ID for the product (simple approach: use max ID + 1)
    if inventory:
        new_id = max(int(k) for k in inventory.keys()) + 1
    else:
        new_id = 1

    # Add new product
    inventory[new_id] = {
        "name": name.strip(),
        "category": category.strip(),
        "quantity": quantity,
        "price": round(price, 2),
        "date_added": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    }

    # Save the updated inventory
    save_inventory(inventory)

    return True, f"Product '{name}' added successfully with ID {new_id}"


def update_product_quantity(product_id, new_quantity):
    """
    Update the quantity of a product in the inventory.

    Args:
        product_id (int): ID of the product to update
        new_quantity (int): New quantity for the product

    Returns:
        tuple: (success (bool), message (str))
    """
    # Validate inputs
    try:
        product_id = int(product_id)
        new_quantity = int(new_quantity)
        if new_quantity < 0:
            return False, "Quantity cannot be negative"
    except ValueError:
        return False, "Both product ID and quantity must be valid numbers"

    # Load current inventory
    inventory = load_inventory()

    # Check if product exists
    if product_id not in inventory:
        return False, f"Product with ID {product_id} does not exist"

    # Update quantity
    inventory[product_id]["quantity"] = new_quantity

    # Save the updated inventory
    save_inventory(inventory)

    return True, f"Product ID {product_id} quantity updated to {new_quantity}"


def delete_product(product_id):
    """
    Delete a product from the inventory.

    Args:
        product_id (int): ID of the product to delete

    Returns:
        tuple: (success (bool), message (str))
    """
    # Validate input
    try:
        product_id = int(product_id)
    except ValueError:
        return False, "Product ID must be a valid number"

    # Load current inventory
    inventory = load_inventory()

    # Check if product exists
    if product_id not in inventory:
        return False, f"Product with ID {product_id} does not exist"

    # Store product name for the success message
    product_name = inventory[product_id]["name"]

    # Delete the product
    del inventory[product_id]

    # Save the updated inventory
    save_inventory(inventory)

    return True, f"Product '{product_name}' deleted successfully"


def get_all_products():
    """
    Get all products in the inventory.

    Returns:
        list: List of dictionaries containing product information
    """
    inventory = load_inventory()
    products_list = []

    for product_id, details in inventory.items():
        product_info = {
            "ID": int(product_id),
            "Name": details["name"],
            "Category": details["category"],
            "Quantity": details["quantity"],
            "Price": details["price"],
            "Value": round(details["quantity"] * details["price"], 2),
            "Date Added": details["date_added"],
            "Status": "Low Stock" if details["quantity"] < 5 else "In Stock"
        }
        products_list.append(product_info)

    return products_list


def increase_stock(product_id, amount):
    """
    Increase the stock of a product.

    Args:
        product_id (int): ID of the product
        amount (int): Amount to increase the stock by

    Returns:
        tuple: (success (bool), message (str))
    """
    # Validate inputs
    try:
        product_id = int(product_id)
        amount = int(amount)
        if amount <= 0:
            return False, "Amount to increase must be positive"
    except ValueError:
        return False, "Both product ID and amount must be valid numbers"

    # Load current inventory
    inventory = load_inventory()

    # Check if product exists
    if product_id not in inventory:
        return False, f"Product with ID {product_id} does not exist"

    # Increase the quantity
    current_quantity = inventory[product_id]["quantity"]
    new_quantity = current_quantity + amount

    inventory[product_id]["quantity"] = new_quantity

    # Save the updated inventory
    save_inventory(inventory)

    return True, f"Stock increased. Product ID {product_id}: {current_quantity} → {new_quantity}"


def decrease_stock(product_id, amount):
    """
    Decrease the stock of a product, preventing negative stock.

    Args:
        product_id (int): ID of the product
        amount (int): Amount to decrease the stock by

    Returns:
        tuple: (success (bool), message (str))
    """
    # Validate inputs
    try:
        product_id = int(product_id)
        amount = int(amount)
        if amount <= 0:
            return False, "Amount to decrease must be positive"
    except ValueError:
        return False, "Both product ID and amount must be valid numbers"

    # Load current inventory
    inventory = load_inventory()

    # Check if product exists
    if product_id not in inventory:
        return False, f"Product with ID {product_id} does not exist"

    # Check if there's enough stock to decrease
    current_quantity = inventory[product_id]["quantity"]
    if current_quantity < amount:
        return False, f"Not enough stock to decrease. Current: {current_quantity}, Requested: {amount}"

    # Decrease the quantity
    new_quantity = current_quantity - amount
    inventory[product_id]["quantity"] = new_quantity

    # Save the updated inventory
    save_inventory(inventory)

    return True, f"Stock decreased. Product ID {product_id}: {current_quantity} → {new_quantity}"


def search_products_by_name(search_term):
    """
    Search products by name.

    Args:
        search_term (str): Term to search for in product names

    Returns:
        list: List of matching products
    """
    all_products = get_all_products()
    search_term = search_term.lower().strip()

    matching_products = [product for product in all_products
                         if search_term in product["Name"].lower()]

    return matching_products


def filter_products_by_category(category):
    """
    Filter products by category.

    Args:
        category (str): Category to filter by

    Returns:
        list: List of products in the specified category
    """
    all_products = get_all_products()
    category = category.lower().strip()

    matching_products = [product for product in all_products
                         if category == product["Category"].lower()]

    return matching_products


def get_low_stock_items(threshold=5):
    """
    Get products with low stock (quantity below threshold).

    Args:
        threshold (int): Threshold for low stock (default 5)

    Returns:
        list: List of low stock products
    """
    all_products = get_all_products()
    low_stock_products = [product for product in all_products
                          if product["Quantity"] < threshold]

    return low_stock_products


def get_total_inventory_value():
    """
    Calculate the total value of the inventory.

    Returns:
        float: Total value of all products in inventory
    """
    all_products = get_all_products()
    total_value = sum(product["Value"] for product in all_products)

    return total_value