# SecureShop – Requirements and System Design

## 1. Project Overview

SecureShop is a secure e-commerce backend application developed using Python, FastAPI, SQLAlchemy, and SQLite.

The main objective is to build an e-commerce system that provides essential shopping functionalities while applying software security principles to protect user accounts, product information, and shopping cart operations.

The project focuses on preventing common web application vulnerabilities through server-side validation, secure authentication, access control, and database security.

## 2. Project Objectives

- Develop a functional e-commerce backend.
- Provide product browsing, searching, and filtering.
- Allow users to manage shopping cart items.
- Implement secure user registration and authentication.
- Protect sensitive user information.
- Prevent common attacks such as SQL Injection and IDOR.
- Apply security controls to business logic and user inputs.

## 3. Functional Requirements

### FR-01: Product Catalogue
The system shall allow users to:
- View available product categories.
- View active products.
- Search products by keyword.
- Filter products by category, price range, and stock availability.
- View individual product details.

### FR-02: Shopping Cart
The system shall allow users to:
- Create and maintain a shopping cart session.
- Add products to the cart.
- Update product quantities.
- Remove individual items.
- Clear the entire cart.
- View cart items and the total price.

### FR-03: User Registration
The system shall:
- Accept user registration details.
- Validate email addresses and password lengths.
- Prevent duplicate email registration.
- Hash passwords before storing them.
- Assign new accounts the customer role by default.

### FR-04: Email Verification
The system shall:
- Generate verification tokens.
- Store token hashes instead of raw tokens.
- Enforce token expiration.
- Prevent reuse of verification tokens.
- Allow verified users to proceed with login.

### FR-05: User Authentication
The system shall:
- Authenticate users using their email and password.
- Reject invalid credentials.
- Prevent unverified or inactive users from logging in.
- Generate JWT access tokens after successful authentication.
- Provide an authenticated user profile endpoint.

## 4. Non-Functional Requirements

### NFR-01: Security
The system shall apply secure password hashing, authentication, input validation, access control, and rate limiting.

### NFR-02: Data Integrity
The system shall maintain valid database relationships and enforce appropriate constraints.

### NFR-03: Reliability
The system shall handle invalid requests and database errors without exposing sensitive internal information.

### NFR-04: Performance
The system shall use database queries and pagination limits to support efficient product retrieval.

### NFR-05: Maintainability
The application shall use a modular structure that separates models, schemas, CRUD operations, routers, and security services.

## 5. System Architecture

SecureShop follows a layered backend architecture.

### 5.1 Presentation/API Layer
FastAPI routers expose HTTP endpoints for product catalogue, shopping cart, and authentication operations.

### 5.2 Business Logic Layer
CRUD modules and service functions implement application operations, including product management, cart calculations, user management, and email verification.

### 5.3 Data Access Layer
SQLAlchemy provides database interaction through ORM models and database sessions.

### 5.4 Database Layer
SQLite stores application data, including products, categories, users, carts, cart items, and email verification records.

### 5.5 Security Layer
Security controls include:
- Password hashing using Argon2.
- JWT-based authentication.
- Server-side input validation.
- Cart session ownership validation.
- Rate limiting.
- Secure verification token handling.

## 6. Database Design

The database contains the following main entities:

### User
Stores user account information, including email, full name, password hash, role, account status, and verification status.

### Category
Stores product category names and identifiers.

### Product
Stores product details, including name, description, price, stock quantity, category, and active status.

### Cart
Stores shopping cart sessions using a hashed session identifier.

### Cart Item
Stores the products and quantities associated with each cart.

### Email Verification
Stores hashed verification tokens, expiration timestamps, and token usage status.

### Main Relationships
- A category can contain multiple products.
- A cart can contain multiple cart items.
- A product can appear in multiple cart items.
- A user can have multiple email verification records over time.

## 7. Security Requirements

The application shall apply the following security requirements:

1. Password