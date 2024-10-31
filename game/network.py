import socket
import json
from game.settings import *
from _thread import start_new_thread

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(20)
        self.server = "127.0.0.1"
        # self.server = "192.168.1.9"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()
        self.local_data = {
            'flag' : 2,
            'id' : "",
            'player' : {
                'pos' : (1500,1500),
                'hp' : 100,
                'angle': 90,
                'local_bullets' : [],
                'online_bullets' : [],
                'weapon': None,
            },
        }
        self.server_data = {}

    def player_init(self, player_id):
        init_data = {
            'flag' : 1,
            'id' : player_id,
        }
        self.client.send(json.dumps(init_data).encode())

    def connect(self):
        try:
            self.client.connect(self.addr)
            print("connected to server")
        except socket.timeout:
            print("Connection timed out.")
        except Exception as e:
            print(f"Connection failed: {e}")

    def fetch_data(self):
        try:
            self.client.send(json.dumps(self.local_data).encode())
            self.server_data = json.loads(self.client.recv(MAX_DATA_SIZE).decode())
        except socket.timeout:
            print("Send/receive operation timed out.")
        except socket.error as e:
            print(f"Socket error: {e}")        
            
    def listen(self):
        return self.client.recv(MAX_DATA_SIZE).decode()
    
    def shut_down(self):
        try:
            self.client.shutdown(socket.SHUT_RDWR)  # Use SHUT_RDWR for proper shutdown
            self.client.close()
        except Exception as e:
            print(f"Error during shutdown: {e}")