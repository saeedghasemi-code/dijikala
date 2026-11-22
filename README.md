# 🛍️ DijiKala - Simple Marketplace

A simple online marketplace built with Django, where sellers can create stores and add products, and customers can browse, add to cart, and make demo purchases.

## 🚀 Technologies Used
- **Backend:** Django (Python)
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS
- **Authentication:** Django Built-in Auth

## ⚙️ Features
- Landing page showing latest products
- Store detail pages
- Seller Panel (Create Store, Add Products)
- Customer Panel (Wallet Balance, Order History)
- Shopping Cart & Checkout logic (Deducts from customer, adds to seller)
- Modular settings (`base.py` and `dev.py`) with `.env` for security.

## 🛠️ How to Run
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate it and install dependencies: `pip install -r requirements.txt`
4. Create a `.env` file and add your PostgreSQL credentials.
5. Run migrations: `python manage.py migrate`
6. Start the server: `python manage.py runserver`
