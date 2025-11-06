from __future__ import annotations

import json
from pathlib import Path
from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QListWidget, QListWidgetItem
)


class TodoWindow(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle('Gestionnaire de tâches')

        self.store_path = Path.home() / '.ordo_todos.json'
        self.todos: List[dict] = []

        layout = QVBoxLayout(self)
        row = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText('Nouvelle tâche...')
        add_btn = QPushButton('[+ ]')
        add_btn.clicked.connect(self.add_todo)
        row.addWidget(self.input)
        row.addWidget(add_btn)
        layout.addLayout(row)

        self.list = QListWidget()
        layout.addWidget(self.list, 1)

        self.load()
        self.render()

        self.input.returnPressed.connect(self.add_todo)
        self.list.itemDoubleClicked.connect(self.toggle_complete)

    def load(self) -> None:
        if self.store_path.exists():
            try:
                self.todos = json.loads(self.store_path.read_text(encoding='utf-8'))
            except Exception:
                self.todos = []

    def save(self) -> None:
        try:
            self.store_path.write_text(json.dumps(self.todos, ensure_ascii=False, indent=2), encoding='utf-8')
        except Exception:
            pass

    def render(self) -> None:
        self.list.clear()
        for t in self.todos:
            txt = ('[x] ' if t.get('completed') else '[ ] ') + t.get('text', '')
            item = QListWidgetItem(txt)
            if t.get('completed'):
                item.setFlags(item.flags() | Qt.ItemIsSelectable)
            self.list.addItem(item)

    def add_todo(self) -> None:
        text = self.input.text().strip()
        if not text:
            return
        self.todos.append({'text': text, 'completed': False})
        self.save()
        self.input.clear()
        self.render()

    def toggle_complete(self, item: QListWidgetItem) -> None:
        idx = self.list.row(item)
        if 0 <= idx < len(self.todos):
            self.todos[idx]['completed'] = not self.todos[idx].get('completed')
            self.save()
            self.render()


