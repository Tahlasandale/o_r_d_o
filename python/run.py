import sys
from PySide6.QtWidgets import QApplication
from src.ordo.main_window import OrdoMainWindow


def main() -> None:
    # Création de l'application Qt
    app = QApplication(sys.argv)
    
    # Configuration du style par défaut pour l'application
    app.setStyle("Fusion")  # Utilisation du style Fusion pour une apparence plus moderne
    
    # Création et affichage de la fenêtre principale
    window = OrdoMainWindow()
    window.show()
    
    # Démarrage de la boucle d'événements
    sys.exit(app.exec())


if __name__ == '__main__':
    main()


