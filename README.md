# SecureShop – Software Security Project

## 1. Project Overview
SecureShop is a secure e-commerce backend API developed using Python, FastAPI, and SQLAlchemy.

The project focuses on implementing secure authentication, product management, shopping cart operations, input validation, and protection against common web application vulnerabilities.

## 2. Technologies Used
- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT Authentication
- Argon2 Password Hashing
- SlowAPI Rate Limiting
- Pytest
- HTTPX

## 3. Implemented Features

### Product Catalogue
- View product categories and products.
- Search products by keyword.
- Filter products by category, price, and stock availability.
- Validate product inputs.

### Shopping Cart
- Add products to the cart.
- Update and remove cart items.
- Calculate prices on the server side.
- Maintain separate shopping cart sessions.

### Authentication
- User registration.
- Password hashing.
- Email verification.
- User login using JWT.
- Authenticated user profile endpoint.

### Security Controls
- SQL injection protection through parameterized database queries.
- Input validation.
- Server-side price calculation.
- Cart ownership validation to prevent IDOR.
- Password hashing using Argon2.
- JWT authentication.
- Rate limiting.
- Email verification tokens are hashed and expire.
- Sensitive configuration is stored in environment variables.

## 4. Installation and Setup

Clone the repository:

```bash
git clone https://github.com/Abdulazim2/SecureShop-Software-Security.git
cd SecureShop-Software-Security
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
JWT_SECRET_KEY=replace_with_a_strong_random_secret
```

Generate a secure secret key before running the application.

## 5. Run the Application

```bash
uvicorn app.main:app --reload
```

API documentation:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health

## 6. Run Tests

```bash
pytest -v
```

## 7. Project Status

This repository contains the first working implementation for Phase 1 of the Software Security project. Additional security features, documentation, and testing will be developed as the project progresses.