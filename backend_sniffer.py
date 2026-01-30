import json
import socket
import threading
import time
import pcapy
import struct
import socket as pysocket

HOST = "127.0.0.1"
PORT = 9090

# Utility: Get system IP
def get_system_ip():
    try:
        s = pysocket.socket(pysocket.AF_INET, pysocket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "unknown"


# Packet Parsing
def parse_packet(header, data):
    if len(data) < 34:
        return None

    eth_header = data[:14]
    eth = struct.unpack("!6s6sH", eth_header)
    eth_protocol = eth[2]

    if eth_protocol != 0x0800:  # IPv4 only
        return None

    ip_header = data[14:34]
    iph = struct.unpack("!BBHHHBBH4s4s", ip_header)

    protocol = iph[6]
    src_ip = pysocket.inet_ntoa(iph[8])
    dst_ip = pysocket.inet_ntoa(iph[9])

    proto_name = {1: "ICMP", 6: "TCP", 17: "UDP"}.get(protocol, str(protocol))

    return {
        "src": src_ip,
        "dst": dst_ip,
        "protocol": proto_name,
        "length": len(data),
        "info": f"{proto_name} packet {src_ip} → {dst_ip}"
    }

# Backend Sniffer Server
class BackendSniffer:
    def __init__(self):
        self.client = None
        self.stats = {
            "total_packets": 0,
            "tcp": 0,
            "udp": 0,
            "icmp": 0,
            "other": 0,
        }

    def start(self):
        print("[Backend] Starting server on port 9090...")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(1)

        self.client, _ = server.accept()
        print("[Backend] Frontend connected.")

        # Send interface info
        iface = pcapy.findalldevs()[0]
        self.send_json("interface", {"name": iface})

        # Start sniffer thread
        threading.Thread(target=self.sniff, daemon=True).start()

        # Stats loop
        while True:
            self.send_json("stats", self.stats)
            time.sleep(1)

    def send_json(self, msg_type, data):
        if not self.client:
            return
        msg = json.dumps({"type": msg_type, "data": data}) + "\n"
        try:
            self.client.sendall(msg.encode())
        except:
            pass

    def sniff(self):
        iface = pcapy.findalldevs()[0]
        cap = pcapy.open_live(iface, 65536, 1, 0)

        print(f"[Backend] Sniffing on {iface}...")

        while True:
            header, packet = cap.next()
            if not packet:
                continue

            parsed = parse_packet(header, packet)
            if not parsed:
                continue

            # Update stats
            self.stats["total_packets"] += 1
            proto = parsed["protocol"].lower()
            if proto in self.stats:
                self.stats[proto] += 1
            else:
                self.stats["other"] += 1

            # Send packet to frontend
            self.send_json("packet", parsed)


# Run backend
if __name__ == "__main__":
    BackendSniffer().start()