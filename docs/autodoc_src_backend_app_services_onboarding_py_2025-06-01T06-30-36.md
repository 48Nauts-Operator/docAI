<!--
This documentation was auto-generated by Claude on 2025-06-01T06-30-36.
Source file: ./src/backend/app/services/onboarding.py
-->

# OnboardingService

## Overview

The `OnboardingService` class manages application onboarding processes, specifically handling Terms of Service (ToS) acceptance tracking through database operations.

## Class Definition

```python
class OnboardingService
```

### Constructor

```python
def __init__(self, db: AsyncSession)
```

**Parameters:**
- `db` (AsyncSession): SQLAlchemy async database session for performing database operations

**Description:**
Initializes the OnboardingService with a database session.

## Public Methods

### accept_tos()

```python
async def accept_tos() -> datetime
```

**Returns:**
- `datetime`: Timestamp when the Terms of Service was accepted

**Description:**
Records the user's acceptance of Terms of Service by setting the current UTC timestamp in the application settings.

**Behavior:**
1. Retrieves the application settings row
2. Sets `tos_accepted_at` to the current UTC datetime
3. Commits the changes to the database
4. Returns the acceptance timestamp

### tos_accepted()

```python
async def tos_accepted() -> bool
```

**Returns:**
- `bool`: `True` if Terms of Service has been accepted, `False` otherwise

**Description:**
Checks whether the Terms of Service has been previously accepted by examining the `tos_accepted_at` field in application settings.

## Private Methods

### _settings_row()

```python
async def _settings_row() -> AppSettings
```

**Returns:**
- `AppSettings`: The application settings database record

**Description:**
Retrieves or creates the application settings row. This method ensures that an `AppSettings` record always exists in the database.

**Behavior:**
1. Attempts to fetch the `AppSettings` record with ID 1
2. If no record exists:
   - Creates a new `AppSettings` record with default values:
     - `inbox_path`: "/tmp"
     - `storage_root`: "/tmp"
   - Adds the record to the database session
   - Commits the transaction
   - Refreshes the record to get the current state
3. Returns the settings record

## Dependencies

```python
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models import AppSettings
```

**Required Imports:**
- `datetime.datetime`: For timestamp operations
- `sqlalchemy.ext.asyncio.AsyncSession`: Async database session handling
- `sqlalchemy.select`, `sqlalchemy.update`: SQL query operations
- `app.models.AppSettings`: Application settings model

## Usage Example

```python
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.onboarding import OnboardingService

async def handle_onboarding(db_session: AsyncSession):
    service = OnboardingService(db_session)
    
    # Check if ToS is already accepted
    if not await service.tos_accepted():
        # Accept ToS
        accepted_at = await service.accept_tos()
        print(f"Terms of Service accepted at: {accepted_at}")
    else:
        print("Terms of Service already accepted")
```

## Notes

- All database operations are asynchronous and require proper `await` handling
- The service assumes a single application settings record with ID 1
- Default paths ("/tmp") are used for new settings records and should be configured appropriately for production environments
- The service automatically handles database session management through commits and refreshes