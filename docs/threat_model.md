# SecureShop – Threat Model

## 1. Introduction

This threat model identifies potential security risks affecting the SecureShop e-commerce backend. It analyzes important assets, possible attackers, attack scenarios, vulnerabilities, and security controls.

The analysis follows a threat-oriented approach inspired by the STRIDE model.

## 2. Assets to Protect

The main assets requiring protection are:

| Asset | Description | Security Requirement |
|---|---|---|
| User Credentials | User emails and password hashes | Confidentiality |
| Authentication Tokens | JWT access tokens | Confidentiality and Integrity |
| User Accounts | Account status, roles, and verification state | Integrity |
| Product Data | Product names, prices, and stock | Integrity |
| Shopping Cart | Cart items, quantities, and totals | Integrity and Isolation |
| Verification Tokens | Email verification tokens | Confidentiality and Integrity |
| Database | Stored application information | Confidentiality, Integrity, and Availability |
| Application Configuration | JWT secret and environment variables | Confidentiality |

## 3. Threat Actors

### 3.1 Unauthenticated Attacker

An external user attempting to access protected resources or exploit input validation weaknesses without logging in.

### 3.2 Malicious Registered User

A legitimate customer attempting to manipulate cart operations, access another session's data, or abuse application business logic.

### 3.3 Automated Attacker

A bot or script attempting repeated login or registration requests, brute-force attacks, or excessive requests.

### 3.4 Malicious Insider

A person with legitimate access who may misuse application privileges or modify sensitive data.

## 4. Threat Analysis Using STRIDE

| Threat Category | Potential Threat | Impact |
|---|---|---|
| Spoofing | Stealing or forging authentication credentials | Unauthorized account access |
| Tampering | Modifying product prices or cart quantities | Financial and data integrity violations |
| Repudiation | Denying performed account or cart actions | Difficulty investigating incidents |
| Information Disclosure | Accessing another user's cart or sensitive data | Privacy violation |
| Denial of Service | Sending excessive requests | Service unavailability |
| Elevation of Privilege | Obtaining unauthorized administrative access | Unauthorized privileged operations |

## 5. Identified Attack Scenarios and Mitigations

### 5.1 SQL Injection

**Attack Scenario:**

An attacker submits malicious SQL input through search or other user-controlled fields to manipulate database queries.

**Potential Impact:**

