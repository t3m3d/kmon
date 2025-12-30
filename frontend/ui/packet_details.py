from cProfile import label
from operator import add
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QFormLayout
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSizePolicy
from ui.styles import TEXT_PRIMARY, TEXT_SECONDARY, FONT_FAMILY_MAIN


class PacketDetailsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Title
        self.title = QLabel("Packet Details")
        self.title.setStyleSheet(f"""
            color: {TEXT_PRIMARY};
            font-family: {FONT_FAMILY_MAIN};
            font-size: 18px;
            font-weight: bold;
        """)
        layout.addWidget(self.title)

        # Form layout for key/value fields
        self.form = QFormLayout()
        self.form.setLabelAlignment(Qt.AlignLeft)
        layout.addLayout(self.form)
        self.setMinimumWidth(300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Text area for raw packet dump
        self.raw_view = QTextEdit()
        self.raw_view.setReadOnly(True)
        self.raw_view.setStyleSheet(f"""
            background-color: #1e1e1e;
            color: {TEXT_SECONDARY};
            font-family: {FONT_FAMILY_MAIN};
            font-size: 13px;
        """)
        layout.addWidget(self.raw_view)

    def show_packet(self, packet: dict, system_ip: str):
        # Clear old rows
        while self.form.rowCount():
            self.form.removeRow(0)

        # Helper to add rows
        def add(label, value):
            lbl = QLabel(label)
            val = QLabel(str(value))
            lbl.setStyleSheet(f"color: {TEXT_PRIMARY}; font-family: {FONT_FAMILY_MAIN};")
            val.setStyleSheet(f"color: {TEXT_SECONDARY}; font-family: {FONT_FAMILY_MAIN};")
            self.form.addRow(lbl, val)
        # Add packet details        
        add("Source IP:", packet.get("src_ip", "Unknown"))
        add("Destination IP:", packet.get("dst_ip", "Unknown"))
        add("Protocol:", packet.get("protocol", "Unknown"))
        add("Length:", packet.get("length", "Unknown"))
        add("System IP:", system_ip)
        # Raw dump
        raw = packet.get("raw", "")
        self.raw_view.setPlainText(raw)
        self.form.update()
        self.raw_view.update()
        self.update()