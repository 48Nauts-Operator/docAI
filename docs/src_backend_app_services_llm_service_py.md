<!-- Auto-generated by Claude on 2025-06-01 10:12 -->

# DocumentLLMService & LLMServiceFactory Documentation

## Overview

This module provides a high-level service layer for integrating Large Language Model (LLM) capabilities with document processing workflows. It acts as a bridge between the core LLM service and document management operations, offering batch processing, metadata extraction, and automatic tagging features.

## Purpose

- **Document Processing Integration**: Seamlessly integrate LLM capabilities into document workflows
- **Batch Operations**: Process multiple documents efficiently with configurable concurrency
- **Metadata Enrichment**: Automatically extract and populate document metadata using AI
- **Tag Suggestion**: Generate relevant tags for documents based on content analysis
- **Factory Pattern**: Provide clean instantiation of service objects

## Classes

### DocumentLLMService

High-level service class that orchestrates document processing with LLM capabilities.

#### Constructor

```python
def __init__(self, db_session: AsyncSession)
```

**Parameters:**
- `db_session`: SQLAlchemy async database session for database operations

#### Key Methods

##### `process_document(document_id: int, force: bool = False) -> Dict[str, Any]`

Processes a single document with comprehensive LLM analysis.

**Features:**
- Metadata extraction (if auto-enrichment enabled)
- Tag suggestion (if auto-tagging enabled) 
- Content analysis
- Duplicate processing prevention

**Parameters:**
- `document_id`: ID of the document to process
- `force`: Skip already-processed check if `True`

**Returns:**
- Dictionary containing processing results and status

##### `batch_process_documents(document_ids: List[int], force: bool = False) -> Dict[str, Any]`

Processes multiple documents with configurable batch size and concurrency limits.

**Features:**
- Configurable batch sizing
- Concurrent processing with semaphore limiting
- Comprehensive result aggregation
- Error handling and reporting

##### `enrich_document_field(document_id: int, field_name: str) -> Dict[str, Any]`

Enriches a specific document field using targeted LLM queries.

**Use Cases:**
- Extract specific information (dates, amounts, names)
- Fill missing metadata fields
- Validate existing field values

#### Private Methods

##### `_update_document_metadata(document: Document, metadata: Dict[str, Any]) -> None`

Maps LLM-extracted metadata to document model fields with intelligent updating logic.

**Field Mappings:**
- `title` → Document title
- `document_type` → Document type classification
- `sender/recipient` → Contact information
- `document_date/due_date` → Important dates
- `amount/currency` → Financial information
- `status` → Document status

##### `_add_tags_to_document(document_id: int, tags: List[str]) -> None`

Adds AI-suggested tags to documents with basic validation and confidence filtering.

### LLMServiceFactory

Factory class providing clean instantiation patterns for LLM services.

#### Static Methods

##### `create_document_service(db_session: AsyncSession) -> DocumentLLMService`

Creates a configured DocumentLLMService instance.

##### `create_llm_service(db_session: AsyncSession) -> LLMService`

Creates a basic LLM service instance for direct usage.

## Configuration Options

The service respects various configuration parameters:

- **`auto_enrichment`**: Enable/disable automatic metadata extraction
- **`auto_tagging`**: Enable/disable automatic tag generation
- **`batch_size`**: Number of documents processed per batch (default: 5)
- **`concurrent_tasks`**: Maximum concurrent processing tasks (default: 2)
- **`min_confidence_tagging`**: Minimum confidence threshold for tag suggestions (default: 0.7)

## Usage Examples

### Single Document Processing

```python
async def process_single_document():
    service = LLMServiceFactory.create_document_service(db_session)
    result = await service.process_document(document_id=123)
    
    if result['status'] == 'success':
        print(f"Extracted tags: {result.get('suggested_tags', [])}")
        print(f"Analysis: {result.get('analysis', 'N/A')}")
```

### Batch Processing

```python
async def process_document_batch():
    service = LLMServiceFactory.create_document_service(db_session)
    document_ids = [1, 2, 3, 4, 5]
    
    results = await service.batch_process_documents(document_ids)
    print(f"Processed: {results['processed']}")
    print(f"Errors: {results['errors']}")
```

### Field Enrichment

```python
async def enrich_specific_field():
    service = LLMServiceFactory.create_document_service(db_session)
    result = await service.enrich_document_field(
        document_id=123, 
        field_name="invoice_number"
    )
    
    if result['status'] == 'success':
        print(f"Extracted {result['field']}: {result['value']}")
```

## Error Handling

The service implements comprehensive error handling:

- **Document Not Found**: Returns appropriate error status
- **LLM Service Disabled**: Graceful degradation with status messages
- **Processing Failures**: Detailed error logging and user-friendly messages
- **Database Errors**: Automatic rollback and error reporting

## Dependencies

- `LLMService`: Core LLM functionality
- `DocumentRepository`: Database operations for documents
- `TenantExtractionAgent`: Tenant information extraction (referenced but not fully implemented)
- SQLAlchemy async sessions for database operations

## Notes and Suggestions

### ⚠️ Current Limitations

1. **Tenant Extraction**: The tenant extraction feature is referenced but not fully implemented
2. **Hard-coded User Context**: User ID handling needs improvement for multi-tenant scenarios
3. **Basic Tag Validation**: Tag confidence scoring could be enhanced

### 🔧 Suggested Improvements

1. **Add Retry Logic**: Implement exponential backoff for failed LLM requests
2. **Progress Tracking**: Add progress callbacks for long-running batch operations
3. **Caching**: Cache LLM responses to avoid duplicate processing
4. **Metrics**: Add processing time and success rate metrics
5. **Configuration