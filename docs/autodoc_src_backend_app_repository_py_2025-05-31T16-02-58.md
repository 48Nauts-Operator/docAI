<!--
This documentation was auto-generated by Claude on 2025-05-31T16-02-58.
Source file: ./src/backend/app/repository.py
-->

# Document Repository API Documentation

This module provides data access repositories for managing documents, users, LLM configurations, tenants, and processing rules in an async SQLAlchemy-based application.

## Table of Contents

- [DocumentRepository](#documentrepository)
- [UserRepository](#userrepository)
- [LLMConfigRepository](#llmconfigrepository)
- [TenantRepository](#tenantrepository)
- [ProcessingRuleRepository](#processingrulerepository)

## DocumentRepository

Repository class for document data access operations with support for tagging, filtering, and search functionality.

### Methods

#### `create(db: AsyncSession, document: Document) -> Document`

Creates a new document in the database.

**Parameters:**
- `db`: Active database session
- `document`: Document model instance to create

**Returns:**
- `Document`: The created document with generated ID

**Example:**
```python
doc = Document(title="Sample", content="Content")
created_doc = await repo.create(db, doc)
```

#### `get_by_id(db: AsyncSession, document_id: int, as_dict: bool = False) -> Optional[Union[Document, Dict[str, Any]]]`

Retrieves a document by its ID with associated tags pre-loaded.

**Parameters:**
- `db`: Active database session
- `document_id`: Unique identifier of the document
- `as_dict`: If True, returns dictionary representation instead of model instance

**Returns:**
- `Document | Dict | None`: Document instance/dict if found, None otherwise

#### `get_all(db: AsyncSession, status: Optional[str] = None, document_type: Optional[str] = None, search: Optional[str] = None) -> List[Union[Document, Dict[str, Any]]]`

Retrieves all documents with optional filtering and search capabilities.

**Parameters:**
- `db`: Active database session
- `status`: Filter by document status (optional)
- `document_type`: Filter by document type (optional)
- `search`: Search term for title, content, or sender (optional)

**Returns:**
- `List[Dict]`: List of document dictionaries ordered by creation date (descending)

**Example:**
```python
# Get all pending invoices containing "urgent"
docs = await repo.get_all(db, status="pending", document_type="invoice", search="urgent")
```

#### `update(db: AsyncSession, document: Document) -> Document`

Updates an existing document in the database.

**Parameters:**
- `db`: Active database session
- `document`: Document instance with updated fields

**Returns:**
- `Document`: The updated document

#### `delete(db: AsyncSession, document_id: int) -> bool`

Deletes a document and its tag associations.

**Parameters:**
- `db`: Active database session
- `document_id`: ID of document to delete

**Returns:**
- `bool`: True if deleted successfully, False if document not found

#### Tag Management Methods

##### `add_tag(db: AsyncSession, document_id: int, tag_name: str) -> bool`

Adds a tag to a document, creating the tag if it doesn't exist.

##### `remove_tag(db: AsyncSession, document_id: int, tag_name: str) -> bool`

Removes a tag from a document.

##### `get_tags(db: AsyncSession, document_id: int) -> List[str]`

Retrieves all tag names for a document.

### Helper Methods

#### `_to_dict(doc: Document, include_tags: bool = True) -> Dict[str, Any]`

Static method that converts a Document model to a JSON-serializable dictionary.

**Features:**
- Converts vector embeddings to Python float lists
- Handles datetime serialization to ISO format
- Flattens tags to list of names
- Strips SQLAlchemy state information
- Converts numpy types and decimals appropriately

## UserRepository

Repository for user account management operations.

### Methods

#### `get_all(db: AsyncSession) -> List[dict]`

Retrieves all users ordered by creation date.

#### `get_by_id(db: AsyncSession, user_id: int) -> Optional[dict]`

Retrieves a user by ID, returning dictionary representation.

#### `get_by_username(db: AsyncSession, username: str) -> Optional[UserDB]`

Retrieves user by username, returning the actual model instance for authentication purposes.

#### `create(db: AsyncSession, **data) -> dict`

Creates a new user with provided data.

#### `update(db: AsyncSession, user_id: int, **data) -> Optional[dict]`

Updates user information.

#### `delete(db: AsyncSession, user_id: int) -> bool`

Deletes a user account.

## LLMConfigRepository

Repository for managing Large Language Model configuration settings.

### Methods

#### `get_config(db: AsyncSession) -> Optional[dict]`

Retrieves the current LLM configuration (singleton pattern).

#### `create_default_config(db: AsyncSession) -> dict`

Creates a default LLM configuration with model defaults.

#### `update_config(db: AsyncSession, **data) -> dict`

Updates LLM configuration, creating new config if none exists.

#### `test_connection(db: AsyncSession, provider: str, api_url: str = None, api_key: str = None) -> dict`

Tests connection to LLM provider.

**Returns:**
```python
{
    "status": "success" | "error",
    "message": "Connection status message",
    "available_models": ["model1", "model2", ...]
}
```

## TenantRepository

Repository for managing tenant (Entity) profiles and user-tenant relationships.

### Methods

#### `get_user_tenants(db: AsyncSession, user_id: int) -> List[dict]`

Retrieves all active tenants for a user, ordered by default status and alias.

#### `get_default_tenant(db: AsyncSession, user_id: int) -> Optional[dict]`

Gets the default tenant for a user.

#### `get_tenant_by_id(db: AsyncSession, user_id: int, tenant_id: int) -> Optional[dict]`

Retrieves a specific tenant by ID for a user.

#### `create_tenant(db: AsyncSession, user_id: int, **