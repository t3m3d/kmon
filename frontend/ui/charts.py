from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt

from .styles import (
    BG_PANEL,
    BORDER,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    FONT_FAMILY_MAIN,
)


class ChartsPanel(QFrame):
    """
    Placeholder for future charts (bandwidth, protocol distribution, etc.)
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("ChartsPanel")
        self.setStyleSheet(
            f"""
            QFrame#ChartsPanel {{
                background-color: {BG_PANEL};
                border: 1px solid {BORDER};
                border-radius: 4px;
            }}
        """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Title
        title = QLabel("Charts (Coming Soon)")
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet(
            f"""
            color: {TEXT_PRIMARY};
            font-size: 14px;
            font-weight: 600;
            font-family: {FONT_FAMILY_MAIN};
        """
        )

        # Subtitle
        subtitle = QLabel("Bandwidth graphs, protocol distribution, and more.")
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(
            f"""
            color: {TEXT_SECONDARY};
            font-size: 11px;
            font-family: {FONT_FAMILY_MAIN};
        """
        )

        # Placeholder content
        placeholder = QLabel("📊 Chart rendering not implemented yet")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet(
            f"""
            color: {TEXT_SECONDARY};
            font-size: 12px;
            font-family: {FONT_FAMILY_MAIN};
        """
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
        layout.addWidget(placeholder)
        layout.addStretch()