from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QFrame
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt

from ..styles import TEXT_PRIMARY, TEXT_SECONDARY, BG_PANEL, BORDER, FONT_FAMILY_MAIN

class StatusDot(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._color = QColor("#27AE60")  # default green
        self.setFixedSize(12, 12)

    def set_color(self, color: str):
        self._color = QColor(color)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setBrush(self._color)
        painter.setPen(Qt.NoPen)
        radius = min(self.width(), self.height()) // 2
        painter.drawEllipse(
            self.width() // 2 - radius,
            self.height() // 2 - radius,
            radius * 2,
            radius * 2,
        )

class HeaderBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("HeaderBar")
        self.setStyleSheet(
            f"""
            QFrame#HeaderBar {{
                background-color: {BG_PANEL};
                border-bottom: 1px solid {BORDER};
            }}
        """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 4, 10, 4)
        layout.setSpacing(10)

        # Left: Title
        self.title_label = QLabel("KMON")
        self.title_label.setStyleSheet(
            f"color: {TEXT_PRIMARY}; font-size: 16px; font-weight: 600; font-family: {FONT_FAMILY_MAIN};"
        )

        # Center: status + interface
        center_widget = QWidget(self)
        center_layout = QHBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(6)

        self.status_dot = StatusDot(center_widget)
        self.status_label = QLabel("Capturing on:")
        self.status_label.setStyleSheet(
            f"color: {TEXT_SECONDARY}; font-size: 11px; font-family: {FONT_FAMILY_MAIN};"
        )
        self.interface_label = QLabel("Unknown")
        self.interface_label.setStyleSheet(
            f"color: {TEXT_PRIMARY}; font-size: 11px; font-family: {FONT_FAMILY_MAIN};"
        )

        center_layout.addWidget(self.status_dot, 0, Qt.AlignVCenter)
        center_layout.addWidget(self.status_label, 0, Qt.AlignVCenter)
        center_layout.addWidget(self.interface_label, 0, Qt.AlignVCenter)
        center_layout.addStretch()

        # Right: version
        self.version_label = QLabel("v0.1.0")
        self.version_label.setStyleSheet(
            f"color: {TEXT_SECONDARY}; font-size: 11px; font-family: {FONT_FAMILY_MAIN};"
        )

        layout.addWidget(self.title_label)
        layout.addWidget(center_widget, 1)
        layout.addWidget(self.version_label, 0, Qt.AlignRight)

    def set_interface_name(self, name: str):
        self.interface_label.setText(name)

    def set_status(self, status: str):
        # status: "capturing" | "stopped" | anything else
        if status == "capturing":
            self.status_dot.set_color("#27AE60")  # green
            self.status_label.setText("Capturing on:")
        else:
            self.status_dot.set_color("#E74C3C")  # red
            self.status_label.setText("Stopped on:")