import subprocess
import ipaddress
import platform
import socket

class NetworkScanner:
    def __init__(self):
        pass

    def _ping(self, ip):
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", "-w", "100", str(ip)]
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def _get_local_network(self):
        result = subprocess.check_output("ipconfig", text=True)
        ip, mask = None, None
        for line in result.splitlines():
            if "IPv4 Address" in line:
                ip = line.split(":")[1].strip()
            if "Subnet Mask" in line:
                mask = line.split(":")[1].strip()
        return ip, mask

    def scan(self):
        ip, mask = self._get_local_network()
        network = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)

        for host in network.hosts():
            self._ping(host)

        arp_output = subprocess.check_output("arp -a", text=True)
        devices = []

        for line in arp_output.splitlines():
            if "-" in line:
                parts = line.split()
                ip_addr = parts[0]
                mac_addr = parts[1]
                try:
                    hostname = socket.gethostbyaddr(ip_addr)[0]
                except:
                    hostname = "Unknown"
                devices.append((ip_addr, mac_addr, hostname))

        return devices