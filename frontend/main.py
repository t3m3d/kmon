import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QSplitter,
)
from PySide6.QtCore import Qt

from frontend.panels.vital_panel import VitalPanel
from frontend.core.backend_client import BackendClient
from frontend.ui.widgets.header import HeaderBar
from frontend.ui.widgets.footer import FooterBar
from frontend.panels.packet_list import PacketListPanel
from frontend.ui.styles import apply_app_style
from frontend.panels.packet_details import PacketDetailsPanel
from frontend.ui.widgets.crt_panel import CRTPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("K'mon - KryptonBytes Network Monitor")
        self.resize(1200, 700)

        # Central widget + layout
        central = QWidget(self)
        central_layout = QVBoxLayout(central)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        # Header
        self.header = HeaderBar(parent=self)
        central_layout.addWidget(self.header)

        # Splitter layout
        splitter = QSplitter(Qt.Horizontal, parent=self)
        splitter.setHandleWidth(2)

        self.packet_list = PacketListPanel(parent=self)
        self.vital_panel = VitalPanel(parent=self)
        self.packet_details = PacketDetailsPanel(parent=self)
        self.crt_panel = CRTPanel(parent=self)

        splitter.addWidget(self.packet_list)
        splitter.addWidget(self.vital_panel)
        splitter.addWidget(self.packet_details)
        splitter.addWidget(self.crt_panel)

        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)
        splitter.setStretchFactor(2, 2)
        splitter.setStretchFactor(3, 2)

        central_layout.addWidget(splitter)

        # Footer
        self.footer = FooterBar(parent=self)
        central_layout.addWidget(self.footer)

        self.setCentralWidget(central)

        # Backend
        self.backend = BackendClient()
        self.backend.packet_received.connect(self.on_packet_received)
        self.backend.stats_updated.connect(self.on_stats_updated)
        self.backend.interface_changed.connect(self.on_interface_changed)
        self.backend.status_changed.connect(self.on_status_changed)

        # Packet selection
        self.packet_list.packet_selected.connect(self.on_packet_selected)

        # Vital panel stats
        self.backend.stats_updated.connect(self.vital_panel.update_stats)

        self.backend.start()

        # Store system IP
        self.system_ip = "Unknown"

    def closeEvent(self, event):
        self.backend.stop()
        self.backend.wait(2000)
        super().closeEvent(event)

    # ----- Backend slots -----

    def on_packet_received(self, packet: dict):
        self.packet_list.add_packet(packet)

    def on_stats_updated(self, stats: dict):
        self.footer.update_stats(stats)

    def on_interface_changed(self, interface_name: str):
        self.header.set_interface_name(interface_name)
        self.system_ip = interface_name

    def on_status_changed(self, status: str):
        self.header.set_status(status)

    def on_packet_selected(self, packet: dict):
        self.packet_details.show_packet(packet, self.system_ip)


def main():
    app = QApplication(sys.argv)
    apply_app_style(app)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()