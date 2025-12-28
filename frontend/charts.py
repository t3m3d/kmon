from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer
import pyqtgraph as pg

class BandwidthChart(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Bandwidth (Mbps)")
        layout.addWidget(self.label)

        self.graph = pg.PlotWidget()
        layout.addWidget(self.graph)

        self.down_data = []
        self.up_data = []

        self.curve_down = self.graph.plot(pen='y')
        self.curve_up = self.graph.plot(pen='c')

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(500)

    def update_stats(self, stats):
        self.down_data.append(stats["mbps_down"])
        self.up_data.append(stats["mbps_up"])

        if len(self.down_data) > 100:
            self.down_data.pop(0)
            self.up_data.pop(0)

    def refresh(self):
        self.curve_down.setData(self.down_data)
        self.curve_up.setData(self.up_data)