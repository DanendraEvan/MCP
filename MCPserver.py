from flask import Flask, request, jsonify
from research_app import ResearchApp

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
