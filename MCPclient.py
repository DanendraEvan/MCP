import requests
import os

class MCPClient:
    def __init__(self, host=None, port=None):
        self.base_url = host or os.getenv('SERVER_URL', 'https://mcp-production-7472.up.railway.app')
        if port:
            self.base_url = f"{self.base_url}:{port}"
            
    def send_request(self, action, params=None):
        if params is None:
            params = {}
            
        try:
            response = requests.post(
                f"{self.base_url}/api",
                json={"action": action, "params": params},
                timeout=10
            )
            response.raise_for_status()  # Ini akan memunculkan exception untuk HTTP error
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"HTTP request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

if __name__ == "__main__":
    client = MCPClient()
    print(client.send_request("ping"))  # Test koneksi dasar
