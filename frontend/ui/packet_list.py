from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

from .styles import (
    BG_PANEL,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TCP_COLOR,
    UDP_COLOR,
    ICMP_COLOR,
    ARP_COLOR,
    ERROR_COLOR,
    FONT_FAMILY_MONO,
)


class PacketListPanel(QWidget):
    packet_selected = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.table = QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Time", "Source", "Destination", "Proto", "Len", "Info"]
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.table.setStyleSheet(
            f"""
            QTableWidget {{
                background-color: {BG_PANEL};
                color: {TEXT_PRIMARY};
                gridline-color: {BG_PANEL};
                font-family: {FONT_FAMILY_MONO};
                font-size: 11px;
            }}
            QHeaderView::section {{
                background-color: {BG_PANEL};
                color: {TEXT_SECONDARY};
                border: none;
                font-weight: 500;
            }}
            QTableWidget::item:selected {{
                background-color: #333333;
            }}
        """
        )

        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)

        self.table.itemSelectionChanged.connect(self._on_selection_changed)

        layout.addWidget(self.table)

        self._packets = []  # store full packet dicts by row index

    def add_packet(self, packet: dict):
        row = self.table.rowCount()
        self.table.insertRow(row)

        self._packets.append(packet)

        # Map fields
        time_val = packet.get("timestamp", "")
        src = packet.get("src_ip", "")
        dst = packet.get("dst_ip", "")
        proto = packet.get("protocol", "")
        length = str(packet.get("length", ""))
        info = packet.get("info", "")

        values = [time_val, src, dst, proto, length, info]

        for col, val in enumerate(values):
            item = QTableWidgetItem(val)
            item.setTextAlignment(Qt.AlignVCenter | (Qt.AlignLeft if col != 4 else Qt.AlignRight))
            self.table.setItem(row, col, item)

        # Color accent based on protocol
        color = self._color_for_protocol(proto)
        for col in range(self.table.columnCount()):
            item = self.table.item(row, col)
            if item:
                item.setForeground(color)

        # Auto-scroll to bottom
        self.table.scrollToBottom()

    def _color_for_protocol(self, proto: str):
        p = proto.upper()
        if p == "TCP":
            from PySide6.QtGui import QColor

            return QColor(TCP_COLOR)
        if p == "UDP":
            from PySide6.QtGui import QColor

            return QColor(UDP_COLOR)
        if p == "ICMP":
            from PySide6.QtGui import QColor

            return QColor(ICMP_COLOR)
        if p == "ARP":
            from PySide6.QtGui import QColor

            return QColor(ARP_COLOR)
        if p == "ERROR":
            from PySide6.QtGui import QColor

            return QColor(ERROR_COLOR)
        from PySide6.QtGui import QColor

        return QColor(TEXT_PRIMARY)

    def _on_selection_changed(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            return

        row_index = selected_rows[0].row()
        if 0 <= row_index < len(self._packets):
            packet = self._packets[row_index]
            self.packet_selected.emit(packet)