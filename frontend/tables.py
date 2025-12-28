from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

class PacketTable(QTableWidget):
    def __init__(self):
        super().__init__(0, 6)
        self.setHorizontalHeaderLabels([
            "Time", "Src IP", "Dst IP", "Proto", "Len", "Src→Dst"
        ])

    def add_packet(self, pkt):
        row = self.rowCount()
        self.insertRow(row)

        self.setItem(row, 0, QTableWidgetItem(str(pkt["timestamp"])))
        self.setItem(row, 1, QTableWidgetItem(pkt["src_ip"]))
        self.setItem(row, 2, QTableWidgetItem(pkt["dst_ip"]))
        self.setItem(row, 3, QTableWidgetItem(pkt["protocol"]))
        self.setItem(row, 4, QTableWidgetItem(str(pkt["length"])))
        self.setItem(row, 5, QTableWidgetItem(f"{pkt['src_port']} → {pkt['dst_port']}"))