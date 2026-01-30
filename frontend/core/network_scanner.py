import subprocess
import ipaddress
import socket
import re


class NetworkScanner:
    def __init__(self):
        pass

    def _get_local_ip_and_gateway(self):
        try:
            output = subprocess.check_output(
                "ipconfig", text=True, encoding="utf-8", errors="ignore"
            )
        except Exception:
            return None, None

        ip = None
        gw = None
        in_wifi_block = False

        for line in output.splitlines():
            line = line.strip()

            if "Wireless LAN adapter Wi-Fi" in line:
                in_wifi_block = True
                continue

            if in_wifi_block:
                if line == "":
                    break  # end of block

                if "IPv4 Address" in line:
                    m = re.search(r"IPv4.*?:\s*([\d\.]+)", line)
                    if m:
                        ip = m.group(1)

                if "Default Gateway" in line:
                    m = re.search(r"Default Gateway.*?:\s*([\d\.]+)", line)
                    if m:
                        g = m.group(1)
                        if g and g != "0.0.0.0":
                            gw = g

        return ip, gw

    def _load_arp_table(self):
        arp_map = {}
        try:
            output = subprocess.check_output(
                "arp -a", text=True, encoding="utf-8", errors="ignore"
            )
        except Exception:
            return arp_map

        for line in output.splitlines():
            line = line.strip()
            m = re.match(r"^(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F\-]{17})", line)
            if m:
                ip_addr = m.group(1)
                mac_addr = m.group(2).lower()
                if mac_addr not in ["ff-ff-ff-ff-ff-ff", "00-00-00-00-00-00"]:
                    arp_map[ip_addr] = mac_addr

        return arp_map

    def scan(self):
        local_ip, gateway = self._get_local_ip_and_gateway()
        if not local_ip:
            print("ERROR: Could not determine local IP")
            return []

        net = ipaddress.IPv4Network(local_ip + "/24", strict=False)
        print("Scanning subnet:", net)

        try:
            subprocess.call(
                ["ping", "-n", "1", "-w", "100", str(net.broadcast_address)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except Exception:
            pass

        arp_map = self._load_arp_table()
        devices = []

        try:
            hostname = socket.gethostname()
        except Exception:
            hostname = "LocalHost"

        devices.append((local_ip, arp_map.get(local_ip, "Unknown"), hostname))

        if gateway:
            devices.append((gateway, arp_map.get(gateway, "Unknown"), "Default Gateway"))

        for ip, mac in arp_map.items():
            if ip in [local_ip, gateway]:
                continue
            try:
                host = socket.gethostbyaddr(ip)[0]
            except Exception:
                host = "Unknown"
            devices.append((ip, mac, host))

        unique = {ip: (ip, mac, name) for ip, mac, name in devices}
        final = list(unique.values())
        print(f"Found {len(final)} device(s)")
        return final