# LCA Metallurgy Assessment Tool

A minimal AI-powered web application for automated Life Cycle Assessment (LCA) in metallurgy and mining operations.

## Features

### Core Functionality
- **Simple Interface**: Input forms for metal type, production route, energy use, transport distance, and end-of-life options
- **AI Enhancement**: Automatic parameter estimation using industry standards when user data is incomplete
- **LCA Calculations**: Environmental impact calculations (CO₂ equivalent) and circularity indicators
- **Pathway Comparison**: Side-by-side comparison of conventional vs. circular economy approaches
- **Visual Analysis**: Simple charts showing environmental impact reduction and circularity gains
- **PDF Reports**: Downloadable reports with inputs, outputs, and recommendations

### Supported Metals
- Aluminium
- Copper
- Steel
- Other (generic metals)

### Production Routes
- Raw material processing (primary production)
- Recycled material processing (secondary production)

### End-of-Life Options
- Reuse
- Recycle
- Landfill

## Installation

1. **Prerequisites**: Ensure Python 3.7+ is installed
2. **Install Dependencies**:
   ```bash
   pip install flask numpy pandas matplotlib reportlab scikit-learn
   ```

## Usage

1. **Start the Application**:
   ```bash
   python app.py
   ```

2. **Access the Web Interface**:
   - Open your browser and navigate to `http://localhost:5000`
   - Fill in the required parameters (metal type, production route, end-of-life option)
   - Optionally provide energy use and transport distance (AI will estimate if missing)
   - Click "Calculate LCA" to generate results

3. **View Results**:
   - Review AI-enhanced parameters
   - Compare conventional vs. circular pathways
   - Analyze environmental impact metrics
   - View simple visualization chart

4. **Generate Report**:
   - Click "Generate PDF Report" to download a comprehensive report
   - Report includes all inputs, calculations, and recommendations

## Technical Architecture

### Backend Components
- **Flask App** (`app.py`): Main application with API endpoints
- **LCA Calculator** (`models/lca_calculator.py`): Core environmental impact calculations
- **AI Estimator** (`models/ai_estimator.py`): Parameter enhancement using industry standards
- **PDF Generator** (`models/pdf_generator.py`): Report generation with charts and tables

### Frontend
- **HTML Interface** (`templates/index.html`): Simple, responsive web form
- **JavaScript**: Client-side form handling and result visualization
- **CSS**: Minimal styling for clean user experience

## API Endpoints

- `GET /`: Main application interface
- `POST /calculate`: Process LCA calculations
- `POST /generate_report`: Generate and download PDF report

## Key Metrics Calculated

### Environmental Impact
- CO₂ equivalent emissions (kg CO₂/kg metal)
- Energy consumption (kWh/kg)
- Transport emissions
- End-of-life impact

### Circularity Indicators
- Recycled content percentage
- Reuse potential percentage
- Waste generation rates
- Process efficiency

## Example Use Cases

1. **Mining Company**: Compare environmental impact of primary vs. secondary metal production
2. **Manufacturing**: Assess circular economy opportunities in metal supply chains
3. **Policy Analysis**: Evaluate environmental benefits of recycling programs
4. **Research**: Quick LCA estimates for metallurgy studies

## Limitations

This is a minimal implementation focused on core functionality:
- Basic calculations using industry averages
- Simplified AI estimation (rule-based, not machine learning)
- Limited visualization options
- No external integrations or databases
- No user authentication or data persistence

## Future Enhancements

- Integration with real LCA databases
- Advanced machine learning models for parameter estimation
- More detailed visualization options
- User account management and data storage
- API integration with external systems
- Mobile-responsive design improvements

## Development

The application follows a modular structure:
- Models handle business logic and calculations
- Templates provide the user interface
- Static files contain CSS and JavaScript
- Main app.py coordinates everything

To extend functionality:
1. Add new metal types in `lca_calculator.py`
2. Enhance AI estimation in `ai_estimator.py`
3. Customize PDF reports in `pdf_generator.py`
4. Modify the UI in `templates/index.html`

## License

This project is provided as-is for educational and research purposes.