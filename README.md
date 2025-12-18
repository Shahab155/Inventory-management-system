# 📦 Inventory Management System

A simple and intuitive inventory management application built with Python and Streamlit that allows you to efficiently manage your product inventory.

## ✨ Features

- **Add Products**: Easily add new products with name, category, quantity, and price
- **View Inventory**: See all products with detailed information and statistics
- **Update Stock**: Increase or decrease product quantities with simple controls
- **Delete Products**: Remove products from your inventory when needed
- **Low Stock Alerts**: Automatic notifications when items fall below 5 units
- **Export Data**: Download inventory as CSV for record keeping
- **Real-time Statistics**: Track total products, inventory value, and low stock items

## 🛠️ Tech Stack

- **Python**: Core programming language
- **Streamlit**: Web framework for creating the user interface
- **Pandas**: Data manipulation and export capabilities
- **JSON**: Local storage for inventory data

## 📋 Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.6 or higher
- pip (Python package installer)

## 🚀 Installation

1. Clone or download this repository to your local machine
2. Navigate to the project directory:
   ```bash
   cd inventory_app
   ```
3. Install the required dependencies:
   ```bash
   pip install streamlit pandas
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## 📖 Usage

Once the application is running, you can access it through your web browser at `http://localhost:8501`.

### Navigation Menu

The sidebar contains the main navigation options:

- **Home**: Overview dashboard showing inventory statistics and low stock alerts
- **Add Product**: Form to add new products to your inventory
- **View Inventory**: Full inventory list with filtering and export options
- **Update Stock**: Adjust product quantities (increase or decrease)
- **Delete Product**: Remove products from your inventory

### Key Functions

- **Adding Products**: Enter product name, category, quantity, and price to add new items
- **Managing Stock**: Select products from a dropdown and specify amounts to increase/decrease
- **Low Stock Monitoring**: Items with less than 5 units are highlighted for easy identification
- **Data Export**: Download your inventory as a CSV file for external use

## 🗂️ File Structure

```
inventory_app/
├── app.py              # Main Streamlit application
├── utils.py            # Utility functions for inventory operations
├── inventory.json      # Local storage file for inventory data
└── README.md           # Project documentation
```

## 💾 Data Storage

The application stores inventory data in `inventory.json` file in the following format:

```json
{
  "product_id": {
    "name": "Product Name",
    "category": "Category",
    "quantity": 10,
    "price": 15.00,
    "date_added": "YYYY-MM-DD HH:MM:SS"
  }
}
```

## 🔧 Contributing

Feel free to fork this repository, make improvements, and submit pull requests. Issues and suggestions are welcome!

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Developer

Built with 💖 by **Shahab Ud Din**

---

_Happy Inventory Management! 🎉_