<!--
This documentation was auto-generated by Claude on 2025-05-31T16-01-01.
Source file: ./src/backend/app/models.py
-->

# Document Management System - Database Models

## Overview

This module contains the SQLAlchemy ORM models for the Document Management System. The models support multi-tenant document management, vector embeddings, automated processing, and user management.

## Database Compatibility

The system supports both PostgreSQL and SQLite databases:
- **PostgreSQL**: Uses `pgvector` extension for vector embeddings
- **SQLite**: Falls back to Text fields for vector storage as JSON

## Models

### Core Document Models

#### Document

The primary model representing processed documents in the system.

**Table**: `documents`

**Key Features**:
- Document metadata extraction and storage
- Vector embeddings for semantic search
- Multi-tenant support via entity relationships
- File deduplication using SHA-256 hashing
- Automated processing workflow support

**Important Fields**:
- `hash`: SHA-256 hash for deduplication (unique, indexed)
- `embedding`: Vector field for semantic search (1536 dimensions)
- `entity_id`: Multi-tenant foreign key
- `confidence_score`: Processing confidence metric
- `status`: Processing status (default: "pending")

**Relationships**:
- Many-to-many with `Tag` via association table
- One-to-many with `Notification`
- Many-to-one with `Entity` (tenant)

#### Tag

Model for document categorization and organization.

**Table**: `tags`

**Features**:
- Unique tag names
- Many-to-many relationship with documents
- Eager loading configured for performance

#### DocumentTag

Association table helper class for document-tag relationships.

**Table**: `document_tag`

Provides ORM mapping for the many-to-many relationship between documents and tags.

### User Management

#### User

User authentication and authorization model.

**Table**: `users`

**Key Features**:
- Role-based access control
- Account status management
- Unique username and email constraints

**Roles**:
- `admin`: Full system access
- `viewer`: Read-only access
- Custom roles supported

#### UserEntity

Multi-tenant access control linking users to entities.

**Table**: `user_entities`

**Features**:
- User-entity access mapping
- Role assignment per entity
- Default tenant selection

### Multi-Tenant Support

#### Entity

Company or personal profile representing billing/ownership context.

**Table**: `entities`

**Key Features**:
- Company and individual profile support
- Complete address information
- Financial details (IBAN, VAT ID)
- Alias support for LLM matching
- Active/inactive status management

**Types**:
- `company`: Business entity
- `individual`: Personal profile

### Notifications

#### Notification

User alert and notification system.

**Table**: `notifications`

**Features**:
- Document-linked notifications
- Type-based categorization
- Read/unread status tracking

**Notification Types**:
- `overdue`: Payment or action overdue
- `reminder`: Upcoming deadlines
- `system`: System-generated alerts

### Address Management

#### AddressEntry

Comprehensive address book for contacts and organizations.

**Table**: `address_book`

**Key Features**:
- Person and organization support
- Complete address breakdown
- Transaction history tracking
- Group-based organization
- Document source tracking

**Entity Types**:
- `company`: Business contact
- `person`: Individual contact
- `government`: Government entity

### Vector Search

#### VectorEntry

Mapping between document pages and vector database entries.

**Table**: `vectors`

**Purpose**:
- Links internal documents to Qdrant vector database
- Stores patch-level vector IDs per page
- Supports ColPali vision embeddings

**Data Format**:
- `vector_ids`: JSON array of UUID strings

### System Configuration

#### AppSettings

Singleton table for mutable system configuration.

**Table**: `settings`

**Key Settings**:
- `inbox_path`: Document upload directory
- `storage_root`: Document organization root
- `locked`: Prevents accidental path changes
- `tos_accepted_at`: Terms of service acceptance

#### LLMConfig

Configuration for local-first AI integration.

**Table**: `llm_config`

**Provider Support**:
- `local`: Local model inference
- `openai`: OpenAI API integration
- `anthropic`: Anthropic API integration
- `custom`: Custom endpoint support

**Model Assignment**:
- `model_tagger`: Lightweight tagging model
- `model_enricher`: Field completion model
- `model_analytics`: Analytics summaries
- `model_responder`: Response generation (Pro feature)

**Processing Controls**:
- Automatic tagging and enrichment
- Retry logic and fallback providers
- Confidence thresholds
- Batch processing configuration

### Automated Processing

#### ProcessingRule

Rules for automated document processing and classification.

**Table**: `processing_rules`

**Key Features**:
- Vendor-based matching
- JSON-based conditions and actions
- Priority-based execution order
- Usage statistics tracking
- Rule enable/disable control

**Rule Structure**:
- `conditions`: JSON array of matching criteria
- `actions`: JSON array of automated actions
- `priority`: Execution order (lower = higher priority)

## Database Relationships

### Many-to-Many
- `Document` ↔ `Tag` (via `document_tag`)

### One-to-Many
- `Document` → `Notification`
- `Document` → `VectorEntry`
- `Entity` → `Document`
- `Entity` → `ProcessingRule`

### Many-to-One
- `UserEntity` → `User`
- `UserEntity` → `Entity`

## Indexes

Key indexes for performance:
- `documents.hash` (unique)
- `documents.entity_id`
- `processing_rules.vendor`
- `processing_rules.priority`
- `processing_rules.enabled`

## Performance Optimizations

### Eager Loading
- Tag relationships use `lazy="selectin"` to avoid N+1 queries
- Overlap warnings suppressed for complex relationships

### Vector Storage
- PostgreSQL: Native vector type with pgvector
- SQLite: JSON serialization in Text fields

## Migration Considerations

### Adding New Fields
- Use nullable columns for backward compatibility
- Consider default values for required fields

### Vector Database Changes
- VectorEntry model decouples internal storage from vector database
- Supports migration between vector database providers

## Security Notes

### Sensitive Data