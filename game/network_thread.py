import socket
import json
import queue
from game.settings import *
from threading import Thread

class NetworkThread:
    def __init__(self, server="127.0.0.1", port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(20)
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)
        self.running = True
        self.incoming_data_queue = queue.Queue()
        self.outgoing_data_queue = queue.Queue()
        
        self.connect()
        
    def connect(self):
        try:
            self.client.connect(self.addr)
            print("Connected to server")
        except socket.timeout:
            print("Connection timed out.")
            self.running = False
        except Exception as e:
            print(f"Connection failed: {e}")
            self.running = False

    def player_init(self, player_id, team):
        init_data = {
            'flag': 1,
            'id': player_id,
            'team': team
        }
        self.send_data(init_data)
        
    def send_data(self, data):
        if self.running:
            self.outgoing_data_queue.put(data)
        
    def receive_data(self):
        if not self.incoming_data_queue.empty():
            return self.incoming_data_queue.get()
        return None

    def networking_thread(self):
        while self.running:
            try:
                server_data = json.loads(self.client.recv(MAX_DATA_SIZE).decode())
                self.incoming_data_queue.put(server_data)
                
                if not self.outgoing_data_queue.empty():
                    data_to_send = self.outgoing_data_queue.get()
                    self.client.send(json.dumps(data_to_send).encode())
                    
            except socket.error as e:
                print(f"Socket error: {e}")
                break
            except json.JSONDecodeError as e:
                print(f"Data decoding error: {e}")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                break
            
        self.shutdown()

    def run(self):
        self.network_thread = Thread(target=self.networking_thread, daemon=True)
        self.network_thread.start()
    
    def shutdown(self):
        self.running = False
        try:
            self.client.shutdown(socket.SHUT_RDWR)
            self.client.close()
            print("Disconnected from server")
        except Exception as e:
            print(f"Error during shutdown: {e}")
