<!--
This documentation was auto-generated by Claude on 2025-06-01T06-34-25.
Source file: ./src/backend/alembic/versions/2025_05_25_add_llm_config_table.py
-->

# Database Migration: LLM Configuration Table

## Overview

This Alembic migration creates the `llm_config` table to support local-first AI integration capabilities. The table stores configuration settings for Large Language Model (LLM) providers, model preferences, and processing parameters.

## Migration Details

- **Revision ID**: `20250525_llm_config`
- **Parent Revision**: `20250525_entities`
- **Created**: 2025-05-25
- **Purpose**: Add LLM configuration support for local-first AI integration

## Table Schema: `llm_config`

### Primary Key
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY | Unique identifier for configuration records |

### Provider Configuration
| Column | Type | Default | Nullable | Description |
|--------|------|---------|----------|-------------|
| `provider` | VARCHAR(50) | `'local'` | No | LLM provider name (local, openai, anthropic, etc.) |
| `api_key` | VARCHAR(255) | None | Yes | API authentication key for external providers |
| `api_url` | VARCHAR(255) | None | Yes | Custom API endpoint URL |

### Model Preferences
| Column | Type | Default | Nullable | Description |
|--------|------|---------|----------|-------------|
| `model_tagger` | VARCHAR(100) | `'phi3'` | No | Model used for tagging tasks |
| `model_enricher` | VARCHAR(100) | `'llama3'` | No | Model used for data enrichment |
| `model_analytics` | VARCHAR(100) | `'llama3'` | No | Model used for analytics tasks |
| `model_responder` | VARCHAR(100) | None | Yes | Model used for response generation |

### Processing Configuration
| Column | Type | Default | Nullable | Description |
|--------|------|---------|----------|-------------|
| `enabled` | BOOLEAN | `false` | No | Master switch for LLM processing |
| `auto_tagging` | BOOLEAN | `true` | No | Enable automatic content tagging |
| `auto_enrichment` | BOOLEAN | `true` | No | Enable automatic data enrichment |
| `external_enrichment` | BOOLEAN | `false` | No | Allow external API enrichment |

### Reliability Settings
| Column | Type | Default | Nullable | Description |
|--------|------|---------|----------|-------------|
| `max_retries` | INTEGER | `3` | No | Maximum retry attempts for failed requests |
| `retry_delay` | INTEGER | `300` | No | Delay between retries (seconds) |
| `backup_provider` | VARCHAR(50) | None | Yes | Fallback provider for reliability |
| `backup_model` | VARCHAR(100) | None | Yes | Fallback model name |

### Performance Settings
| Column | Type | Default | Nullable | Description |
|--------|------|---------|----------|-------------|
| `batch_size` | INTEGER | `5` | No | Number of items processed per batch |
| `concurrent_tasks` | INTEGER | `2` | No | Maximum concurrent processing tasks |
| `cache_responses` | BOOLEAN | `true` | No | Enable response caching |

### Quality Control
| Column | Type | Default | Nullable | Description |
|--------|------|---------|----------|-------------|
| `min_confidence_tagging` | FLOAT | `0.7` | No | Minimum confidence threshold for tagging |
| `min_confidence_entity` | FLOAT | `0.8` | No | Minimum confidence threshold for entity extraction |

### Audit Fields
| Column | Type | Default | Nullable | Description |
|--------|------|---------|----------|-------------|
| `created_at` | DATETIME | `NOW()` | No | Record creation timestamp |
| `updated_at` | DATETIME | `NOW()` | No | Last modification timestamp |

## Indexes

- **Primary Index**: `ix_llm_config_id` on `id` column

## Migration Functions

### `upgrade()`
Creates the `llm_config` table with all specified columns, constraints, and indexes. This enables LLM configuration management functionality.

### `downgrade()`
Removes the `ix_llm_config_id` index and drops the `llm_config` table, reverting all changes made by this migration.

## Usage Notes

1. **Local-First Design**: Default configuration prioritizes local models (`phi3`, `llama3`) over external APIs
2. **Security**: API keys should be encrypted at the application layer before storage
3. **Performance**: Batch processing and concurrency limits help manage resource usage
4. **Reliability**: Backup provider/model settings ensure fallback capabilities
5. **Quality Control**: Confidence thresholds filter low-quality AI outputs

## Related Tables

This migration depends on the `20250525_entities` migration and is part of the AI integration feature set.