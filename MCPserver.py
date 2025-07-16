from flask import Flask, request, jsonify
from research_app import ResearchApp
import threading
import socket
import json

app = Flask(__name__)
research_app = ResearchApp()

@app.route('/api', methods=['POST'])
def handle_api_request():
    """Handle all API requests through HTTP"""
    try:
        data = request.get_json()
        action = data.get('action')
        params = data.get('params', {})
        
        if action == 'ping':
            return jsonify({"status": "alive"})
        elif action == 'search_papers':
            result = research_app.search_papers(**params)
        elif action == 'get_paper_content':
            result = research_app.get_paper_content(**params)
        elif action == 'extract_info':
            result = research_app.extract_info(**params)
        elif action == 'research_assistant':
            result = research_app.research_assistant(**params)
        else:
            return jsonify({"error": "Invalid action specified"}), 400
            
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Optional: Keep socket server running in background
def run_socket_server():
    """Run the original socket server in a separate thread"""
    host = 'localhost'
    port = 5000
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Socket server listening on {host}:{port}")
        
        while True:
            conn, addr = s.accept()
            try:
                data = conn.recv(1024).decode('utf-8')
                if data:
                    request = json.loads(data)
                    response = research_app.process_request(request)
                    conn.send(json.dumps(response).encode('utf-8'))
            except Exception as e:
                print(f"Socket error: {e}")
            finally:
                conn.close()

# Start socket server in background if needed
if __name__ == '__main__':
    # Only start socket server when running directly
    socket_thread = threading.Thread(target=run_socket_server, daemon=True)
    socket_thread.start()
    
    # Start Flask app
    app.run(host='0.0.0.0', port=8080)
