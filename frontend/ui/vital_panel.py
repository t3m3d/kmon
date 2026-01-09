from PySide6.QtWidgets import QLabel, QVBoxLayout, QFrame
from PySide6.QtCore import Qt

from .styles import (
    BG_PANEL,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    FONT_FAMILY_MAIN,
)


class VitalPanel(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("StatsPanel")
        self.setStyleSheet(
            f"""
            QFrame#StatsPanel {{
                background-color: {BG_PANEL};
                border-radius: 4px;
                padding: 10px;
            }}
            QLabel {{
                font-family: {FONT_FAMILY_MAIN};
            }}
        """
        )

        layout = QVBoxLayout(self)
        layout.setSpacing(4)

        # Title
        self.title = QLabel("Live Stats")
        self.title.setStyleSheet(
            f"color: {TEXT_PRIMARY}; font-size: 14px; font-weight: 600;"
        )

        # Stats labels
        self.interface_label = QLabel("Interface: —")
        self.packets_sec_label = QLabel("Packets/sec: —")
        self.total_packets_label = QLabel("Total Packets: —")
        self.tcp_label = QLabel("TCP: —")
        self.udp_label = QLabel("UDP: —")
        self.icmp_label = QLabel("ICMP: —")
        self.bandwidth_label = QLabel("Bandwidth: —")

        # NEW — VPN status
        self.vpn_label = QLabel("VPN: —")

        for lbl in [
            self.interface_label,
            self.packets_sec_label,
            self.total_packets_label,
            self.tcp_label,
            self.udp_label,
            self.icmp_label,
            self.bandwidth_label,
            self.vpn_label,
        ]:
            lbl.setStyleSheet(f"color: {TEXT_SECONDARY}; font-size: 12px;")

        # Layout
        layout.addWidget(self.title)
        layout.addSpacing(6)
        layout.addWidget(self.interface_label)
        layout.addWidget(self.packets_sec_label)
        layout.addWidget(self.total_packets_label)
        layout.addWidget(self.tcp_label)
        layout.addWidget(self.udp_label)
        layout.addWidget(self.icmp_label)
        layout.addWidget(self.bandwidth_label)
        layout.addWidget(self.vpn_label)
        layout.addStretch()

    # Update panel with backend stats
    def update_stats(self, stats: dict):
        """Update system vitals panel with new data from the backend"""

        self.interface_label.setText(f"Interface: {stats.get('interface', '—')}")
        self.packets_sec_label.setText(f"Packets/sec: {stats.get('pps', '—')}")
        self.total_packets_label.setText(f"Total Packets: {stats.get('total', '—')}")
        self.tcp_label.setText(f"TCP: {stats.get('tcp', '—')}")
        self.udp_label.setText(f"UDP: {stats.get('udp', '—')}")
        self.icmp_label.setText(f"ICMP: {stats.get('icmp', '—')}")
        self.bandwidth_label.setText(f"Bandwidth: {stats.get('bandwidth', '—')} kbps")

        # NEW — VPN status
        vpn_active = stats.get("vpn_active", 0)
        vpn_type = stats.get("vpn_type", "")
        vpn_iface = stats.get("vpn_iface", "")

        if vpn_active:
            self.vpn_label.setText(f"VPN: {vpn_type} ({vpn_iface})")
        else:
            self.vpn_label.setText("VPN: None")