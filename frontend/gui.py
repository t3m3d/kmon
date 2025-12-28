import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from charts import BandwidthChart
from tables import PacketTable
from api_client import APIClient

class KMonGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("kmon — Network Monitor")
        self.setMinimumSize(900, 600)

        # API client (receives data from C backend)
        self.api = APIClient(self.handle_packet, self.handle_stats)

        # Layout
        central = QWidget()
        layout = QVBoxLayout()
        central.setLayout(layout)
        self.setCentralWidget(central)

        # Charts + tables
        self.chart = BandwidthChart()
        self.table = PacketTable()

        layout.addWidget(self.chart)
        layout.addWidget(self.table)

        # Start receiving data
        self.api.start()

    def handle_packet(self, pkt):
        """Called when backend sends a parsed packet."""
        self.table.add_packet(pkt)

    def handle_stats(self, stats):
        """Called when backend sends stats snapshot."""
        self.chart.update_stats(stats)

def main():
    app = QApplication(sys.argv)
    gui = KMonGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()