from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QFormLayout, QSizePolicy
from PySide6.QtCore import Qt
from frontend.ui.styles import (
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    FONT_FAMILY_MAIN,
)


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

        # Raw packet dump
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

        self.raw_view.setMinimumHeight(150)

        # Helper to add rows
        def add(label, value):
            lbl = QLabel(label)
            val = QLabel(str(value) if value else " ")

            lbl.setStyleSheet(f"color: {TEXT_PRIMARY}; font-family: {FONT_FAMILY_MAIN};")
            val.setStyleSheet(f"color: {TEXT_SECONDARY}; font-family: {FONT_FAMILY_MAIN};")

            lbl.setFixedHeight(22)
            val.setFixedHeight(22)

            self.form.addRow(lbl, val)

        # Use backend keys
        add("Source IP:", packet.get("src_ip", "Unknown"))
        add("Destination IP:", packet.get("dst_ip", "Unknown"))
        add("Protocol:", packet.get("protocol", "Unknown"))
        add("Length:", packet.get("length", "Unknown"))
        add("Info:", packet.get("info", ""))
        add("System IP:", system_ip)

        # Raw dump
        raw = packet.get("raw", "")
        self.raw_view.setPlainText(raw)

        self.update()