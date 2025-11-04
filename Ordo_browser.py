#!/usr/bin/env python3
"""
Ordo Browser - Navigateur minimaliste dédié
Version complète avec interface native PyQt5
"""

import os
import sys
import threading
import http.server
import socketserver
from pathlib import Path

# Vérification et import des modules requis
try:
    from PyQt5.QtCore import QUrl, Qt
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QShortcut, 
                               QMessageBox, QLineEdit, QVBoxLayout, QWidget)
    from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
    from PyQt5.QtGui import QKeySequence
    PYQT_AVAILABLE = True
except ImportError as e:
    print(f"Erreur d'importation PyQt5: {e}")
    PYQT_AVAILABLE = False
    import webbrowser

# Configuration
PORT = 8000
HERE = Path(__file__).parent.absolute()
INDEX_FILE = HERE / "index.html"

class LocalServerHandler(http.server.SimpleHTTPRequestHandler):
    """Handler HTTP personnalisé pour servir les fichiers locaux"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(HERE), **kwargs)
    
    def log_message(self, format, *args):
        """Surcharge pour logger proprement"""
        print(f"[Ordo Server] {format % args}")
    
    def end_headers(self):
        """Ajoute les headers CORS pour éviter les problèmes"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()


class OrdoBrowser(QMainWindow):
    """Fenêtre principale du navigateur Ordo avec WebEngine"""
    
    def __init__(self, url):
        super().__init__()
        self.init_ui(url)
    
    def init_ui(self, url):
        """Initialise l'interface utilisateur"""
        # Configuration de la fenêtre
        self.setWindowTitle("Ordo Browser")
        self.setGeometry(0, 0, 1920, 1080)
        
        # Widget central et layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Barre d'URL (cachée par défaut)
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Entrez une URL et appuyez sur Entrée...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.hide()  # Masquée par défaut
        self.url_bar.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 4px;
                margin: 5px;
                background-color: white;
                color: #333;
            }
            QLineEdit:focus {
                border: 2px solid #4a90e2;
                padding: 7px;
            }
        """)
        layout.addWidget(self.url_bar)
        
        # WebView
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))
        self.browser.urlChanged.connect(self.update_url)
        layout.addWidget(self.browser)
        
        # Configuration du moteur web
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)
        
        # Raccourcis clavier
        self.setup_shortcuts()
        
        # Mode plein écran par défaut
        self.showFullScreen()
        
        print("[Ordo Browser] Interface lancée en mode plein écran")
    
    def setup_shortcuts(self):
        """Configure les raccourcis clavier"""
        # F11 pour basculer plein écran
        fullscreen_shortcut = QShortcut(QKeySequence("F11"), self)
        fullscreen_shortcut.activated.connect(self.toggle_fullscreen)
        
        # Raccourcis pour quitter
        quit_shortcut1 = QShortcut(QKeySequence("Ctrl+Q"), self)
        quit_shortcut1.activated.connect(self.close)
        
        # Ajout de Ctrl+W pour quitter (comme dans la plupart des navigateurs)
        quit_shortcut2 = QShortcut(QKeySequence("Ctrl+W"), self)
        quit_shortcut2.activated.connect(self.close)
        
        # Ctrl+U pour afficher/masquer la barre d'URL
        url_shortcut = QShortcut(QKeySequence("Ctrl+U"), self)
        url_shortcut.activated.connect(self.toggle_url_bar)
        
        # F5 pour recharger
        reload_shortcut = QShortcut(QKeySequence("F5"), self)
        reload_shortcut.activated.connect(self.browser.reload)
        
        # Ctrl+R pour recharger
        reload_shortcut2 = QShortcut(QKeySequence("Ctrl+R"), self)
        reload_shortcut2.activated.connect(self.browser.reload)
        
        # Retour arrière
        back_shortcut = QShortcut(QKeySequence("Alt+Left"), self)
        back_shortcut.activated.connect(self.browser.back)
        
        # Avancer
        forward_shortcut = QShortcut(QKeySequence("Alt+Right"), self)
        forward_shortcut.activated.connect(self.browser.forward)
    
    def toggle_fullscreen(self):
        """Bascule entre mode plein écran et fenêtré"""
        if self.isFullScreen():
            self.showNormal()
            print("[Ordo Browser] Mode fenêtré")
        else:
            self.showFullScreen()
            print("[Ordo Browser] Mode plein écran")
    
    def toggle_url_bar(self):
        """Affiche ou masque la barre d'URL"""
        if self.url_bar.isHidden():
            # Met à jour l'URL actuelle avant d'afficher la barre
            current_url = self.browser.url().toString()
            self.url_bar.setText(current_url)
            self.url_bar.show()
            self.url_bar.setFocus()
            self.url_bar.selectAll()
        else:
            self.url_bar.hide()
            self.browser.setFocus()
    
    def navigate_to_url(self):
        """Navigue vers l'URL entrée dans la barre"""
        url = self.url_bar.text().strip()
        if not url:
            self.url_bar.hide()
            return
            
        if not url.startswith(('http://', 'https://', 'file://')):
            url = 'http://' + url
            
        self.browser.setUrl(QUrl(url))
        self.url_bar.hide()
        self.browser.setFocus()
    
    def update_url(self, url):
        """Met à jour la barre d'URL lors de la navigation"""
        self.url_bar.setText(url.toString())
    
    def keyPressEvent(self, event):
        """Gestion des touches clavier globales"""
        # ESC pour quitter le plein écran (mais pas fermer l'app)
        if event.key() == Qt.Key_Escape and self.isFullScreen():
            self.showNormal()
        else:
            super().keyPressEvent(event)


