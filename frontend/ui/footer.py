from PySide6.QtWidgets import QFrame, QLabel, QHBoxLayout
from PySide6.QtCore import Qt

from .styles import BG_PANEL, BORDER, TEXT_SECONDARY, FONT_FAMILY_MAIN


class FooterBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("FooterBar")
        self.setStyleSheet(
            f"""
            QFrame#FooterBar {{
                background-color: {BG_PANEL};
                border-top: 1px solid {BORDER};
            }}
        """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 2, 10, 2)
        layout.setSpacing(20)

        self.pps_label = QLabel("Packets/sec: 0")
        self.total_label = QLabel("Total: 0")
        self.dropped_label = QLabel("Dropped: 0")

        for lbl in (self.pps_label, self.total_label, self.dropped_label):
            lbl.setStyleSheet(
                f"color: {TEXT_SECONDARY}; font-size: 10px; font-family: {FONT_FAMILY_MAIN};"
            )

        layout.addWidget(self.pps_label)
        layout.addWidget(self.total_label)
        layout.addWidget(self.dropped_label)
        layout.addStretch()

    def update_stats(self, stats: dict):
        pps = stats.get("packets_per_sec", 0)
        total = stats.get("total_packets", 0)
        dropped = stats.get("dropped_packets", 0)

        self.pps_label.setText(f"Packets/sec: {pps}")
        self.total_label.setText(f"Total: {total}")
        self.dropped_label.setText(f"Dropped: {dropped}")