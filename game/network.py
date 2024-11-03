import socket
import json
from game.settings import *

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Change to UDP
        self.client.settimeout(20)
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
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

    def respawn_request(self, player_id):
        respawn_data = {
            'flag' : 3,
            'id' : player_id,
        }
        # Send respawn request to the server
        self.client.sendto(json.dumps(respawn_data).encode(), self.addr)

    def player_init(self, player_id, team):
        init_data = {
            'flag' : 1,
            'id' : player_id,
            'team' : team
        }
        # Send initialization data to the server
        self.client.sendto(json.dumps(init_data).encode(), self.addr)

    def fetch_data(self):
        try:
            # Send player data to the server
            self.client.sendto(json.dumps(self.local_data).encode(), self.addr)
            
            # Receive data from the server
            data, _ = self.client.recvfrom(MAX_DATA_SIZE)
            self.server_data = json.loads(data.decode())
        except socket.timeout:
            print("Send/receive operation timed out.")
        except socket.error as e:
            print(f"Socket error: {e}")

    def listen(self):
        try:
            data, _ = self.client.recvfrom(MAX_DATA_SIZE)
            return data.decode()
        except socket.timeout:
            print("Listening operation timed out.")
        except socket.error as e:
            print(f"Socket error while listening: {e}")
            return None
    
    def shut_down(self):
        try:
            self.client.close()  # For UDP, close the socket directly
        except Exception as e:
            print(f"Error during shutdown: {e}")