def start_local_server():
    """Lance le serveur HTTP local en arrière-plan"""
    try:
        with socketserver.TCPServer(("", PORT), LocalServerHandler) as httpd:
            print(f"[Ordo Server] Serveur démarré sur http://localhost:{PORT}")
            httpd.serve_forever()
    except OSError as e:
        print(f"[Ordo Server] Erreur: {e}")
        print(f"[Ordo Server] Le port {PORT} est peut-être déjà utilisé")


def check_needs_server():
    """Vérifie si le fichier index.html nécessite un serveur"""
    if not INDEX_FILE.exists():
        return True
    
    # Lecture du contenu pour détecter fetch() ou API calls
    try:
        content = INDEX_FILE.read_text(encoding='utf-8')
        needs_server = any([
            'fetch(' in content,
            'XMLHttpRequest' in content,
            '.json' in content and 'fetch' in content.lower(),
            'import ' in content and 'from' in content,  # ES6 modules
        ])
        return needs_server
    except Exception:
        return True


def launch_with_pyqt(url):
    """Lance le navigateur avec PyQt5"""
    app = QApplication(sys.argv)
    app.setApplicationName("Ordo Browser")
    
    browser = OrdoBrowser(url)
    browser.show()
    
    sys.exit(app.exec_())


def launch_with_webbrowser(url):
    """Lance le navigateur par défaut du système"""
    print(f"[Ordo Browser] PyQt5 non disponible, utilisation du navigateur système")
    print(f"[Ordo Browser] Ouverture de: {url}")
    webbrowser.open(url, new=1)
    
    # Garder le script actif si un serveur tourne
    if "localhost" in url:
        print("[Ordo Browser] Serveur actif. Pressez Ctrl+C pour arrêter.")
        try:
            while True:
                threading.Event().wait(1)
        except KeyboardInterrupt:
            print("\n[Ordo Browser] Arrêt du serveur")


def main():
    """Point d'entrée principal"""
    print("=" * 60)
    print("    ORDO BROWSER - Navigateur Minimaliste Dédié")
    print("=" * 60)
    print()
    
    # Vérification du fichier index.html
    if not INDEX_FILE.exists():
        print(f"[Ordo Browser] ERREUR: {INDEX_FILE} introuvable!")
        print(f"[Ordo Browser] Créez un fichier index.html dans: {HERE}")
        
        # Création d'un index.html de démo
        demo_html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ordo Browser - Démo</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            text-align: center;
            max-width: 800px;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            padding: 60px 40px;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        h1 { font-size: 3em; margin-bottom: 20px; }
        p { font-size: 1.2em; line-height: 1.6; margin-bottom: 30px; }
        .shortcuts {
            text-align: left;
            background: rgba(0,0,0,0.2);
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
        }
        .shortcuts h2 { margin-bottom: 15px; }
        .shortcuts ul { list-style: none; }
        .shortcuts li { padding: 8px 0; }
        .key {
            background: rgba(255,255,255,0.2);
            padding: 4px 8px;
            border-radius: 4px;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Ordo Browser</h1>
        <p>Bienvenue dans votre navigateur minimaliste dédié !</p>
        <p>Remplacez ce fichier <strong>index.html</strong> par votre propre contenu.</p>
        
        <div class="shortcuts">
            <h2>⌨️ Raccourcis clavier</h2>
            <ul>
                <li><span class="key">F11</span> → Basculer plein écran</li>
                <li><span class="key">F5</span> ou <span class="key">Ctrl+R</span> → Recharger</li>
                <li><span class="key">Alt+←</span> / <span class="key">Alt+→</span> → Navigation</li>
                <li><span class="key">Ctrl+Q</span> → Quitter</li>
                <li><span class="key">ESC</span> → Sortir du plein écran</li>
            </ul>
        </div>
    </div>
    
    <script>
        console.log('Ordo Browser - Prêt!');
        console.log('Accès Internet:', navigator.onLine ? 'Actif' : 'Inactif');
    </script>
</body>
</html>"""
        
        INDEX_FILE.write_text(demo_html, encoding='utf-8')
        print(f"[Ordo Browser] ✓ Fichier de démo créé: {INDEX_FILE}")
        print()
    
    # Détermination du mode de lancement
    needs_server = check_needs_server()
    
    if needs_server:
        print("[Ordo Browser] Détection: serveur HTTP nécessaire")
        # Lancement du serveur en thread daemon
        server_thread = threading.Thread(target=start_local_server, daemon=True)
        server_thread.start()
        
        # Attendre que le serveur soit prêt
        import time
        time.sleep(0.5)
        
        url = f"http://localhost:{PORT}/index.html"
    else:
        print("[Ordo Browser] Détection: ouverture directe possible")
        url = INDEX_FILE.as_uri()
    
    print(f"[Ordo Browser] URL: {url}")
    print()
    
    # Lancement du navigateur
    if PYQT_AVAILABLE:
        print("[Ordo Browser] Lancement avec PyQt5 WebEngine")
        launch_with_pyqt(url)
    else:
        print("[Ordo Browser] PyQt5 non installé")
        print("[Ordo Browser] Installez-le avec: pip install PyQt5 PyQtWebEngine")
        launch_with_webbrowser(url)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[Ordo Browser] Arrêt demandé par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n[Ordo Browser] ERREUR: {e}")
        sys.exit(1)