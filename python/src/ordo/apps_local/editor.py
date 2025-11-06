from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel


class EditorWindow(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle('Éditeur')

        self.store_path = Path.home() / '.ordo_editor.txt'

        layout = QVBoxLayout(self)
        self.text = QTextEdit()
        self.status = QLabel('└─ Sauvegarde automatique activée')
        layout.addWidget(self.text, 1)
        layout.addWidget(self.status)

        if self.store_path.exists():
            try:
                self.text.setText(self.store_path.read_text(encoding='utf-8'))
            except Exception:
                pass

        self.debounce = QTimer(self)
        self.debounce.setInterval(1000)
        self.debounce.setSingleShot(True)
        self.debounce.timeout.connect(self.save)
        self.text.textChanged.connect(self.on_change)

    def on_change(self) -> None:
        self.status.setText('└─ Sauvegarde en cours...')
        self.debounce.start()

    def save(self) -> None:
        try:
            self.store_path.write_text(self.text.toPlainText(), encoding='utf-8')
            self.status.setText('└─ Sauvegardé')
        except Exception:
            self.status.setText('└─ Erreur de sauvegarde')


