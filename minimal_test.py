#!/usr/bin/env python3
"""
Minimal Flask test to verify Flask is working
"""

print("Starting minimal Flask test...")

try:
    from flask import Flask, jsonify
    print("✓ Flask imported successfully")
except ImportError as e:
    print(f"✗ Flask import failed: {e}")
    input("Press Enter to exit...")
    exit(1)

app = Flask(__name__)

@app.route('/')
def hello():
    print("Received request to /")
    return """
    <html>
    <head><title>Flask Test</title></head>
    <body>
        <h1>Flask is Working!</h1>
        <p>If you see this page, Flask is running correctly.</p>
        <button onclick="testAPI()">Test API</button>
        <div id="result"></div>
        
        <script>
        function testAPI() {
            fetch('/api/test')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('result').innerHTML = 
                        '<p style="color:green">API Test: ' + data.message + '</p>';
                })
                .catch(error => {
                    document.getElementById('result').innerHTML = 
                        '<p style="color:red">API Error: ' + error + '</p>';
                });
        }
        </script>
    </body>
    </html>
    """

@app.route('/api/test')
def test_api():
    print("Received request to /api/test")
    return jsonify({"status": "success", "message": "API is working!"})

if __name__ == '__main__':
    print("✓ Flask app created")
    print("Starting server on http://127.0.0.1:5000")
    print("Open your browser and go to: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        app.run(debug=True, host='127.0.0.1', port=5000)
    except Exception as e:
        print(f"✗ Failed to start Flask server: {e}")
        input("Press Enter to exit...")