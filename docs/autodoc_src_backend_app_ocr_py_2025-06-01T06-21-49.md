<!--
This documentation was auto-generated by Claude on 2025-06-01T06-21-49.
Source file: ./src/backend/app/ocr.py
-->

# OCR and Document Processing Module

## Overview

This module provides OCR (Optical Character Recognition) and document processing capabilities for the Document Management System. It supports multiple document formats including PDFs, images, and text files, with optimized processing strategies to minimize resource usage and avoid common stability issues.

## Key Features

- **Multi-format support**: PDF, image (JPG, PNG, TIFF), and text files
- **Optimized PDF processing**: Hybrid approach using embedded text extraction and selective OCR
- **Asynchronous processing**: Non-blocking operations for better performance
- **Lazy imports**: Reduced startup cost and memory overhead
- **Error handling**: Comprehensive logging and graceful error recovery

## Dependencies

- `pytesseract`: OCR text extraction
- `PIL (Pillow)`: Image processing
- `pdfplumber`: PDF text extraction (lightweight, pure Python)
- `PyMuPDF (fitz)`: PDF rasterization when OCR is needed
- Standard library: `os`, `logging`, `asyncio`, `io`, `importlib`

## Classes

### OCRProcessor

Main class responsible for processing documents and extracting text content.

#### Methods

##### `process_document(file_path: str) -> str`

**Description**: Main entry point for document processing. Automatically detects file type and applies appropriate processing strategy.

**Parameters**:
- `file_path` (str): Absolute or relative path to the document file

**Returns**: 
- `str`: Extracted text content from the document

**Supported File Types**:
- PDF: `.pdf`
- Images: `.jpg`, `.jpeg`, `.png`, `.tiff`, `.tif`
- Text: `.txt`

**Example**:
```python
processor = OCRProcessor()
text = await processor.process_document("/path/to/document.pdf")
```

##### `_process_pdf(file_path: str) -> str` (Private)

**Description**: Specialized PDF processing using a two-pass approach for optimal performance and stability.

**Processing Strategy**:
1. **Pass 1**: Extract embedded text using `pdfplumber` (fast, stable)
2. **Pass 2**: Apply OCR only to pages without embedded text using `PyMuPDF` rasterization

**Parameters**:
- `file_path` (str): Path to the PDF file

**Returns**:
- `str`: Complete extracted text from all pages

**Benefits**:
- Avoids unnecessary OCR on digital-native PDFs
- Eliminates segmentation faults from poppler C-libraries
- Significantly faster processing for text-based PDFs

##### `_process_image(file_path: str) -> str` (Private)

**Description**: Processes image files using Tesseract OCR.

**Parameters**:
- `file_path` (str): Path to the image file

**Returns**:
- `str`: Extracted text from the image

**Configuration**:
- Language: English (`eng`)
- Asynchronous processing to avoid blocking

##### `_process_text(file_path: str) -> str` (Private)

**Description**: Reads and returns content from plain text files.

**Parameters**:
- `file_path` (str): Path to the text file

**Returns**:
- `str`: File content as string

## Utility Functions

### `_lazy_import(module_name: str)`

**Description**: Lazy imports heavy-weight libraries only when needed and caches them for reuse.

**Parameters**:
- `module_name` (str): Name of the module to import

**Returns**:
- Module object

**Purpose**: Reduces startup cost and memory overhead by deferring imports of resource-intensive libraries.

## Usage Examples

### Basic Document Processing

```python
import asyncio
from ocr_processor import OCRProcessor

async def main():
    processor = OCRProcessor()
    
    # Process a PDF
    pdf_text = await processor.process_document("document.pdf")
    print(f"Extracted {len(pdf_text)} characters from PDF")
    
    # Process an image
    image_text = await processor.process_document("scanned_doc.png")
    print(f"OCR extracted: {image_text[:100]}...")
    
    # Process a text file
    text_content = await processor.process_document("readme.txt")
    print(f"Text file content: {text_content}")

# Run the async function
asyncio.run(main())
```

### Error Handling

```python
async def process_with_error_handling():
    processor = OCRProcessor()
    
    try:
        text = await processor.process_document("document.pdf")
        if text.startswith("Error processing document"):
            print("Processing failed, but application continues")
        else:
            print(f"Successfully extracted: {len(text)} characters")
    except Exception as e:
        print(f"Unexpected error: {e}")
```

## Configuration Requirements

### Tesseract Installation

Ensure Tesseract OCR is installed on your system:

**Ubuntu/Debian**:
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-eng
```

**macOS**:
```bash
brew install tesseract
```

**Windows**:
Download and install from the [official Tesseract repository](https://github.com/UB-Mannheim/tesseract/wiki).

### Python Dependencies

Install required packages:
```bash
pip install pytesseract Pillow pdfplumber PyMuPDF
```

## Performance Considerations

- **PDF Processing**: The hybrid approach significantly reduces processing time for digital PDFs
- **Memory Usage**: Lazy imports keep memory footprint low until processing begins
- **Concurrency**: Async processing allows handling multiple documents simultaneously
- **OCR Optimization**: Only processes pages that actually need OCR, avoiding unnecessary computation

## Error Handling

The module implements comprehensive error handling:

- **File Type Errors**: Unsupported formats return descriptive error messages
- **Processing Errors**: Individual document failures are logged and return error descriptions
- **Library Failures**: Graceful fallbacks when extraction libraries fail
- **Logging**: Detailed logging for debugging and monitoring

## Logging

The module uses Python's standard logging framework with the logger name matching the module name. Configure logging levels as needed:

```python
import logging
logging.getLogger('ocr_processor').