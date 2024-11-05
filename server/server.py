import socket
import json
import sys
from _thread import *
from pydantic import BaseModel
from settings import *
from room import *

HOST = "127.0.0.1"
PORT = 5555

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
print("Server started, waiting for connections...")

    
test_room = Room('room1')
server_data = {    
    'room1' : test_room
}

def handle_client_data(client_data, conn : socket):
    try:
        if client_data['flag'] == 1: # player info to server
            client_id = client_data['data']['id']
            client_room = client_data['data']['room']
            server_data[client_room][client_id] = client_data['data']
            conn.send(json.dumps(server_data[client_room]).encode())
    except Exception as e:
        print(f'client {conn} error {e}')





def broadcast(message):
    """Send a message to all connected clients."""
    for client in clients:
        try:
            client.send(message)
        except socket.error as e:
            print(f"Error sending message to a client: {e}")
            client.close()
            clients.remove(client) 
            
def thread_client(conn):
    clients.append(conn) 
    client_id = ""
    while True:
        try:
            data = conn.recv(MAX_DATA_SIZE)
            if not data:
                print("Client disconnected")
                break
            client_data = Message()
            print(data)
            client_data.model_validate(data)
            handle_client_data(client_data, conn)
        except Exception as e:
            print(f"Error: {e}")
            break

    conn.close()
    server_data.pop(client_id)
    clients.remove(conn)  # Remove the client from the list



try:
    while True:
        conn, addr = s.accept()
        print(f"Connected to: {addr}")
        start_new_thread(thread_client, (conn,))
except KeyboardInterrupt:
    print("\nShutting down the server...")

finally:
    s.close()
    for client in clients:
        client.close()
    print("Server closed.")
    sys.exit(0)
