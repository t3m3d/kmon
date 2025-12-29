from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

BG_DARK = "#1E1E1E"
BG_PANEL = "#202124"
TEXT_PRIMARY = "#E0E0E0"
TEXT_SECONDARY = "#A0A0A0"
BORDER = "#2A2A2A"

TCP_COLOR = "#4A90E2"
UDP_COLOR = "#9B59B6"
ICMP_COLOR = "#F1C40F"
ARP_COLOR = "#1ABC9C"
ERROR_COLOR = "#E74C3C"

FONT_FAMILY_MONO = "HeavyData Nerd Font"
FONT_FAMILY_MAIN = "HeavyData Nerd Font"


def apply_app_style(app: QApplication):
    """
    Basic dark style that still respects platform hints.
    You can later enhance this to fully follow system theme.
    """
    palette = QPalette()

    palette.setColor(QPalette.Window, QColor(BG_DARK))
    palette.setColor(QPalette.WindowText, QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.Base, QColor(BG_PANEL))
    palette.setColor(QPalette.AlternateBase, QColor(BG_DARK))
    palette.setColor(QPalette.Text, QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.Button, QColor(BG_PANEL))
    palette.setColor(QPalette.ButtonText, QColor(TEXT_PRIMARY))
    palette.setColor(QPalette.Highlight, QColor(TCP_COLOR))
    palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))

    app.setPalette(palette)

    # modern style hints
    app.setStyle("Fusion")