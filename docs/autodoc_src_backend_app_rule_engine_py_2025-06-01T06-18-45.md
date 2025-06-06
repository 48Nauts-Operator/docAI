<!--
This documentation was auto-generated by Claude on 2025-06-01T06-18-45.
Source file: ./src/backend/app/rule_engine.py
-->

# Rule Engine Documentation

A comprehensive rule engine for automated document processing and classification that evaluates processing rules against documents and executes actions when rules match.

## Overview

The Rule Engine consists of three main components:
- **RuleEvaluator**: Evaluates processing rules against documents
- **RuleActionExecutor**: Executes actions from matched rules
- **DocumentRuleProcessor**: Main orchestrator for rule-based document processing

## Classes

### RuleEvaluator

Evaluates processing rules against documents to determine which rules match and what actions should be executed.

#### Constructor

```python
def __init__(self)
```

Creates a new RuleEvaluator instance with an initialized ProcessingRuleRepository.

#### Methods

##### evaluate_document

```python
async def evaluate_document(db: AsyncSession, document: Document) -> List[Dict[str, Any]]
```

Evaluates all enabled rules against a document and returns matching actions.

**Parameters:**
- `db` (AsyncSession): Database session for rule retrieval
- `document` (Document): Document to evaluate against rules

**Returns:**
- `List[Dict[str, Any]]`: List of actions to execute, each containing rule metadata

**Example:**
```python
evaluator = RuleEvaluator()
actions = await evaluator.evaluate_document(db_session, document)
# Returns: [{'type': 'set_category', 'value': 'Invoice', 'rule_id': 1, 'rule_name': 'Invoice Classification'}]
```

##### _evaluate_rule

```python
async def _evaluate_rule(document: Document, rule: Dict[str, Any]) -> bool
```

Evaluates a single rule against a document using AND logic for all conditions.

**Parameters:**
- `document` (Document): Document to evaluate
- `rule` (Dict[str, Any]): Rule configuration containing conditions and metadata

**Returns:**
- `bool`: True if all rule conditions match, False otherwise

##### _matches_vendor

```python
def _matches_vendor(document_sender: str, rule_vendor: str) -> bool
```

Performs case-insensitive partial matching between document sender and rule vendor.

**Parameters:**
- `document_sender` (str): Sender information from document
- `rule_vendor` (str): Vendor pattern from rule

**Returns:**
- `bool`: True if vendor matches, False otherwise

##### _evaluate_condition

```python
def _evaluate_condition(document: Document, condition: Dict[str, Any]) -> bool
```

Evaluates a single condition against a document field.

**Supported Operators:**
- `equals`: Exact match (case-insensitive)
- `contains`: Substring search
- `starts_with`: Prefix match
- `ends_with`: Suffix match
- `not_equals`: Negated exact match
- `not_contains`: Negated substring search

**Parameters:**
- `document` (Document): Document to evaluate
- `condition` (Dict[str, Any]): Condition with field, operator, and value

**Returns:**
- `bool`: True if condition matches, False otherwise

##### _get_document_field_value

```python
def _get_document_field_value(document: Document, field: str) -> Any
```

Retrieves the value of a specified document field.

**Supported Fields:**
- `title`: Document title
- `content`/`text`: Document content
- `sender`: Document sender
- `recipient`: Document recipient
- `document_type`: Document type classification
- `category`: Document category
- `amount`: Financial amount
- `currency`: Currency code
- `status`: Processing status
- `filename`: Original filename
- `file_path`: Storage path

**Parameters:**
- `document` (Document): Source document
- `field` (str): Field name to retrieve

**Returns:**
- `Any`: Field value or None if field doesn't exist

---

### RuleActionExecutor

Executes actions from matched rules, modifying documents according to rule specifications.

#### Methods

##### execute_actions

```python
async def execute_actions(db: AsyncSession, document: Document, actions: List[Dict[str, Any]]) -> Dict[str, Any]
```

Executes a list of actions on a document with error handling and result tracking.

**Parameters:**
- `db` (AsyncSession): Database session for persistence
- `document` (Document): Target document for modifications
- `actions` (List[Dict[str, Any]]): Actions to execute

**Returns:**
- `Dict[str, Any]`: Execution summary with results and failures

**Return Structure:**
```python
{
    'executed': [{'action': {...}, 'result': True}],
    'failed': [{'action': {...}, 'error': 'Error message'}],
    'total': 5
}
```

##### _execute_action

```python
async def _execute_action(db: AsyncSession, document: Document, action: Dict[str, Any]) -> bool
```

Executes a single action on a document.

**Supported Action Types:**
- `assign_tenant`: Assigns document to a tenant
- `set_category`: Sets document category
- `add_tag`: Adds a tag to the document
- `set_status`: Updates document status
- `set_document_type`: Sets document type

**Parameters:**
- `db` (AsyncSession): Database session
- `document` (Document): Target document
- `action` (Dict[str, Any]): Action configuration

**Returns:**
- `bool`: True if action executed successfully

##### Action-Specific Methods

###### _assign_tenant
```python
async def _assign_tenant(document: Document, tenant_id: Any) -> bool
```
Assigns document to specified tenant with validation.

###### _set_category
```python
async def _set_category(document: Document, category: str) -> bool
```
Sets document category with string conversion.

###### _add_tag
```python
async def _add_tag(db: AsyncSession, document: Document, tag_name: str) -> bool
```
Adds tag using DocumentRepository integration.

###### _set_status
```python
async def _set_status(document: Document, status: str) -> bool
```
Updates document processing status.

###### _set_document_type
```python
async def _set_document_type(document: Document, doc_type: str) -> bool
```