import json
import random
import time

from PySide6.QtCore import QThread, Signal


class BackendClient(QThread):
    packet_received = Signal(dict)
    stats_updated = Signal(dict)
    interface_changed = Signal(str)
    status_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = True
        self._packets_total = 0
        self._last_stats_time = time.time()
        self._packets_in_interval = 0

    def run(self):
        # TODO: Replace this simulation with real backend integration.

        self.status_changed.emit("capturing")
        self.interface_changed.emit("Ethernet0")

        while self._running:
            # Simulate packet every 50ms
            time.sleep(0.05)
            packet = self._generate_fake_packet()
            self.packet_received.emit(packet)

            self._packets_total += 1
            self._packets_in_interval += 1

            now = time.time()
            if now - self._last_stats_time >= 1.0:
                pps = self._packets_in_interval
                stats = {
                    "packets_per_sec": pps,
                    "total_packets": self._packets_total,
                    "dropped_packets": 0,
                }
                self.stats_updated.emit(stats)
                self._packets_in_interval = 0
                self._last_stats_time = now

        self.status_changed.emit("stopped")

    def stop(self):
        self._running = False

    def _generate_fake_packet(self) -> dict:
        src_ips = ["192.168.1.10", "10.0.0.5", "192.168.1.22"]
        dst_ips = ["8.8.8.8", "1.1.1.1", "192.168.1.1"]
        protos = ["TCP", "UDP", "ICMP", "ARP"]
        flags_tcp = ["SYN", "ACK", "PSH", "FIN"]

        proto = random.choice(protos)
        length = random.randint(60, 1500)

        packet = {
            "timestamp": time.strftime("%H:%M:%S", time.localtime()),
            "src_ip": random.choice(src_ips),
            "dst_ip": random.choice(dst_ips),
            "protocol": proto,
            "length": length,
            "flags": "",
            "info": "",
            "hex_dump": "",
        }

        if proto == "TCP":
            packet["flags"] = ", ".join(random.sample(flags_tcp, k=2))
            packet["info"] = "TCP segment"
        elif proto == "UDP":
            packet["info"] = "UDP datagram"
        elif proto == "ICMP":
            packet["info"] = "ICMP echo request"
        elif proto == "ARP":
            packet["info"] = "ARP who has"

        # Fake hex dump
        hex_bytes = [f"{random.randint(0, 255):02x}" for _ in range(64)]
        lines = []
        for i in range(0, len(hex_bytes), 16):
            chunk = hex_bytes[i : i + 16]
            offset = f"{i:04x}"
            lines.append(f"{offset}  " + " ".join(chunk))
        packet["hex_dump"] = "\n".join(lines)

        return packet