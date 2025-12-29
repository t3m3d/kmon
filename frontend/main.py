import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
)
from PySide6.QtCore import Qt

from core.backend_client import BackendClient
from ui.header import HeaderBar
from ui.footer import FooterBar
from ui.packet_list import PacketListPanel
from ui.packet_details import PacketDetailsPanel
from ui.styles import apply_app_style


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("kmon - KryptonBytes Network Monitor")
        self.resize(1200, 700)

        # Central widget and layout
        central = QWidget(self)
        central_layout = QVBoxLayout(central)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        # Header
        self.header = HeaderBar(parent=self)
        central_layout.addWidget(self.header)

        # Splitter: left = packet list, right = packet details
        splitter = QSplitter(Qt.Horizontal, parent=self)
        splitter.setHandleWidth(2)

        self.packet_list = PacketListPanel(parent=self)
        self.packet_details = PacketDetailsPanel(parent=self)

        splitter.addWidget(self.packet_list)
        splitter.addWidget(self.packet_details)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)

        central_layout.addWidget(splitter)

        # Footer
        self.footer = FooterBar(parent=self)
        central_layout.addWidget(self.footer)

        self.setCentralWidget(central)

        # Backend client thread
        self.backend = BackendClient()
        self.backend.packet_received.connect(self.on_packet_received)
        self.backend.stats_updated.connect(self.on_stats_updated)
        self.backend.interface_changed.connect(self.on_interface_changed)
        self.backend.status_changed.connect(self.on_status_changed)

        self.packet_list.packet_selected.connect(self.on_packet_selected)

        self.backend.start()

    def closeEvent(self, event):
        self.backend.stop()
        self.backend.wait(2000)
        super().closeEvent(event)

    # --- Slots called from backend ---

    def on_packet_received(self, packet: dict):
        self.packet_list.add_packet(packet)

    def on_stats_updated(self, stats: dict):
        self.footer.update_stats(stats)

    def on_interface_changed(self, interface_name: str):
        self.header.set_interface_name(interface_name)

    def on_status_changed(self, status: str):
        # status: "capturing" | "stopped"
        self.header.set_status(status)

    # --- Slot called from packet list ---

    def on_packet_selected(self, packet: dict):
        self.packet_details.show_packet(packet)


def main():
    app = QApplication(sys.argv)
    apply_app_style(app)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()