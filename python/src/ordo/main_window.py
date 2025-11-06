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
    """Charge le registre des applications (avec cache)
    
    Les chemins des applications sont résolus dynamiquement par rapport à l'emplacement du projet.
    """
    registry: Dict[str, AppEntry] = {}
    
    try:
        # Chemin de base du projet (dossier parent du dossier python)
        base_path = Path(__file__).resolve().parents[2]
        project_root = base_path.parent  # Dossier parent de python/
        cfg_path = base_path / 'apps.yaml'
        
        if not cfg_path.exists():
            cfg_path = project_root / 'apps.yaml'
        
        if not cfg_path.exists():
            print(f"Avertissement: Fichier apps.yaml introuvable dans {base_path}")
            return registry
            
        data = yaml.safe_load(cfg_path.read_text(encoding='utf-8'))
        
        for app in data.get('apps', []):
            try:
                # Traitement des URLs
                url = app.get('url')
                if url and url.startswith('file://'):
                    # Si c'est un chemin de fichier local, on le résout par rapport à la racine du projet
                    rel_path = url.replace('file://', '')
                    # Nettoyer le chemin (supprimer les / en début si nécessaire)
                    rel_path = rel_path.lstrip('/')
                    # Construire le chemin absolu
                    abs_path = (project_root / rel_path).resolve()
                    # Vérifier que le fichier existe
                    if not abs_path.exists():
                        print(f"Avertissement: Fichier introuvable: {abs_path}")
                        continue
                    # Utiliser le chemin absolu avec le préfixe file://
                    url = f'file:///{abs_path}'.replace('\\', '/')
                
                entry = AppEntry(
                    id=app['id'], 
                    title=app['title'], 
                    icon=app.get('icon', '📄'),
                    type=app['type'], 
                    url=url, 
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
    
    # Constantes de style (noir et blanc uniquement)
    BACKGROUND_COLOR = "#ffffff"  # Blanc pur
    BORDER_COLOR = "#000000"     # Noir pur
    BORDER_WIDTH = 1             # Bordure plus fine
    MENU_WIDTH = 300
    MENU_HEIGHT = 400
    
    # Stylesheet centralisé (noir et blanc uniquement)
    STYLESHEET = """
        QMainWindow, QWidget, QMainWindow > QWidget {
            background-color: #ffffff !important;
        }
        
        QStatusBar {
            background-color: #ffffff;
            border: 1px solid #000000;
            height: 30px;
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
            border: 1px solid #000000;
            padding: 4px 10px 4px 20px;
            min-width: 120px;
            min-height: 24px;
            max-height: 28px;
            text-align: left;
            font-family: 'Courier New', 'Consolas', 'Monaco', monospace;
            font-size: 10pt;
            font-weight: bold;
            text-transform: uppercase;
            margin: 2px 0 2px 4px;
        }
        
        QPushButton#startButton:hover {
            background-color: #000000;
            border-color: #000000;
        }
        
        QPushButton#startButton:pressed {
            background-color: #000000;
            border-color: #000000;
            color: #ffffff;
        }
        
        QMenu {
            background-color: #ffffff;
            border: 1px solid #000000;
            padding: 4px 0;
            min-width: 250px;
            max-width: 300px;
            max-height: 500px;
            font-family: 'Courier New', 'Consolas', 'Monaco', monospace;
            font-size: 10px;
            font-weight: normal;
            margin: 0;
        }
        
        QMenu::item {
            padding: 8px 20px 8px 30px;
            background: transparent;
            min-height: 24px;
            border: none;
            margin: 0;
            text-align: left;
            color: #000000;
            font-family: 'Courier New', 'Consolas', 'Monaco', monospace;
            font-size: 10px;
            font-weight: normal;
        }
        
        QMenu::item:selected {
            background-color: #000000;
            color: #ffffff;
        }
        
        QMenu::separator {
            height: 1px;
            background: #000000;
            margin: 4px 0;
        }
        
        QMenu::item#shutdownItem {
            background: #000000;
            color: #ffffff;
            padding: 8px 20px 8px 30px;
            margin: 4px 0 0 0;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        QMenu::item#shutdownItem:selected {
            background: #000000;
            color: #ffffff;
        }
        
        QMdiArea {
            background: #ffffff !important;
            border: none !important;
            background-color: #ffffff !important;
        }
        
        QWidget {
            background-color: #ffffff !important;
        }
        
        QMdiSubWindow {
            background: #ffffff !important;
            border: 1px solid #000000 !important;
            border-radius: 0 !important;
        }
        
        QMdiSubWindow::title {
            background: #000000;
            color: #ffffff;
            padding: 4px 8px;
            text-align: left;
            font-family: 'Courier New', 'Consolas', 'Monaco', monospace;
            font-weight: bold;
            font-size: 9px;
            text-transform: uppercase;
        }
        
        QMdiSubWindow::close-button, QMdiSubWindow::max-button {
            background: #000000;
            color: #ffffff;
            border: 1px solid #000000;
            width: 16px;
            height: 16px;
            margin: 1px;
            padding: 0;
            subcontrol-origin: margin;
            subcontrol-position: right center;
            font-weight: bold;
        }
        
        QMdiSubWindow::close-button:hover, QMdiSubWindow::max-button:hover {
            background: #000000;
            border-color: #000000;
        }
        
        QMdiSubWindow::close-button:pressed, QMdiSubWindow::max-button:pressed {
            background: #000000;
            border-color: #000000;
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
        """Create start menu with application list (without icons)"""
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
        """Désactivé - Ne plus afficher d'icônes"""
        return None
        
    def _create_emoji_icon(self, emoji: str) -> Optional[QIcon]:
        """Create icon from emoji"""
        if not emoji or not emoji.strip():
            return None
            
        try:
            # Créer une pixmap plus grande pour un meilleur rendu
            size = 24  # Taille plus grande pour un meilleur rendu
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.TextAntialiasing)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            
            # Essayer différentes polices emoji avec des tailles adaptées
            font_families = [
                "Segoe UI Emoji", 
                "Apple Color Emoji", 
                "Noto Color Emoji",
                "Segoe UI Symbol",
                "Arial",
                "DejaVu Sans"
            ]
            
            # Nettoyer l'emoji (prendre seulement le premier caractère si c'est une séquence)
            clean_emoji = emoji.strip()
            if len(clean_emoji) > 1 and not any(font in clean_emoji for font in font_families):
                clean_emoji = clean_emoji[0]
            
            found_font = False
            for font_family in font_families:
                font = QFont(font_family)
                font.setPixelSize(size - 4)  # Ajuster la taille selon la pixmap
                
                # Vérifier si le caractère est supporté
                if not QFontMetrics(font).inFont(clean_emoji[0]):
                    continue
                    
                found_font = True
                painter.setFont(font)
                fm = QFontMetrics(font)
                
                # Calculer la position pour centrer l'emoji
                text_width = fm.horizontalAdvance(clean_emoji)
                text_height = fm.height()
                x = (size - text_width) // 2
                y = (size - text_height) // 2 + fm.ascent()
                
                # Dessiner l'emoji
                painter.drawText(x, y, clean_emoji)
                break
            
            painter.end()
            
            if found_font:
                # Redimensionner à la taille souhaitée (16x16) avec un lissage
                return QIcon(pixmap.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                
        except Exception as e:
            print(f"Erreur création icône emoji '{emoji}': {e}")
            
        # En cas d'échec, retourner une icône par défaut
        return self.style().standardIcon(QStyle.SP_ComputerIcon)