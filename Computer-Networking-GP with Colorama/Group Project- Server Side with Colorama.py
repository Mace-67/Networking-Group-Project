import socket
from colorama import Fore, Back, Style
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

# Load private key
with open("private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8080)) #IP address with port number 
    server.listen(1)
    print(Fore.CYAN + Style.DIM +"Server listening on 127.0.0.1:8080..."+Style.RESET_ALL)

    conn, addr = server.accept()
    print(Fore.MAGENTA + Style.DIM + "\nConnection from"+Style.RESET_ALL+ f" {addr}")

    try:
        print(Fore.LIGHTBLUE_EX + "Waiting for Client to send message..." +Style.RESET_ALL)
        print(Fore.LIGHTMAGENTA_EX + "Press 'q' to end the chat" +Style.RESET_ALL)
        while True:
            # Receive message length
            length_bytes = conn.recv(4)
            if not length_bytes:
                break
            message_length = int.from_bytes(length_bytes, 'big')

            # Receive the encrypted message
            encrypted_message = b''
            while len(encrypted_message) < message_length:
                chunk = conn.recv(message_length - len(encrypted_message))
                if not chunk:
                    break
                encrypted_message += chunk

            # Decrypt
            try:
                decrypted = private_key.decrypt(
                    encrypted_message,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
            except Exception as e:
                print(Fore.YELLOW + "⚠️ Decryption error:" +Style.RESET_ALL + f" {e}")
                break

            client_msg = decrypted.decode()
            print(Fore.LIGHTYELLOW_EX+"Client:"+Style.RESET_ALL+ f" {client_msg}")

            if client_msg.lower() in ['q', 'bye', 'goodbye']:
                print(Back.RED+"\nClient ended the session."+Style.RESET_ALL)
                break

            # Send message back to client (plaintext)
            server_reply = input(Fore.GREEN+"Server: "+Style.RESET_ALL)
            if server_reply.lower() in ['q', 'bye','goodbye']:
                print(Fore.RED+"\nEnding session."+Style.RESET_ALL)
                break

            # Send plaintext reply (no encryption)
            conn.sendall(len(server_reply.encode()).to_bytes(4, 'big'))
            conn.sendall(server_reply.encode())

    finally:
        conn.close()
        server.close()
        print(Back.YELLOW+"\nConnection closed."+Style.RESET_ALL)

start_server()
