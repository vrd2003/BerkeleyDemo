
import socket
import os

HOST = input("Enter server IP (127.0.0.1 for same PC): ").strip()
PORT = 5000


def receive_line(sock):
    data = b""
    while not data.endswith(b"\n"):
        part = sock.recv(1)
        if not part:
            raise ConnectionError("Server disconnected")
        data += part
    return data.decode().strip()


def send_line(sock, message):
    sock.sendall((str(message) + "\n").encode())


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        print(receive_line(client))

        while True:
            print("\n1. Say Hello")
            print("2. File Transfer")
            print("3. Arithmetic Calculator")
            print("4. Trigonometry Calculator")
            print("5. Exit")

            choice = input("Enter choice: ").strip()

            if choice == "1":
                send_line(client, "HELLO")
                print("Server:", receive_line(client))

            elif choice == "2":
                path = input("Enter file path: ").strip().strip('"')

                if not os.path.isfile(path):
                    print("File not found")
                    continue

                filename = os.path.basename(path)
                size = os.path.getsize(path)

                send_line(client, "FILE")
                send_line(client, filename)
                send_line(client, size)

                if receive_line(client) != "READY":
                    print("Server rejected file transfer")
                    continue

                with open(path, "rb") as file:
                    while True:
                        chunk = file.read(4096)
                        if not chunk:
                            break
                        client.sendall(chunk)

                print("Server:", receive_line(client))

            elif choice == "3":
                a = input("Enter first number: ")
                op = input("Enter operator (+, -, *, /): ").strip()
                b = input("Enter second number: ")

                try:
                    float(a)
                    float(b)
                    if op not in ("+", "-", "*", "/"):
                        raise ValueError
                except ValueError:
                    print("Invalid input")
                    continue

                send_line(client, "ARITHMETIC")
                send_line(client, f"{a} {op} {b}")
                print("Result:", receive_line(client))

            elif choice == "4":
                function = input("Function (sin/cos/tan): ").strip().lower()

                if function not in ("sin", "cos", "tan"):
                    print("Invalid function")
                    continue

                try:
                    angle = float(input("Enter angle in degrees: "))
                except ValueError:
                    print("Invalid angle")
                    continue

                send_line(client, "TRIG")
                send_line(client, f"{function} {angle}")
                print("Result:", receive_line(client))

            elif choice == "5":
                send_line(client, "EXIT")
                print("Disconnected.")
                break

            else:
                print("Invalid choice")


if __name__ == "__main__":
    main()
