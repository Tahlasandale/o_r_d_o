from __future__ import annotations

import importlib
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Dict, Optional

import yaml
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QKeySequence, QAction, QIcon, QPixmap, QPainter, QFont, QFontMetrics, QShortcut
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QMdiArea, QMdiSubWindow, QStatusBar, QMenu, QStyle
)
from PySide6.QtWebEngineWidgets import QWebEngineView


@dataclass(frozen=True)
class AppEntry:
    """Configuration d'une application (immutable pour meilleures performances)"""
    id: str
    title: str
    icon: str
    type: str  # 'web' | 'local'
    url: Optional[str] = None
    class_path: Optional[str] = None
    width: int = 600
    height: int = 400
    x: int = 100
    y: int = 100


@lru_cache(maxsize=1)
def load_registry() -> Dict[str, AppEntry]:
    """Charge le registre des applications (avec cache)"""
    registry: Dict[str, AppEntry] = {}
    
    try:
        # Recherche du fichier apps.yaml
        base_path = Path(__file__).resolve().parents[2]
        cfg_path = base_path / 'apps.yaml'
        
        if not cfg_path.exists():
            cfg_path = base_path.parent / 'apps.yaml'
        
        if not cfg_path.exists():
            print(f"Avertissement: Fichier apps.yaml introuvable dans {base_path}")
            return registry
            
        data = yaml.safe_load(cfg_path.read_text(encoding='utf-8'))
        
        for app in data.get('apps', []):
            try:
                entry = AppEntry(
                    id=app['id'], 
                    title=app['title'], 
                    icon=app.get('icon', '📄'),
                    type=app['type'], 
                    url=app.get('url'), 
                    class_path=app.get('class'),
                    width=app.get('width', 600), 
                    height=app.get('height', 400),
                    x=app.get('x', 100), 
                    y=app.get('y', 100),
                )
                registry[entry.id] = entry
            except KeyError as e:
                print(f"Configuration invalide pour '{app.get('id', 'inconnu')}': champ manquant {e}")
                
    except FileNotFoundError:
        print("Fichier apps.yaml introuvable")
    except yaml.YAMLError as e:
        print(f"Erreur de parsing YAML: {e}")
    except Exception as e:
        print(f"Erreur lors du chargement du registre: {e}")
    
    return registry


