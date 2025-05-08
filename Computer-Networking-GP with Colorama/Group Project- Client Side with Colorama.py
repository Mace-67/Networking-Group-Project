import socket
from colorama import Fore, Back, Style
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

# Load server's public key
with open("public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

def start_client():
    server_address = ('127.0.0.1', 8080)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(server_address)

    try:
        print(Fore.LIGHTGREEN_EX + "✅ Connected Successfully" +Style.RESET_ALL)
        print(Fore.LIGHTMAGENTA_EX + "Press 'q' to end the chat" +Style.RESET_ALL)
        while True:
            message = input(Fore.GREEN + "You: " + Style.RESET_ALL)
            if message.lower() in ['q', 'bye', 'goodbye']:
                print(Fore.RED + "\nEnding session." + Style.RESET_ALL)
                break

            # Encrypt message
            encrypted = public_key.encrypt(
                message.encode(),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            # Send encrypted message
            client.sendall(len(encrypted).to_bytes(4, 'big'))
            client.sendall(encrypted)

            # Wait for server reply
            length_bytes = client.recv(4)
            if not length_bytes:
                print(Back.RED + "\nServer Closed Messaging." + Style.RESET_ALL)
                break
            reply_length = int.from_bytes(length_bytes, 'big')

            reply_data = b''
            while len(reply_data) < reply_length:
                chunk = client.recv(reply_length - len(reply_data))
                if not chunk:
                    break
                reply_data += chunk

            server_reply = reply_data.decode()
            print(Fore.LIGHTYELLOW_EX+ "Server:"+Style.RESET_ALL+ f" {server_reply}")

            if server_reply.lower() in ['q', 'bye']:
                print(Back.RED +"\nServer ended the session." + Style.RESET_ALL)
                break

    finally:
        client.close()

start_client()
