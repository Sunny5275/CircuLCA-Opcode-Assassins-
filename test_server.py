#!/usr/bin/env python3
"""
Simple test script to check if Flask server is working
"""

import json
import sys
try:
    from flask import Flask, jsonify
except ImportError as e:
    print(f"Flask import error: {e}")
    sys.exit(1)

# Test basic Flask functionality
app = Flask(__name__)

@app.route('/test')
def test():
    return jsonify({"status": "working", "message": "Flask server is running"})

@app.route('/test_calculate', methods=['POST'])
def test_calculate():
    from flask import request
    try:
        data = request.get_json()
        return jsonify({
            "success": True,
            "received_data": data,
            "message": "POST request received successfully"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == '__main__':
    print("Starting test Flask server...")
    app.run(debug=True, host='127.0.0.1', port=5001)