class OrdoMainWindow(QMainWindow):
    """Fenêtre principale de l'application Ordo Desktop"""
    
    # Constantes de style (évite les chaînes magiques)
    BACKGROUND_COLOR = "#8f8f8f"
    BORDER_COLOR = "#000000"
    BORDER_WIDTH = 3
    MENU_WIDTH = 300
    MENU_HEIGHT = 400
    
    # Stylesheet centralisé (chargé une seule fois)
    STYLESHEET = """
        QMainWindow, QWidget {
            background-color: #8f8f8f;
        }
        
        QStatusBar {
            background-color: #8f8f8f;
            border: 3px solid #000000;
            height: 46px;
            padding: 0;
            spacing: 0;
            margin: 0;
        }
        
        QStatusBar::item {
            border: none;
            padding: 0;
            margin: 0 2px;
            background: transparent;
        }
        
        QPushButton#startButton {
            background-color: #000000;
            color: #ffffff;
            border: 3px solid #000000;
            padding: 8px 20px 8px 40px;
            min-width: 150px;
            min-height: 34px;
            max-height: 38px;
            text-align: left;
            font-family: 'Courier New', 'Consolas', 'Monaco', monospace;
            font-size: 11.5pt;
            font-weight: bold;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            margin: 4px 0 4px 6px;
        }
        
        QPushButton#startButton:hover {
            background-color: #333333;
            border-color: #333333;
        }
        
        QPushButton#startButton:pressed {
            background-color: #000000;
            border-color: #ffffff;
            color: #ffffff;
        }
        
        QMenu {
            background-color: #ffffff;
            border: 3px solid #000000;
            padding: 8px 0;
            min-width: 280px;
            max-width: 320px;
            max-height: 600px;
            font-family: 'Courier New', 'Consolas', 'Monaco', monospace;
            font-size: 11px;
            font-weight: normal;
            margin: 0;
        }
        
        QMenu::item {
            padding: 10px 25px 10px 35px;
            background: transparent;
            min-height: 28px;
            border: none;
            margin: 0;
            text-align: left;
            color: #000000;
            font-family: 'Courier New', 'Consolas', 'Monaco', monospace;
            font-size: 11px;
            font-weight: normal;
            letter-spacing: 0.1px;
        }
        
        QMenu::item:selected {
            background-color: #000000;
            color: #ffffff;
        }
        
        QMenu::icon {
            left: 10px;
            width: 18px;
            height: 18px;
        }
        
        QMenu::separator {
            height: 3px;
            background: #000000;
            margin: 8px 0;
        }
        
        QMenu::item#shutdownItem {
            background: #000000;
            color: #ffffff;
            padding: 12px 25px 12px 35px;
            margin: 8px 0 0 0;
            font-weight: 800;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        
        QMenu::item#shutdownItem:selected {
            background: #333333;
            color: #ffffff;
        }
        
        QMdiArea {
            background: #8f8f8f;
            border: none;
        }
        
        QMdiSubWindow {
            background: #ffffff;
            border: 3px solid #000000;
            border-radius: 0;
        }
        
        QMdiSubWindow::title {
            background: #000000;
            color: #ffffff;
            padding: 8px;
            text-align: left;
            font-family: 'Courier New', 'Consolas', 'Monaco', monospace;
            font-weight: bold;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        QMdiSubWindow::close-button, QMdiSubWindow::max-button {
            background: #000000;
            color: #ffffff;
            border: 2px solid #000000;
            width: 20px;
            height: 20px;
            margin: 2px;
            padding: 0;
            subcontrol-origin: margin;
            subcontrol-position: right center;
            font-weight: bold;
        }
        
        QMdiSubWindow::close-button:hover, QMdiSubWindow::max-button:hover {
            background: #333333;
            border-color: #333333;
        }
        
        QMdiSubWindow::close-button:pressed, QMdiSubWindow::max-button:pressed {
            background: #000000;
            border-color: #ffffff;
        }
    """
    
    def __init__(self) -> None:
        super().__init__()
        self._init_window()
        self._init_ui()
        self._init_shortcuts()
        
    def _init_window(self) -> None:
        """Initialize window properties"""
        self.setWindowTitle('Ordo Desktop')
        
        # Mode kiosk (plein écran sans bordure)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.showFullScreen()
        
        self.setStyleSheet(self.STYLESHEET)
        
        # Configuration de la police
        font = self.font()
        font.setFamily("'Courier New', 'Consolas', 'Monaco', monospace")
        font.setPointSize(10)
        font.setBold(True)
        self.setFont(font)
        
    def _init_shortcuts(self) -> None:
        """Initialize keyboard shortcuts"""
        # Raccourci Alt pour le menu Démarrer
        alt_action = QAction('Show Start Menu', self)
        alt_action.setShortcut(QKeySequence('Alt'))
        alt_action.triggered.connect(self.toggle_start_menu)
        self.addAction(alt_action)
        
        # Raccourci Échap pour quitter le mode plein écran
        esc_action = QAction('Toggle Fullscreen', self)
        esc_action.setShortcut(QKeySequence('Escape'))
        esc_action.triggered.connect(self.toggle_fullscreen)
        self.addAction(esc_action)
        
        # Gestion spécifique de Ctrl+W pour éviter les conflits
        self.shortcut_close = QShortcut(QKeySequence('Ctrl+W'), self)
        self.shortcut_close.activated.connect(self.close)
        
    def _init_ui(self) -> None:
        """Initialize user interface components"""
        self.registry = load_registry()
        self.start_menu_visible = False
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Zone MDI
        self.mdi = QMdiArea()
        self.mdi.setViewMode(QMdiArea.SubWindowView)
        layout.addWidget(self.mdi, 1)
        
        # Barre des tâches
        self._init_taskbar()
        
        # Menu démarrer
        self._create_start_menu()
        
    def _init_taskbar(self) -> None:
        """Initialize taskbar"""
        self.taskbar = QStatusBar()
        self.setStatusBar(self.taskbar)
        self.taskbar.setSizeGripEnabled(False)
        
        taskbar_container = QWidget()
        taskbar_layout = QHBoxLayout(taskbar_container)
        taskbar_layout.setContentsMargins(2, 2, 2, 2)
        taskbar_layout.setSpacing(2)
        
        # Bouton Démarrer
        self.start_button = QPushButton("Démarrer")
        self.start_button.setObjectName("startButton")
        self.start_button.setFixedSize(100, 24)
        self.start_button.clicked.connect(self.toggle_start_menu)
        
        taskbar_layout.addWidget(self.start_button)
        taskbar_layout.addStretch()
        
        self.taskbar.addPermanentWidget(taskbar_container, 1)
        
    def toggle_start_menu(self) -> None:
        """Toggle start menu visibility"""
        if self.start_menu_visible:
            self.start_menu.hide()
        else:
            self._update_menu_position()
            self.start_menu.show()
            self.start_menu_visible = True
            
    def _on_menu_hidden(self) -> None:
        """Handle menu hide event"""
        self.start_menu_visible = False
        
    def toggle_fullscreen(self) -> None:
        """Toggle between fullscreen and windowed mode"""
        if self.isFullScreen():
            self.showNormal()
            self.setWindowFlags(self.windowFlags() & ~Qt.FramelessWindowHint)
            self.show()
        else:
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
            self.showFullScreen()
        
    def _update_menu_position(self) -> None:
        """Update start menu position"""
        screen = self.screen()
        screen_rect = screen.availableGeometry()
        
        taskbar_height = self.statusBar().height()
        x = screen_rect.left()
        y = screen_rect.bottom() - self.MENU_HEIGHT - taskbar_height
        
        # Ajustement si le menu est trop grand
        if y < screen_rect.top():
            menu_height = screen_rect.height() - taskbar_height
            y = screen_rect.top()
        else:
            menu_height = self.MENU_HEIGHT
            
        self.start_menu.setGeometry(x, y, self.MENU_WIDTH, menu_height)
        
    def open_app(self, app_id: str) -> None:
        """Open an application by ID"""
        app = self.registry.get(app_id)
        if not app:
            print(f"Application '{app_id}' introuvable")
            return
        
        # Vérifier si déjà ouvert
        if self._activate_existing_window(app.title):
            return
        
        # Créer le widget
        widget = self._create_app_widget(app)
        if not widget:
            return
        
        # Créer la sous-fenêtre
        self._create_subwindow(widget, app)
        
    def _activate_existing_window(self, title: str) -> bool:
        """Activate window if already open"""
        for sub in self.mdi.subWindowList():
            if sub.windowTitle() == title:
                self.mdi.setActiveSubWindow(sub)
                if sub.isMinimized():
                    sub.showNormal()
                return True
        return False
        
    def _create_app_widget(self, app: AppEntry) -> Optional[QWidget]:
        """Create widget for application"""
        try:
            if app.type == 'web':
                return self._create_web_widget(app)
            elif app.type == 'local':
                return self._create_local_widget(app)
            else:
                print(f"Type d'application non supporté: {app.type}")
                return None
        except Exception as e:
            print(f"Erreur création widget pour '{app.id}': {e}")
            return None
            
    def _create_web_widget(self, app: AppEntry) -> Optional[QWebEngineView]:
        """Create web view widget"""
        if not app.url:
            print(f"URL manquante pour '{app.id}'")
            return None
            
        view = QWebEngineView()
        view.setUrl(QUrl(app.url))
        return view
        
    def _create_local_widget(self, app: AppEntry) -> Optional[QWidget]:
        """Create local application widget"""
        if not app.class_path:
            print(f"Chemin de classe manquant pour '{app.id}'")
            return None
            
        try:
            module_path, class_name = app.class_path.rsplit('.', 1)
            module = importlib.import_module(module_path)
            widget_class = getattr(module, class_name)
            return widget_class()
        except (ImportError, AttributeError, ValueError) as e:
            print(f"Erreur chargement classe '{app.class_path}': {e}")
            return None
            
    def _create_subwindow(self, widget: QWidget, app: AppEntry) -> None:
        """Create MDI subwindow for widget"""
        try:
            sub = QMdiSubWindow()
            sub.setWidget(widget)
            sub.setWindowTitle(app.title)
            sub.resize(app.width, app.height)
            self.mdi.addSubWindow(sub)
            sub.move(app.x, app.y)
            sub.show()
        except Exception as e:
            print(f"Erreur affichage application '{app.id}': {e}")
            
    def _create_start_menu(self) -> None:
        """Create start menu with application list"""
        self.start_menu = QMenu(self)
        self.start_menu.setObjectName("startMenu")
        
        # Désactiver la fermeture automatique du menu
        self.start_menu.setWindowFlags(self.start_menu.windowFlags() | Qt.Popup | Qt.NoDropShadowWindowHint)
        self.start_menu.aboutToHide.connect(self._on_menu_hidden)
        
        # Ajouter les applications triées
        for app_id, app in sorted(self.registry.items(), key=lambda x: x[1].title.lower()):
            action = QAction(app.title, self)
            action.setData(app_id)
            action.triggered.connect(lambda checked=False, a=app_id: self.open_app(a))
            
            # Ajouter l'icône
            icon = self._create_app_icon(app)
            if icon:
                action.setIcon(icon)
                
            self.start_menu.addAction(action)
        
        # Bouton d'arrêt
        self.start_menu.addSeparator()
        shutdown_action = QAction("Arrêter...", self)
        shutdown_action.triggered.connect(self.close)
        shutdown_action.setObjectName("shutdownItem")
        self.start_menu.addAction(shutdown_action)
        
        self.start_menu.setMinimumWidth(250)
        self.start_menu.setMaximumHeight(500)
        
    def _create_app_icon(self, app: AppEntry) -> Optional[QIcon]:
        """Create icon for application"""
        if not app.icon or not app.icon.strip():
            return self.style().standardIcon(QStyle.SP_ComputerIcon)
            
        # Essayer de créer une icône emoji
        if len(app.icon.strip()) <= 3:
            return self._create_emoji_icon(app.icon)
        
        # Essayer de charger depuis un fichier
        icon_path = Path(__file__).parent.parent.parent / 'apps' / f'{app.id}.png'
        if icon_path.exists():
            return QIcon(str(icon_path))
            
        return self.style().standardIcon(QStyle.SP_ComputerIcon)
        
    def _create_emoji_icon(self, emoji: str) -> Optional[QIcon]:
        """Create icon from emoji"""
        try:
            pixmap = QPixmap(16, 16)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            
            # Essayer différentes polices emoji
            for font_family in ["Segoe UI Emoji", "Segoe UI Symbol", "Arial"]:
                font = QFont(font_family, 12)
                painter.setFont(font)
                fm = QFontMetrics(font)
                
                if fm.inFont(emoji[0]):
                    # Centrer l'emoji
                    text_width = fm.horizontalAdvance(emoji)
                    text_height = fm.height()
                    x = (16 - text_width) // 2
                    y = (16 - text_height) // 2 + fm.ascent()
                    
                    painter.drawText(x, y, emoji)
                    painter.end()
                    return QIcon(pixmap)
                    
            painter.end()
        except Exception as e:
            print(f"Erreur création icône emoji: {e}")
            
        return None