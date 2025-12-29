import json
import socket
import threading

class APIClient:
    def __init__(self, packet_cb, stats_cb):
        self.packet_cb = packet_cb
        self.stats_cb = stats_cb
        self.running = False

    def start(self):
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()

    def run(self):
        self.running = True
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", 9000))

        buffer = ""

        while self.running:
            data = sock.recv(4096).decode()
            buffer += data

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                self.handle_message(line)

    def handle_message(self, line):
        try:
            msg = json.loads(line)
        except:
            return

        if msg["type"] == "packet":
            self.packet_cb(msg["data"])
        elif msg["type"] == "stats":
            self.stats_cb(msg["data"])