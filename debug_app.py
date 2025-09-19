from flask import Flask, render_template, request, jsonify, send_file, abort
import json
import numpy as np
import os
from datetime import datetime
import traceback

print("Starting Flask app with debug mode...")

try:
    from models.lca_calculator import LCACalculator
    from models.ai_estimator import AIEstimator
    from models.pdf_generator import PDFGenerator
    print("All model imports successful")
except Exception as e:
    print(f"Model import error: {e}")
    traceback.print_exc()

app = Flask(__name__)

# Initialize components
try:
    lca_calc = LCACalculator()
    ai_estimator = AIEstimator()
    pdf_gen = PDFGenerator()
    print("All components initialized successfully")
except Exception as e:
    print(f"Component initialization error: {e}")
    traceback.print_exc()

@app.route('/')
def index():
    """Main page with LCA input form"""
    print("Serving index page")
    return render_template('index.html')

@app.route('/test')
def test_page():
    """Test page for debugging"""
    print("Serving test page")
    return render_template('test.html')

@app.route('/calculate', methods=['POST'])
def calculate_lca():
    """Process LCA calculation and return results"""
    print("Received calculate request")
    try:
        # Get form data
        data = request.get_json()
        print(f"Received data: {data}")
        
        # Use AI to estimate missing parameters
        enhanced_data = ai_estimator.enhance_parameters(data)
        print(f"Enhanced data: {enhanced_data}")
        
        # Calculate LCA results
        results = lca_calc.calculate(enhanced_data)
        print(f"Calculation results: {results}")
        
        response = {
            'success': True,
            'results': results,
            'enhanced_data': enhanced_data
        }
        print(f"Sending response: {response}")
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Calculate error: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/generate_report', methods=['POST'])
def generate_report():
    """Generate PDF report"""
    print("Received generate report request")
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
        })

@app.route('/download_pdf/<filename>')
def download_pdf(filename):
    """Download a specific PDF file"""
    try:
        pdf_dir = os.path.join(os.path.dirname(__file__), 'generated_pdfs')
        pdf_path = os.path.join(pdf_dir, filename)
        
        # Security check: ensure file exists and is in the correct directory
        if not os.path.exists(pdf_path) or not os.path.commonpath([pdf_dir, pdf_path]) == pdf_dir:
            abort(404)
        
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

if __name__ == '__main__':
    print("Starting Flask app on port 5000...")
    app.run(debug=True, host='0.0.0.0', port=5000)