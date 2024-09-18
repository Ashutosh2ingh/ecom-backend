"# ecom-backend" 

A Django-based e-commerce application designed to provide a seamless shopping experience. This application includes features for product management, user authentication, shopping cart functionality, and order processing.

## Features

- **User Authentication**: Register, login, and manage user accounts.
- **Product Management**: Browse and search for products with detailed information.
- **Shopping Cart**: Add products to the cart and proceed to checkout.
- **Order Processing**: Manage orders and track order status.
- **Admin Dashboard**: Admin interface for managing products, users, and orders.

## Technologies Used

- **Django**: Web framework for building the application.
- **SQLite/MySQL**: Database for storing application data (SQLite used for development, MySQL recommended for production).
- **Bootstrap**: Frontend framework for styling.
- **Python**: Programming language used for the backend.

## Installation

To set up and run this project locally, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Ashutosh2ingh/ecom-backend.git
   cd your-repo-name

2. **Set Up a Virtual Environment:**
    python -m venv venv
    source venv/bin/activate  
    # On Windows, use `venv\Scripts\activate`

3. **Install Dependencies:**
    pip install -r requirements.txt

4. **Configure the Database:**
    python manage.py migrate

5. **Create a Superuser:**
    python manage.py createsuperuser

6. **Run the Development Server:**
    Run the Development Server: