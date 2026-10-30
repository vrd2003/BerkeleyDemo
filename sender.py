
import socket
import os
import json
import struct

PORT = 5001
CHUNK_SIZE = 1200
TIMEOUT = 2
MAX_RETRIES = 10


def receive_ack(sock, expected):
    packet, _ = sock.recvfrom(1024)
    return (
        len(packet) == 5
        and packet[0:1] == b"A"
        and struct.unpack("!I", packet[1:5])[0] == expected
    )


def send_reliably(sock, packet, expected):
    for attempt in range(MAX_RETRIES):
        sock.sendto(packet, DESTINATION)
        try:
            if receive_ack(sock, expected):
                return True
        except socket.timeout:
            print("Timeout; retry", attempt + 1)

    return False


def main():
    global DESTINATION

    ip = input("Enter receiver IPv4 address: ").strip()
    DESTINATION = (ip, PORT)

    categories = ["Script", "Text", "Audio", "Video"]

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.settimeout(TIMEOUT)

        for category in categories:
            path = input(f"Enter {category} file path: ").strip().strip('"')

            if not os.path.isfile(path):
                print("File not found:", path)
                return

            size = os.path.getsize(path)
            total = (size + CHUNK_SIZE - 1) // CHUNK_SIZE

            metadata = {
                "filename": os.path.basename(path),
                "size": size,
                "chunks": total
            }

            # Send metadata and wait for READY
            ready = False
            for attempt in range(MAX_RETRIES):
                client.sendto(
                    b"M" + json.dumps(metadata).encode(),
                    DESTINATION
                )
                try:
                    response, _ = client.recvfrom(1024)
                    if response == b"R":
                        ready = True
                        break
                except socket.timeout:
                    print("Waiting for receiver... retry", attempt + 1)

            if not ready:
                print("Receiver did not respond. Transfer stopped.")
                return

            print("\nSending", category, "file:", path)

            with open(path, "rb") as file:
                for seq in range(total):
                    data = file.read(CHUNK_SIZE)
                    packet = b"D" + struct.pack("!I", seq) + data

                    if not send_reliably(client, packet, seq):
                        print("Transfer failed at chunk", seq)
                        return

                    print(f"\rProgress: {seq + 1}/{total}", end="")

            print("\nFile transfer completed:", os.path.basename(path))

        client.sendto(b"Q", DESTINATION)
        print("\nAll four files sent.")


if __name__ == "__main__":
    main()
