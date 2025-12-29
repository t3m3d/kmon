from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QFrame,
    QTextEdit,
)
from PySide6.QtCore import Qt

from .styles import BG_PANEL, BORDER, TEXT_PRIMARY, TEXT_SECONDARY, FONT_FAMILY_MONO, FONT_FAMILY_MAIN


class PacketDetailsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAutoFillBackground(True)
        self.setStyleSheet(
            f"""
            QWidget {{
                background-color: {BG_PANEL};
            }}
        """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Card frame for details
        self.card = QFrame(self)
        self.card.setFrameShape(QFrame.StyledPanel)
        self.card.setStyleSheet(
            f"""
            QFrame {{
                background-color: {BG_PANEL};
                border: 1px solid {BORDER};
                border-radius: 4px;
            }}
        """
        )

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(8, 8, 8, 8)
        card_layout.setSpacing(6)

        title = QLabel("Packet Details")
        title.setStyleSheet(
            f"color: {TEXT_PRIMARY}; font-size: 12px; font-weight: 600; font-family: {FONT_FAMILY_MAIN};"
        )

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setFormAlignment(Qt.AlignTop)

        self.lbl_src = QLabel("-")
        self.lbl_dst = QLabel("-")
        self.lbl_proto = QLabel("-")
        self.lbl_len = QLabel("-")
        self.lbl_flags = QLabel("-")
        self.lbl_time = QLabel("-")

        for lbl in (self.lbl_src, self.lbl_dst, self.lbl_proto, self.lbl_len, self.lbl_flags, self.lbl_time):
            lbl.setStyleSheet(
                f"color: {TEXT_PRIMARY}; font-size: 11px; font-family: {FONT_FAMILY_MONO};"
            )

        def make_label(text: str) -> QLabel:
            lbl = QLabel(text)
            lbl.setStyleSheet(
                f"color: {TEXT_SECONDARY}; font-size: 11px; font-family: {FONT_FAMILY_MAIN};"
            )
            return lbl

        form.addRow(make_label("Source IP:"), self.lbl_src)
        form.addRow(make_label("Destination IP:"), self.lbl_dst)
        form.addRow(make_label("Protocol:"), self.lbl_proto)
        form.addRow(make_label("Length:"), self.lbl_len)
        form.addRow(make_label("Flags:"), self.lbl_flags)
        form.addRow(make_label("Timestamp:"), self.lbl_time)

        # Hex dump
        self.hex_label = QLabel("Hex Dump")
        self.hex_label.setStyleSheet(
            f"color: {TEXT_SECONDARY}; font-size: 11px; font-family: {FONT_FAMILY_MAIN};"
        )

        self.hex_view = QTextEdit(self)
        self.hex_view.setReadOnly(True)
        self.hex_view.setStyleSheet(
            f"""
            QTextEdit {{
                background-color: {BG_PANEL};
                border: 1px solid {BORDER};
                color: {TEXT_PRIMARY};
                font-family: {FONT_FAMILY_MONO};
                font-size: 10px;
            }}
        """
        )

        card_layout.addWidget(title)
        card_layout.addLayout(form)
        card_layout.addWidget(self.hex_label)
        card_layout.addWidget(self.hex_view, 1)

        layout.addWidget(self.card, 1)

    def show_packet(self, packet: dict):
        self.lbl_src.setText(packet.get("src_ip", "-"))
        self.lbl_dst.setText(packet.get("dst_ip", "-"))
        self.lbl_proto.setText(packet.get("protocol", "-"))
        self.lbl_len.setText(str(packet.get("length", "-")))
        self.lbl_flags.setText(packet.get("flags", "-"))
        self.lbl_time.setText(packet.get("timestamp", "-"))
        self.hex_view.setPlainText(packet.get("hex_dump", ""))