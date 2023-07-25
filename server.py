import socket
import threading

def handle_client(client_socket, address):
    # try:
    #     while True:
    #         message = client_socket.recv(1024).decode('utf-8')
    #         if message == 'exit':
    #             break
    #         # Send the message to the paired client, if available
    #         send_to_paired_client(message, client_socket, address)
    # except ConnectionResetError:
    #     print(f"Connection with {address} closed.")
    # finally:
    #     client_socket.close()
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'exit':
                for clientObj in clients:
                    clientObj[0].sendall("pleaseEnd".encode())
                break
            else:
                send_to_paired_client(message, client_socket, address)
            # Send the message to the paired client, if available
            
    except ConnectionResetError:
        print(f"Connection with {address} closed.")
    finally:
        # Notify the paired client that the other client exited the chat
        '''send_to_paired_client("Your chat partner has exited the chat.", client_socket, address)
        client_socket.close()

        # Remove the pair for the disconnected client
        pair = get_pair(address)
        if pair:
            client_pairs.remove(pair)'''

def send_to_paired_client(message, sender_socket, sender_address):
    sender_pair = get_pair(sender_address)
    if sender_pair:
        for client, address in clients:
            if address == sender_pair and client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))

                except ConnectionResetError:
                    print(f"Connection with {address} closed.")
                    remove_client(client)

def get_pair(address):
    for pair in client_pairs:
        if address in pair:
            return pair[0] if pair[0] != address else pair[1]
    return None

def remove_client(client_socket):
    for client, address in clients:
        if client == client_socket:
            clients.remove((client, address))
            # Remove the pair for the disconnected client
            pair = get_pair(address)
            if pair:
                client_pairs.remove(pair)
            break

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    host = socket.gethostbyname('44.211.75.62')
    port = 1122
    server_socket.bind((host, port))

    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")

        clients.append((client_socket, client_address))

        # Create pairs for clients
        if len(clients) % 2 == 0:
            client_pairs.append((clients[-2][1], clients[-1][1]))

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

    server_socket.close()

if __name__ == "__main__":
    clients = []  # List to store connected clients and their addresses
    client_pairs = []  # List to store paired client addresses
    main()
