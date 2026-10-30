
import socket
import json
import os
import struct

HOST = "0.0.0.0"
PORT = 5001
CHUNK_SIZE = 1200
TIMEOUT = 2
MAX_RETRIES = 10

# Packet types: M = metadata, D = data, A = acknowledgement,
# R = ready, Q = quit


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((HOST, PORT))
        print("UDP Receiver listening on port", PORT)

        while True:
            packet, sender = server.recvfrom(65507)

            if packet == b"Q":
                print("Transfer session completed.")
                break

            if not packet.startswith(b"M"):
                continue

            try:
                meta = json.loads(packet[1:].decode())
                filename = os.path.basename(meta["filename"])
                size = int(meta["size"])
                total = int(meta["chunks"])

                if size < 0 or total < 0 or total > 1000000:
                    continue
            except (ValueError, KeyError, TypeError):
                continue

            print("\nReceiving:", filename, "Size:", size, "bytes")
            server.sendto(b"R", sender)

            os.makedirs("received_files", exist_ok=True)
            output_path = os.path.join("received_files", filename)

            expected = 0
            written = 0

            with open(output_path, "wb") as file:
                while expected < total:
                    packet, addr = server.recvfrom(65507)

                    if addr != sender or not packet.startswith(b"D"):
                        continue

                    if len(packet) < 5:
                        continue

                    seq = struct.unpack("!I", packet[1:5])[0]
                    payload = packet[5:]

                    if seq == expected:
                        file.write(payload)
                        written += len(payload)
                        expected += 1

                    # ACK current or previously received packet.
                    # This also handles retransmitted duplicate packets.
                    if seq < expected:
                        server.sendto(
                            b"A" + struct.pack("!I", seq), sender
                        )
                    elif seq == expected:
                        server.sendto(
                            b"A" + struct.pack("!I", expected - 1),
                            sender
                        )

            if written == size:
                print("Saved:", output_path)
                print("File received successfully.")
            else:
                print("Warning: file size mismatch.")

        print("Receiver stopped.")


if __name__ == "__main__":
    main()
