from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))

@app.route('/marina', methods=['GET'])
def handle_marina():
    laza_param = request.args.get('laza')
    
    if not laza_param:
        return jsonify({"error": "Required params"}), 400
    
    try:
        make_process = subprocess.run(["make"], check=True, capture_output=True, text=True, cwd="../src")

        
        if make_process.returncode != 0:
            return jsonify({
                "error": "Build error",
                "details": marina_process.stderr.strip()
            }), 500
        
        marina_process = subprocess.run(["../src/marina", laza_param],
                                      capture_output=True,
                                      text=True,
                                      shell=False)
        
        if marina_process.returncode != 0:
            return jsonify({
                "error": "Runtime error in marina",
                "details": marina_process.stderr.strip()
            }), 500
            
        return jsonify({
            "input": laza_param,
            "result": marina_process.stdout.strip()
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)