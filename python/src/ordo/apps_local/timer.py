from __future__ import annotations

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout


class TimerWindow(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle('Minuteur')

        self.time_left = 25 * 60
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.tick)

        layout = QVBoxLayout(self)
        self.display = QLabel(self.format_time(self.time_left))
        self.display.setStyleSheet('font-size: 36px; qproperty-alignment: AlignCenter;')
        layout.addWidget(self.display)

        row = QHBoxLayout()
        self.start_btn = QPushButton('[START]')
        self.reset_btn = QPushButton('[RESET]')
        row.addWidget(self.start_btn)
        row.addWidget(self.reset_btn)
        layout.addLayout(row)

        self.start_btn.clicked.connect(self.toggle)
        self.reset_btn.clicked.connect(self.reset)

    def format_time(self, s: int) -> str:
        m, s = divmod(s, 60)
        return f"{m:02d}:{s:02d}"

    def tick(self) -> None:
        self.time_left -= 1
        self.display.setText(self.format_time(self.time_left))
        if self.time_left <= 0:
            self.timer.stop()
            self.start_btn.setText('[START]')

    def toggle(self) -> None:
        if self.timer.isActive():
            self.timer.stop()
            self.start_btn.setText('[START]')
        else:
            self.timer.start()
            self.start_btn.setText('[PAUSE]')

    def reset(self) -> None:
        self.timer.stop()
        self.time_left = 25 * 60
        self.display.setText(self.format_time(self.time_left))
        self.start_btn.setText('[START]')


