from flask import Flask, request, jsonify
from main import ResearchApp
import os

app = Flask(__name__)
research_app = ResearchApp()

@app.route('/api', methods=['POST'])
def handle_request():
    data = request.json
    action = data.get('action')
    params = data.get('params', {})
    
    try:
        if action == 'search_papers':
            return jsonify(research_app.search_papers(**params))
        elif action == 'get_paper_content':
            return jsonify(research_app.get_paper_content(**params))
        elif action == 'extract_info':
            return jsonify(research_app.extract_info(**params))
        elif action == 'research_assistant':
            return jsonify(research_app.research_assistant(**params))
        else:
            return jsonify({"error": "Invalid action specified"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
