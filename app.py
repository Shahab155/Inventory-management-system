import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from utils import (
    add_product, update_product_quantity, delete_product, get_all_products,
    increase_stock, decrease_stock, search_products_by_name,
    filter_products_by_category, get_low_stock_items, get_total_inventory_value,
    hash_password, verify_password
)

# Load environment variables from .env file
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Inventory Management System",
    page_icon="📦",
    layout="wide"
)

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Initialize session state for form resets
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Define admin credentials (hashed)
ADMIN_USERNAME = os.getenv("ADMIN")  # Change this to your preferred username
ADMIN_PASSWORD_HASHED = hash_password("PASSWORD")  # Change this to your preferred password


def login_page():
    """Display the login page"""
    st.title("📦 Inventory Management System - Login")
    st.markdown("---")

    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.header("🔐 Admin Login")

        username = st.text_input("Username", key="username")
        password = st.text_input("Password", type="password", key="password")

        if st.button("Login", use_container_width=True):
            if not username or not password:
                st.error("❌ Please enter both username and password!")
            elif username == ADMIN_USERNAME and verify_password(password, ADMIN_PASSWORD_HASHED):
                st.session_state.authenticated = True
                st.success("✅ Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Invalid username or password!")


# Main application logic
if not st.session_state.authenticated:
    login_page()
else:
    # Title of the app
    st.title("📦 Inventory Management System")
    st.markdown("---")

    # Sidebar for logout
    with st.sidebar:
        st.header("Menu")
        page = st.selectbox(
            "Select an option:",
            ["Home", "Add Product", "View Inventory", "Update Stock", "Delete Product"]
        )

        # Add logout button in sidebar
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            st.session_state.authenticated = False
            st.rerun()

    # Main content based on selected page
    if page == "Home":
        st.header("Welcome to Inventory Management System!")
        st.write("This is a simple inventory management system built with Python and Streamlit.")
        st.write("Use the sidebar to navigate between different functions:")

        # Display some inventory stats
        all_products = get_all_products()
        total_products = len(all_products)
        total_value = get_total_inventory_value()
        low_stock_items = get_low_stock_items()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Products", total_products)
        col2.metric("Total Value ($)", f"{total_value:,.2f}")
        col3.metric("Low Stock Items", len(low_stock_items))

        # Show low stock alert if any items have low stock
        if low_stock_items:
            st.warning(f"⚠️ Warning: You have {len(low_stock_items)} item(s) with low stock (below 5 units)")
            low_stock_df = pd.DataFrame(low_stock_items)
            st.dataframe(low_stock_df, use_container_width=True, hide_index=True)

    elif page == "Add Product":
        st.header("➕ Add New Product")

        # Create form for adding a new product
        with st.form(key="add_product_form"):
            name = st.text_input("Product Name*", placeholder="Enter product name")
            category = st.text_input("Category*", placeholder="Enter category")
            quantity = st.number_input("Quantity*", min_value=0, value=0, step=1)
            price = st.number_input("Price*", min_value=0.0, value=0.0, step=0.01)

            submit_button = st.form_submit_button("Add Product")

        # Handle form submission
        if submit_button:
            # Validate required fields
            if not name.strip() or not category.strip():
                st.error("❌ Product name and category are required!")
            elif quantity < 0 or price < 0:
                st.error("❌ Quantity and price cannot be negative!")
            else:
                success, message = add_product(name, category, quantity, price)
                if success:
                    st.success(f"✅ {message}")
                    st.session_state.form_submitted = True
                else:
                    st.error(f"❌ {message}")

    elif page == "View Inventory":
        st.header("📋 View All Products")

        # Get all products
        products = get_all_products()

        if products:
            # Create DataFrame from products
            df = pd.DataFrame(products)

            # Display statistics
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Products", len(products))
            col2.metric("Total Value ($)", f"{get_total_inventory_value():,.2f}")
            col3.metric("Low Stock Items", len([p for p in products if p["Quantity"] < 5]))

            # Show DataFrame
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Option to download as CSV
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="💾 Download Inventory as CSV",
                data=csv_data,
                file_name="inventory_export.csv",
                mime="text/csv"
            )

            # Show low stock items separately if any
            low_stock = get_low_stock_items()
            if low_stock:
                st.subheader("⚠️ Low Stock Alerts")
                low_stock_df = pd.DataFrame(low_stock)
                st.dataframe(low_stock_df, use_container_width=True, hide_index=True)
        else:
            st.info("📭 No products in inventory. Add some products to get started!")

    elif page == "Update Stock":
        st.header("🔄 Update Product Stock")

        # Get all products for selection
        products = get_all_products()

        if not products:
            st.warning("No products available. Add products first before updating stock.")
        else:
            # Create product selection dropdown
            product_names = [f"{p['ID']} - {p['Name']} ({p['Category']})" for p in products]
            selected_product = st.selectbox("Select Product to Update", product_names)

            # Extract product ID from selection
            if selected_product:
                product_id = int(selected_product.split(" - ")[0])

                # Find the selected product details
                selected_product_details = next(p for p in products if p["ID"] == product_id)

                st.write(f"**Current Info:** {selected_product_details['Name']} | "
                        f"Quantity: {selected_product_details['Quantity']} | "
                        f"Price: ${selected_product_details['Price']}")

                # Operation selection (increase/decrease)
                operation = st.radio("Choose operation:", ["Increase Stock", "Decrease Stock"])

                if operation == "Increase Stock":
                    amount = st.number_input("Enter amount to add", min_value=1, value=1, step=1)
                    if st.button("Increase Stock"):
                        success, message = increase_stock(product_id, amount)
                        if success:
                            st.success(f"✅ {message}")
                        else:
                            st.error(f"❌ {message}")

                elif operation == "Decrease Stock":
                    amount = st.number_input("Enter amount to subtract", min_value=1, value=1, step=1)
                    if st.button("Decrease Stock"):
                        success, message = decrease_stock(product_id, amount)
                        if success:
                            st.success(f"✅ {message}")
                        else:
                            st.error(f"❌ {message}")

    elif page == "Delete Product":
        st.header("🗑️ Delete Product")

        # Get all products for selection
        products = get_all_products()

        if not products:
            st.warning("No products available to delete.")
        else:
            # Create product selection dropdown
            product_names = [f"{p['ID']} - {p['Name']} (Qty: {p['Quantity']})" for p in products]
            selected_product = st.selectbox("Select Product to Delete", product_names)

            # Extract product ID from selection
            if selected_product:
                product_id = int(selected_product.split(" - ")[0])

                # Show confirmation
                st.write(f"⚠️ Are you sure you want to delete the following product?")
                product_to_delete = next(p for p in products if p["ID"] == product_id)
                st.write(f"**Name:** {product_to_delete['Name']}")
                st.write(f"**Category:** {product_to_delete['Category']}")
                st.write(f"**Quantity:** {product_to_delete['Quantity']}")
                st.write(f"**Price:** ${product_to_delete['Price']}")

                if st.button("Confirm Delete", type="primary"):
                    success, message = delete_product(product_id)
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")

    # Footer
    st.markdown("---")
    st.markdown("*Inventory Management System - Built with 💖 by* **Shahab Ud Din** ")