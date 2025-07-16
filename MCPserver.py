import socket
import json
from threading import Thread
from research_app import ResearchApp  # Sekarang mengimpor dari file yang benar

class MCPServer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.research_app = ResearchApp()
        
    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"MCP Server listening on {self.host}:{self.port}")
        
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Connection from {addr}")
            Thread(target=self.handle_client, args=(client_socket,)).start()
    
    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                    
                try:
                    request = json.loads(data)
                    response = self.process_request(request)
                    client_socket.send(json.dumps(response).encode('utf-8'))
                except json.JSONDecodeError:
                    response = {"error": "Invalid JSON format"}
                    client_socket.send(json.dumps(response).encode('utf-8'))
                    
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            client_socket.close()
    
    def process_request(self, request):
        action = request.get('action')
        params = request.get('params', {})
        
        try:
            if action == 'search_papers':
                return self.research_app.search_papers(**params)
            elif action == 'get_paper_content':
                return self.research_app.get_paper_content(**params)
            elif action == 'extract_info':
                return self.research_app.extract_info(**params)
            elif action == 'research_assistant':
                return self.research_app.research_assistant(**params)
            else:
                return {"error": "Invalid action specified"}
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    server = MCPServer()
    server.start()
