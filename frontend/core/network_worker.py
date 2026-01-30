from PySide6.QtCore import QThread, Signal
from frontend.core.network_scanner import NetworkScanner

class NetworkScanWorker(QThread):
    result = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        print("Worker __init__ called")  # DEBUG
        self.scanner = NetworkScanner()

    def run(self):
        print("Worker thread STARTED")  # DEBUG
        try:
            devices = self.scanner.scan()
            print("Worker thread GOT DEVICES:", devices)  # DEBUG
            self.result.emit(devices)
        except Exception as e:
            print("Worker thread ERROR:", e)
        print("Worker thread ENDING")  # DEBUG
        return