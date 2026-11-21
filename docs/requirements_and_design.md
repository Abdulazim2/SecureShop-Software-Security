# SecureShop – Requirements and System Design

## 1. Project Overview

SecureShop is a secure e-commerce backend application developed using Python, FastAPI, SQLAlchemy, and SQLite.

The main objective is to build an e-commerce system that provides essential shopping functionalities while applying software security principles to protect user accounts, product information, and shopping cart operations.

The project focuses on preventing common web application vulnerabilities through server-side validation, secure authentication, access control, and database security.

## 2. Project Objectives

- Develop a functional e-commerce backend.
- Provide product browsing, searching, and filtering.
- Allow clients to manage shopping cart items.
- Implement secure user registration and authentication.
- Protect sensitive user information.
- Prevent common attacks such as SQL Injection and IDOR.
- Apply security controls to business logic and user inputs.
- Establish a foundation for additional secure e-commerce features.

## 3. Functional Requirements

### FR-01: Product Catalogue

The system shall allow clients to:

- View available product categories.
- View active products.
- Search products by keyword.
- Filter products by category, price range, and stock availability.
- View individual product details.

### FR-02: Shopping Cart

The system shall allow clients to:

- Create and maintain a shopping cart session.
- Add products to the cart.
- Update product quantities.
- Remove individual items.
- Clear the entire cart.
- View cart items and the total price.

Cart sessions are maintained using a session cookie. Cart operations must be restricted to the current session.

### FR-03: User Registration

The system shall:

- Accept user registration details.
- Validate email addresses and password lengths.
- Prevent duplicate email registration.
- Hash passwords before storing them.
- Assign new accounts the customer role by default.
- Create new accounts as unverified until email verification succeeds.

### FR-04: Email Verification

The system shall:

- Generate verification tokens.
- Store token hashes instead of raw tokens.
- Enforce token expiration.
- Prevent reuse of verification tokens.
- Allow verified users to proceed with login.

**Current Implementation Note:** The verification workflow is implemented. In the development environment, the verification token is returned in the API response for testing. Actual email delivery has not yet been implemented.

### FR-05: User Authentication

The system shall:

- Authenticate users using their email and password.
- Reject invalid credentials.
- Prevent unverified or inactive users from logging in.
- Generate JWT access tokens after successful authentication.
- Provide an authenticated user profile endpoint.
- Enforce access token expiration.

## 4. Non-Functional Requirements

### NFR-01: Security

The system shall apply secure password hashing, authentication, input validation, session isolation, and rate limiting.

### NFR-02: Data Integrity

The system shall maintain valid database relationships and enforce appropriate constraints, including product quantity and stock validation.

### NFR-03: Reliability

The system shall handle invalid requests and database errors without intentionally exposing sensitive internal information.

### NFR-04: Performance

The system shall use database queries and appropriate filtering to support product retrieval and cart operations.

### NFR-05: Maintainability

The application shall use a modular structure that separates models, schemas, CRUD operations, routers, and security services.

### NFR-06: Configuration Security

Sensitive configuration values, including the JWT signing secret, shall be stored in environment variables and excluded from version control.

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

- Password hashing using Argon