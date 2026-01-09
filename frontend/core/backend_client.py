import json
import socket
import time

from PySide6.QtCore import QThread, Signal


class BackendClient(QThread):
    packet_received = Signal(dict)
    stats_updated = Signal(dict)
    interface_changed = Signal(str)
    status_changed = Signal(str)

    def __init__(self, host="127.0.0.1", port=9090, parent=None):
        super().__init__(parent)
        self.host = host
        self.port = port
        self._running = True
        self.sock = None

    # Thread entry point
    def run(self):
        self.status_changed.emit("connecting")

        # Try to connect to backend
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.sock.settimeout(1.0)
            self.status_changed.emit("capturing")
        except Exception as e:
            self.status_changed.emit(f"error: {e}")
            return

        buffer = ""

        while self._running:
            try:
                data = self.sock.recv(4096)

                if not data:
                    self.status_changed.emit("backend disconnected")
                    break

                buffer += data.decode("utf-8")

                # Process complete JSON lines
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if not line.strip():
                        continue

                    try:
                        msg = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    self._handle_message(msg)

            except socket.timeout:
                continue
            except Exception as e:
                self.status_changed.emit(f"error: {e}")
                break

        self.status_changed.emit("stopped")

    # Stop thread
    def stop(self):
        self._running = False
        try:
            if self.sock:
                self.sock.close()
        except:
            pass

    # Handle backend JSON messages
    def _handle_message(self, msg):
        msg_type = msg.get("type")
        data = msg.get("data", {})

        if msg_type == "packet":
            self.packet_received.emit(data)

        elif msg_type == "stats":
            # Stats include VPN fields now:
            #   vpn_active
            #   vpn_type
            #   vpn_iface
            self.stats_updated.emit(data)

        elif msg_type == "interface":
            iface = data.get("name", "unknown")
            self.interface_changed.emit(iface)