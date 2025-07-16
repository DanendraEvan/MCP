from flask import Flask
from MCPserver import MCPServer
import threading

app = Flask(__name__)

# Jalankan MCPServer di thread terpisah
server = MCPServer(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
threading.Thread(target=server.start, daemon=True).start()

@app.route("/")
def home():
    return "MCP Server is running."

if __name__ == "__main__":
    app.run()
