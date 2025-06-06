<!--
This documentation was auto-generated by Claude on 2025-06-01T06-33-18.
Source file: ./src/backend/alembic/versions/2025_05_22_expand_address_book.py
-->

# Database Migration: Expand Address Book Columns

## Overview

This Alembic migration script expands the `address_book` table by adding seven new columns to store comprehensive address and contact information.

## Migration Details

| Property | Value |
|----------|-------|
| **Revision ID** | `2025_05_22_expand_address_book` |
| **Previous Revision** | `2025_05_21_add_users_table` |
| **Created** | 2025-05-22 00:00:00.000000 |
| **Branch Labels** | None |
| **Dependencies** | None |

## Changes

### Upgrade Operation

The migration adds the following columns to the `address_book` table:

| Column Name | Data Type | Max Length | Nullable | Description |
|-------------|-----------|------------|----------|-------------|
| `street` | String | 255 | Yes | Primary street address |
| `address2` | String | 255 | Yes | Secondary address line (apartment, suite, etc.) |
| `town` | String | 255 | Yes | City or town name |
| `zip` | String | 20 | Yes | Postal/ZIP code |
| `county` | String | 100 | Yes | County or administrative region |
| `group_name` | String | 100 | Yes | Contact group classification |
| `last_transaction` | String | 50 | Yes | Most recent transaction identifier |

### Downgrade Operation

The migration can be reversed by dropping all seven columns in the reverse order of their creation:

1. `last_transaction`
2. `group_name`
3. `county`
4. `zip`
5. `town`
6. `address2`
7. `street`

## Technical Implementation

### Functions

#### `upgrade()`

Executes the forward migration by adding new columns to the `address_book` table using Alembic's batch operation context.

**Behavior:**
- Uses batch alter table context for database compatibility
- Adds columns sequentially with appropriate data types and constraints
- All new columns are nullable to prevent issues with existing data

#### `downgrade()`

Executes the reverse migration by removing the added columns from the `address_book` table.

**Behavior:**
- Uses batch alter table context for safe column removal
- Drops columns in reverse order to avoid dependency issues
- Completely removes all data stored in these columns

## Usage

### Apply Migration
```bash
alembic upgrade 2025_05_22_expand_address_book
```

### Revert Migration
```bash
alembic downgrade 2025_05_21_add_users_table
```

## Notes

- All new columns are optional (nullable) to maintain compatibility with existing records
- The migration uses batch operations for better database engine compatibility
- Column order in downgrade is intentionally reversed to ensure clean removal
- String length limits are set to accommodate typical address data requirements

## Dependencies

- **alembic**: Database migration framework
- **sqlalchemy**: SQL toolkit and ORM