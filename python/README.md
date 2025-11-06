# ORDO Python Desktop

Mini-navigateur de bureau style ORDO, avec apps Web (QWebEngineView) et apps locales Qt.

## Prérequis
- Python 3.10+
- Windows (testé), devrait fonctionner macOS/Linux

## Installation
```bash
python -m venv .venv
.venv/Scripts/pip install -r python/requirements.txt
```

## Lancer
```bash
python python/run.py
```

## Structure
- `python/src/ordo/` coeur de l'app
- `python/apps.yaml` manifest des apps (web/local)
- `css/poc-styles.css` réutilisé et appliqué comme Qt stylesheet

## Notes
- Les sites qui bloquent l'embed en iframe Web ne sont pas bloquants ici: on charge la page directement dans un navigateur intégré.
- Les apps locales sont stylées via le stylesheet dérivé de `poc-styles.css` (Qt ignore les règles non supportées).

