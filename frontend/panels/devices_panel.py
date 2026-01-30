from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from frontend.core.network_scanner import NetworkScanner

class DevicesPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.scanner = NetworkScanner()

        layout = QVBoxLayout(self)

        self.refresh_btn = QPushButton("Scan Network")
        self.refresh_btn.clicked.connect(self.run_scan)
        layout.addWidget(self.refresh_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["IP Address", "MAC Address", "Hostname"])
        layout.addWidget(self.table)

    def run_scan(self):
        devices = self.scanner.scan()
        self.table.setRowCount(len(devices))

        for row, (ip, mac, host) in enumerate(devices):
            self.table.setItem(row, 0, QTableWidgetItem(ip))
            self.table.setItem(row, 1, QTableWidgetItem(mac))
            self.table.setItem(row, 2, QTableWidgetItem(host))