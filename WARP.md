# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Overview

This is an AI-powered web application for Life Cycle Assessment (LCA) in metallurgy and mining operations. It's built with Flask and provides environmental impact calculations comparing conventional vs. circular economy approaches for metal production.

## Development Commands

### Core Development
```bash
# Install dependencies
pip install flask numpy pandas matplotlib reportlab scikit-learn

# Run the application in development mode
python app.py
```

### Testing and Development
```bash
# Start the Flask development server (with debug mode)
python app.py

# Access the application at http://localhost:5000

# Check Python syntax
python -m py_compile app.py
python -m py_compile models/*.py

# Run with verbose output for debugging
python -v app.py
```

### Dependencies Management
```bash
# Install from requirements file
pip install -r requirements.txt

# Generate new requirements (after adding dependencies)
pip freeze > requirements.txt
```

## Architecture Overview

### Core Components

**Flask Web Application (`app.py`)**
- Main entry point with three endpoints: `/` (form), `/calculate` (LCA processing), `/generate_report` (PDF generation)
- Orchestrates the interaction between AI estimator, LCA calculator, and PDF generator
- Handles JSON API communication with the frontend

**Modular Business Logic (`models/`)**
- `LCACalculator`: Core environmental impact calculations using industry emission factors
- `AIEstimator`: Rule-based parameter enhancement when user input is incomplete
- `PDFGenerator`: Report generation using ReportLab with charts and tables

**Frontend (`templates/index.html`)**
- Two-column responsive layout with main form and calculation history sidebar
- Self-contained HTML with embedded CSS and JavaScript for form handling and visualization
- Client-side history management using localStorage for persistent data storage
- Interactive history panel with click-to-load and delete functionality

### Data Flow Pattern

1. User submits form data through web interface
2. `AIEstimator` enhances incomplete parameters using industry standards
3. `LCACalculator` processes both conventional and circular economy pathways
4. Results returned to frontend for visualization
5. Calculation automatically saved to browser's localStorage for history tracking
6. Optional PDF report generation via `PDFGenerator`

### Key Calculation Logic

**LCA Calculator (`models/lca_calculator.py`)**
- Maintains emission factors for different metals (aluminium, copper, steel, other)
- Compares raw vs. recycled production routes
- Factors in transport, energy use, and end-of-life scenarios
- Calculates circularity indicators (recycled content, reuse potential)

**AI Parameter Enhancement (`models/ai_estimator.py`)**
- Uses industry averages with realistic variation (±10%)
- Estimates energy consumption and transport distances based on metal type and production route
- Infers additional parameters like process efficiency, material purity, and waste rates
- Rule-based system (not machine learning) for predictable results

## Working with the Codebase

### Adding New Metal Types

1. Update emission factors in `LCACalculator.__init__()` (lines 9-26)
2. Add parameter estimates in `AIEstimator.__init__()` (lines 8-26)
3. Update water usage mapping in `AIEstimator._infer_additional_parameters()` (lines 105-111)
4. Add option to HTML dropdown in `templates/index.html` (lines 94-99)

### Modifying Calculation Logic

- Core calculation methods are in `LCACalculator._calculate_pathway()` (lines 105-132)
- Circular economy improvements calculated in `LCACalculator.calculate()` (lines 77-100)
- AI estimation logic in `AIEstimator.enhance_parameters()` (lines 31-72)

### Customizing PDF Reports

- Report structure defined in `PDFGenerator.generate_report()` (lines 35-113)
- Chart generation uses matplotlib in `PDFGenerator._create_comparison_chart()` (lines 197-231)
- Recommendations logic in `PDFGenerator._create_recommendations()` (lines 233-271)

### Frontend Modifications

- Form handling JavaScript starts at line 309 in `templates/index.html`
- Chart visualization using HTML5 canvas at line 376
- API communication pattern: JSON POST to `/calculate`, response handling with error management
- History management functions start at line 442, including localStorage operations and UI updates

### History Feature Details

**Storage Mechanism:**
- Uses browser's localStorage with key `'lca_calculation_history'`
- Stores up to 10 most recent calculations (configurable via `MAX_HISTORY_ITEMS`)
- Each history item includes timestamp, input parameters, full results, and PDF metadata
- Generated PDFs are stored persistently in the `generated_pdfs/` directory

**User Interface:**
- Right sidebar panel shows calculation history with responsive design
- Each history item displays: date/time, metal type, production route, key parameters, CO₂ results
- PDF section shows when report is available with download button and file size
- Click any history item to reload its parameters and results
- Individual delete buttons (✕) and "Clear All" option for calculations
- "+ New LCA" button in history panel header for starting fresh calculations
- "New Calculation" and "Start New LCA" buttons in form and results sections
- Keyboard shortcuts: Ctrl+N (new calculation), Escape (clear form)
- Responsive design: history panel moves above form on smaller screens

**Key Functions:**
- `saveToHistory()`: Automatically saves each successful calculation with unique calculation ID
- `loadHistoryItem()`: Reloads form and results from selected history item
- `deleteHistoryItem()`: Removes individual calculations with confirmation
- `clearAllHistory()`: Clears entire history with confirmation
- `updateHistoryWithPDF()`: Updates history item when PDF is generated
- `downloadPDF()`: Downloads stored PDF files from server
- `generatePDFReport()`: Enhanced to save PDFs persistently and track metadata
- `startNewLCA()`: Clears form, hides results, scrolls to top, and focuses on first field
- `clearForm()`: Resets all form fields and removes validation styling
- `resetCalculation()`: Alternative function name for backward compatibility

## Environment and Dependencies

**Required Python Packages:**
- Flask 2.3.2 (web framework)
- numpy 1.24.3 (numerical calculations) 
- pandas 2.0.3 (data handling)
- matplotlib 3.7.1 (chart generation)
- reportlab 4.0.4 (PDF generation)
- scikit-learn 1.3.0 (unused but included for future ML enhancements)

**Runtime Requirements:**
- Python 3.7+
- No external databases or services required
- Temporary files created in system temp directory for PDF generation
- Charts generated in-memory and cleaned up automatically

## Key Design Patterns

- **Separation of Concerns**: Clear separation between web layer (app.py), business logic (models/), and presentation (templates/)
- **Factory Pattern**: Each model class initialized once in app.py and reused across requests
- **Data Enhancement Pipeline**: Input → AI Enhancement → LCA Calculation → Results
- **Stateless Design**: No session management or persistent storage, each request is independent
- **Error Handling**: Try/catch blocks in all endpoints with JSON error responses

## PDF Management

**PDF Storage System:**
- PDFs stored in `generated_pdfs/` directory with descriptive filenames
- Filename format: `lca_report_{metal}_{production_route}_{timestamp}_{calc_id}.pdf`
- Automatic cleanup of temporary chart files after PDF generation
- File metadata includes size, creation timestamp, and calculation parameters

**PDF Generator Updates (`models/pdf_generator.py`):**
- `generate_report()` now returns metadata dictionary instead of file path
- Persistent file storage replaces temporary file creation
- Includes calculation ID tracking for history correlation

## API Endpoints

- `GET /`: Serves the main HTML interface
- `POST /calculate`: Processes LCA calculation (expects JSON, returns enhanced data + results)
- `POST /generate_report`: Creates PDF report (expects calculation results with optional calculation_id, returns metadata and download URL)
- `GET /download_pdf/<filename>`: Downloads specific PDF file with security validation
- `GET /list_pdfs`: Returns list of all available PDF files with metadata

All POST endpoints expect JSON content-type and return structured JSON responses with success/error status.
