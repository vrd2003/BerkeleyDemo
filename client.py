
import socket
import math
import os

HOST = "0.0.0.0"
PORT = 5000
BUFFER = 4096


def receive_line(conn):
    data = b""
    while not data.endswith(b"\n"):
        part = conn.recv(1)
        if not part:
            return ""
        data += part
    return data.decode().strip()


def send_line(conn, message):
    conn.sendall((str(message) + "\n").encode())


def handle_client(conn, addr):
    print("Connected to:", addr)

    try:
        send_line(conn, "Connected to TCP Server")

        while True:
            request = receive_line(conn)

            if not request or request == "EXIT":
                break

            if request == "HELLO":
                send_line(conn, "Hello Client! Greetings from Server.")

            elif request == "ARITHMETIC":
                expr = receive_line(conn)
                try:
                    a, op, b = expr.split()
                    a, b = float(a), float(b)

                    if op == "+":
                        result = a + b
                    elif op == "-":
                        result = a - b
                    elif op == "*":
                        result = a * b
                    elif op == "/" and b != 0:
                        result = a / b
                    else:
                        result = "Invalid operator or division by zero"

                    send_line(conn, result)
                except ValueError:
                    send_line(conn, "Invalid expression")

            elif request == "TRIG":
                expr = receive_line(conn)
                try:
                    function, angle = expr.split()
                    angle = float(angle)
                    radians = math.radians(angle)

                    functions = {
                        "sin": math.sin,
                        "cos": math.cos,
                        "tan": math.tan
                    }

                    if function not in functions:
                        send_line(conn, "Invalid function")
                    elif function == "tan" and abs(math.cos(radians)) < 1e-10:
                        send_line(conn, "Undefined: tangent at this angle")
                    else:
                        send_line(conn, functions[function](radians))
                except ValueError:
                    send_line(conn, "Invalid input")

            elif request == "FILE":
                filename = receive_line(conn)
                size_text = receive_line(conn)

                try:
                    size = int(size_text)
                    if size < 0 or size > 100_000_000:
                        send_line(conn, "ERROR")
                        continue
                except ValueError:
                    send_line(conn, "ERROR")
                    continue

                send_line(conn, "READY")

                safe_name = os.path.basename(filename)
                received = 0

                with open("received_" + safe_name, "wb") as file:
                    while received < size:
                        chunk = conn.recv(min(BUFFER, size - received))
                        if not chunk:
                            raise ConnectionError("File transfer interrupted")
                        file.write(chunk)
                        received += len(chunk)

                send_line(conn, "File received successfully")

            else:
                send_line(conn, "Unknown request")

    except (ConnectionError, OSError) as error:
        print("Connection error:", error)

    finally:
        conn.close()
        print("Client disconnected:", addr)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)

        print("TCP Server running on port", PORT)

        while True:
            conn, addr = server.accept()
            handle_client(conn, addr)


if __name__ == "__main__":
    main()
