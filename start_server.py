#!/usr/bin/env python3
"""
Comprehensive startup script for LCA Flask application
"""

import sys
import os
import traceback

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("Checking dependencies...")
    
    required_modules = [
        'flask',
        'numpy', 
        'pandas',
        'matplotlib',
        'reportlab',
        'sklearn'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"✗ {module} - MISSING")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\nMissing dependencies: {', '.join(missing_modules)}")
        print("Install with: pip install " + " ".join(missing_modules))
        return False
    
    print("All dependencies available!")
    return True

def check_file_structure():
    """Check if all required files exist"""
    print("\nChecking file structure...")
    
    required_files = [
        'app.py',
        'models/__init__.py',
        'models/lca_calculator.py',
        'models/ai_estimator.py', 
        'models/pdf_generator.py',
        'templates/index.html'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - MISSING")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\nMissing files: {', '.join(missing_files)}")
        return False
    
    print("All files present!")
    return True

def test_imports():
    """Test importing the application modules"""
    print("\nTesting imports...")
    
    try:
        from flask import Flask, render_template, request, jsonify, send_file, abort
        print("✓ Flask imports")
    except Exception as e:
        print(f"✗ Flask import error: {e}")
        return False
    
    try:
        from models.lca_calculator import LCACalculator
        from models.ai_estimator import AIEstimator
        from models.pdf_generator import PDFGenerator
        print("✓ Model imports")
    except Exception as e:
        print(f"✗ Model import error: {e}")
        traceback.print_exc()
        return False
    
    try:
        import numpy as np
        import pandas as pd
        import matplotlib
        print("✓ Data science libraries")
    except Exception as e:
        print(f"✗ Data science library error: {e}")
        return False
    
    print("All imports successful!")
    return True

def test_model_initialization():
    """Test initializing the model classes"""
    print("\nTesting model initialization...")
    
    try:
        from models.lca_calculator import LCACalculator
        from models.ai_estimator import AIEstimator
        from models.pdf_generator import PDFGenerator
        
        lca_calc = LCACalculator()
        print("✓ LCACalculator initialized")
        
        ai_estimator = AIEstimator()
        print("✓ AIEstimator initialized")
        
        pdf_gen = PDFGenerator()
        print("✓ PDFGenerator initialized")
        
        print("All models initialized successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Model initialization error: {e}")
        traceback.print_exc()
        return False

def create_directories():
    """Create necessary directories"""
    print("\nCreating directories...")
    
    directories = ['generated_pdfs', 'templates']
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✓ {directory} directory ready")
        except Exception as e:
            print(f"✗ Error creating {directory}: {e}")
            return False
    
    return True

def start_flask_app():
    """Start the Flask application"""
    print("\nStarting Flask application...")
    
    try:
        # Import the main app
        import app
        
        print("✓ Main app imported successfully")
        print("Starting server on http://127.0.0.1:5000")
        print("Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Start the app
        app.app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
        
    except Exception as e:
        print(f"✗ Flask startup error: {e}")
        traceback.print_exc()
        return False

def main():
    """Main startup function"""
    print("=" * 50)
    print("LCA Flask Application Startup")
    print("=" * 50)
    
    # Run all checks
    checks = [
        check_dependencies,
        check_file_structure, 
        test_imports,
        create_directories,
        test_model_initialization
    ]
    
    for check in checks:
        if not check():
            print(f"\n❌ Startup failed at: {check.__name__}")
            input("Press Enter to exit...")
            sys.exit(1)
    
    print("\n✅ All checks passed! Starting Flask server...")
    print("\nOnce server starts, open your browser and go to:")
    print("  http://127.0.0.1:5000")
    print("\n" + "=" * 50)
    
    start_flask_app()

if __name__ == "__main__":
    main()