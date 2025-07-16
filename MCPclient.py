import socket
import json

class MCPClient:
    def __init__(self, host='web-production-e2a95.up.railway.app', port=5000):
        self.host = host
        self.port = port
        
    def send_request(self, action, params=None):
        if params is None:
            params = {}
            
        request = {
            "action": action,
            "params": params
        }
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.send(json.dumps(request).encode('utf-8'))
                response = s.recv(1024).decode('utf-8')
                return json.loads(response)
        except Exception as e:
            return {"error": str(e)}

# Example usage:
if __name__ == "__main__":
    client = MCPClient()
    
    # Example requests
    print(client.send_request("search_papers", {"topic": "quantum computing", "max_results": 3}))
    print(client.send_request("research_assistant", {"query": "What is quantum computing?"}))
