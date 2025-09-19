from flask import Flask, render_template, request, jsonify, send_file, abort
import json
import numpy as np
import os
import sys
from datetime import datetime
import traceback

print("Starting Windows-compatible LCA Flask app...")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

# Add current directory to Python path to ensure imports work
sys.path.insert(0, os.getcwd())

try:
    from models.lca_calculator import LCACalculator
    from models.ai_estimator import AIEstimator
    from models.pdf_generator import PDFGenerator
    print("✓ All model imports successful")
except Exception as e:
    print(f"✗ Model import error: {e}")
    traceback.print_exc()

app = Flask(__name__)

# Initialize components with error handling
try:
    lca_calc = LCACalculator()
    ai_estimator = AIEstimator()
    pdf_gen = PDFGenerator()
    print("✓ All components initialized")
except Exception as e:
    print(f"✗ Component initialization error: {e}")
    traceback.print_exc()

@app.route('/')
def index():
    """Main page with LCA input form"""
    print("Serving index page")
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"Error serving index page: {e}")
        return f"Error loading page: {e}", 500

@app.route('/calculate', methods=['POST'])
def calculate_lca():
    """Process LCA calculation and return results"""
    print("=" * 50)
    print("CALCULATE REQUEST RECEIVED")
    print("=" * 50)
    
    try:
        # Get form data
        data = request.get_json()
        print(f"Raw request data: {data}")
        
        if not data:
            print("ERROR: No JSON data received")
            return jsonify({
                'success': False,
                'error': 'No data received'
            }), 400
        
        # Validate required fields
        required_fields = ['metalType', 'productionRoute', 'endOfLife']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            error_msg = f"Missing required fields: {', '.join(missing_fields)}"
            print(f"ERROR: {error_msg}")
            return jsonify({
                'success': False,
                'error': error_msg
            }), 400
        
        print("✓ Input validation passed")
        
        # Use AI to estimate missing parameters
        print("Enhancing parameters with AI...")
        enhanced_data = ai_estimator.enhance_parameters(data)
        print(f"✓ Enhanced data: {enhanced_data}")
        
        # Calculate LCA results
        print("Calculating LCA results...")
        results = lca_calc.calculate(enhanced_data)
        print(f"✓ LCA results: {results}")
        
        response = {
            'success': True,
            'results': results,
            'enhanced_data': enhanced_data
        }
        
        print("✅ Calculation completed successfully")
        print("=" * 50)
        
        return jsonify(response)
    
    except Exception as e:
        error_msg = f"Calculation error: {str(e)}"
        print(f"❌ {error_msg}")
        traceback.print_exc()
        print("=" * 50)
        
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

@app.route('/generate_report', methods=['POST'])
def generate_report():
    """Generate PDF report"""
    print("PDF generation requested")
    try:
        data = request.get_json()
        calculation_id = data.get('calculation_id', None)
        
        pdf_metadata = pdf_gen.generate_report(data, calculation_id)
        
        return jsonify({
            'success': True,
            'pdf_metadata': pdf_metadata,
            'download_url': f'/download_pdf/{pdf_metadata["filename"]}'
        })
    
    except Exception as e:
        print(f"PDF generation error: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/download_pdf/<filename>')
def download_pdf(filename):
    """Download a specific PDF file"""
    try:
        pdf_dir = os.path.join(os.path.dirname(__file__), 'generated_pdfs')
        pdf_path = os.path.join(pdf_dir, filename)
        
        print(f"PDF download requested: {filename}")
        print(f"PDF path: {pdf_path}")
        
        # Security check: ensure file exists and is in the correct directory
        if not os.path.exists(pdf_path):
            print(f"PDF file not found: {pdf_path}")
            abort(404)
            
        if not os.path.commonpath([pdf_dir, pdf_path]) == pdf_dir:
            print("Security violation: Path traversal attempt")
            abort(403)
        
        return send_file(pdf_path, as_attachment=True, download_name=filename)
    
    except Exception as e:
        print(f"PDF download error: {e}")
        abort(500)

@app.route('/list_pdfs', methods=['GET'])
def list_pdfs():
    """List all available PDF files"""
    try:
        pdf_dir = os.path.join(os.path.dirname(__file__), 'generated_pdfs')
        if not os.path.exists(pdf_dir):
            return jsonify({'success': True, 'pdfs': []})
        
        pdf_files = []
        for filename in os.listdir(pdf_dir):
            if filename.endswith('.pdf'):
                file_path = os.path.join(pdf_dir, filename)
                file_stat = os.stat(file_path)
                pdf_files.append({
                    'filename': filename,
                    'size': file_stat.st_size,
                    'created': datetime.fromtimestamp(file_stat.st_ctime).isoformat(),
                    'download_url': f'/download_pdf/{filename}'
                })
        
        # Sort by creation time (newest first)
        pdf_files.sort(key=lambda x: x['created'], reverse=True)
        
        return jsonify({
            'success': True,
            'pdfs': pdf_files
        })
    
    except Exception as e:
        print(f"List PDFs error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'components': {
            'lca_calculator': 'ready',
            'ai_estimator': 'ready', 
            'pdf_generator': 'ready'
        }
    })

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("LCA METALLURGY ASSESSMENT TOOL - Windows Edition")
    print("=" * 60)
    print("Server starting on: http://127.0.0.1:5000")
    print("Health check: http://127.0.0.1:5000/health")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        app.run(
            debug=True, 
            host='127.0.0.1', 
            port=5000,
            threaded=True,
            use_reloader=False  # Disable reloader to avoid Windows issues
        )
    except Exception as e:
        print(f"\n❌ Failed to start Flask server: {e}")
        traceback.print_exc()
        input("\nPress Enter to exit...")