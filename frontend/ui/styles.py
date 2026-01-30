from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget

# Color Palette
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

CRT_GLOW = "#00FF99"
HEADER_BG = "#1A1A1A"
FOOTER_BG = "#1A1A1A"

# Font Definitions
FONT_FAMILY_MONO = "HeavyData Nerd Font"
FONT_FAMILY_MAIN = "HeavyData Nerd Font"

FONT_DEFAULT = QFont(FONT_FAMILY_MAIN, 10)
FONT_HEADER = QFont(FONT_FAMILY_MAIN, 12, QFont.Bold)
FONT_FOOTER = QFont(FONT_FAMILY_MAIN, 9)
FONT_CRT = QFont("Pixel Emulator", 11)

#  Application-wide Palette
def apply_app_style(app: QApplication):
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
    app.setStyle("Fusion")

#  Widget Styling Helpers
def apply_crt_theme(widget: QWidget):
    widget.setStyleSheet(f"""
        background-color: {BG_DARK};
        color: {CRT_GLOW};
        font-family: {FONT_CRT.family()};
        font-size: {FONT_CRT.pointSize()}pt;
        border: 1px solid {TCP_COLOR};
    """)

def apply_header_style(widget: QWidget):
    widget.setStyleSheet(f"""
        background-color: {HEADER_BG};
        color: {TCP_COLOR};
        font-family: {FONT_HEADER.family()};
        font-size: {FONT_HEADER.pointSize()}pt;
    """)

def apply_footer_style(widget: QWidget):
    widget.setStyleSheet(f"""
        background-color: {FOOTER_BG};
        color: {TEXT_SECONDARY};
        font-family: {FONT_FOOTER.family()};
        font-size: {FONT_FOOTER.pointSize()}pt;
    """)

def apply_label_style(label: QWidget, primary=True):
    color = TEXT_PRIMARY if primary else TEXT_SECONDARY
    label.setStyleSheet(f"""
        color: {color};
        font-family: {FONT_FAMILY_MAIN};
        font-size: 10pt;
    """)