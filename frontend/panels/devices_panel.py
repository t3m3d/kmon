# frontend/panels/devices_panel.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PySide6.QtCore import QThread, Signal
from frontend.core.network_scanner import NetworkScanner


class NetworkScanWorker(QThread):
    result = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scanner = NetworkScanner()

    def run(self):
        print("Worker thread STARTED")  # DEBUG
        devices = self.scanner.scan()
        print("Worker thread GOT DEVICES")  # DEBUG
        self.result.emit(devices)
        print("Worker thread ENDING")  # DEBUG
        return


class DevicesPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.refresh_btn = QPushButton("Scan Network")
        self.refresh_btn.clicked.connect(self.run_scan)
        layout.addWidget(self.refresh_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["IP Address", "MAC Address", "Hostname"])
        layout.addWidget(self.table)

        self.worker = None

    def run_scan(self):
        print("run_scan() CALLED")  # DEBUG
        self.refresh_btn.setEnabled(False)
        self.refresh_btn.setText("Scanning...")

        self.worker = NetworkScanWorker(self)
        self.worker.result.connect(self.update_table)
        self.worker.finished.connect(self.scan_finished)
        self.worker.start()

    def update_table(self, devices):
        print("update_table() CALLED with", len(devices), "devices")  # DEBUG
        self.table.setRowCount(len(devices))
        for row, (ip, mac, host) in enumerate(devices):
            self.table.setItem(row, 0, QTableWidgetItem(ip))
            self.table.setItem(row, 1, QTableWidgetItem(mac))
            self.table.setItem(row, 2, QTableWidgetItem(host))

    def scan_finished(self):
        print("scan_finished() CALLED")  # DEBUG
        self.refresh_btn.setEnabled(True)
        self.refresh_btn.setText("Scan Network")
        self.worker = None