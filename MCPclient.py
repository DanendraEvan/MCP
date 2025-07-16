import requests  # Ganti socket dengan requests

class MCPClient:
    def __init__(self, host='https://web-production-e2a95.up.railway.app', port=None):
        self.base_url = host
        if port:
            self.base_url = f"{host}:{port}"
            
    def send_request(self, action, params=None):
        if params is None:
            params = {}
            
        try:
            response = requests.post(
                f"{self.base_url}/api",
                json={"action": action, "params": params},
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    client = MCPClient()
    print(client.send_request("search_papers", {"topic": "quantum computing", "max_results": 3}))
