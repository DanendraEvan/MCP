import requests
import os

class MCPClient:
    def __init__(self, host=None):
        self.base_url = host or os.getenv('SERVER_URL', 'http://localhost:5000')
        if not self.base_url.startswith(('http://', 'https://')):
            self.base_url = f"http://{self.base_url}"
            
    def send_request(self, action, params=None):
        try:
            response = requests.post(
                f"{self.base_url}/api",
                json={
                    "action": action,
                    "params": params or {}
                },
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

if __name__ == "__main__":
    client = MCPClient()
    print(client.send_request("ping"))
