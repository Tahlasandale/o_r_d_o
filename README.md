# 🧭 ORDO - Système de Productivité Minimaliste

**ORDO** est un environnement de productivité innovant qui démarre instantanément dans un navigateur web minimaliste, offrant un espace de travail épuré et focalisé.

## 🚀 Fonctionnalités principales

- **Interface épurée** conçue pour les écrans e-ink noir et blanc
- **Démarrage instantané** avec navigation web intégrée
- **Applications essentielles** pour la productivité
- **Environnement local** avec stockage sécurisé
- **Design rétro-moderne** inspiré des interfaces classiques

## 📋 Applications incluses

- 📝 Gestionnaire de tâches (To-do)
- ⏱️ Minuteur Pomodoro
- ✍️ Éditeur Markdown
- 🌐 Navigateur web intégré
- 📂 Gestionnaire de fichiers local
- 📊 Tableau de bord quotidien
- 🎯 Suivi d'objectifs
- ☁️ Applications web (ChatGPT, etc.)

## 🛠️ Architecture technique

- **Système hôte** : Linux minimal (Raspberry Pi OS Lite)
- **Interface** : HTML, CSS, JavaScript pur
- **Backend** : Node.js pour la gestion des fichiers et préférences
- **Stockage** : Fichiers locaux et IndexedDB/SQLite
- **Communication** : API interne via WebSocket local

## 🚧 Développement

### Structure des dossiers

```
/
├── apps/           # Applications web
├── data/           # Données utilisateur
├── public/         # Fichiers statiques
└── system/         # Fichiers système
```

### Prérequis

- Node.js 16+
- Navigateur web moderne
- (Optionnel) Raspberry Pi pour le déploiement

### Installation

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/Tahlasandale/o_r_d_o.git
   cd o_r_d_o
   ```

2. Installer les dépendances :
   ```bash
   npm install
   ```

3. Démarrer le serveur de développement :
   ```bash
   npm start
   ```

## 📝 Todo

- [ ] Remplacer les éléments bleus par du noir et blanc
- [ ] Ajouter la touche Alt pour le menu système
- [ ] Modulariser le code source
- [ ] Unifier les fichiers CSS
- [ ] Développer le navigateur en mode kiosk

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus d'informations.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📞 Contact

Pour toute question ou suggestion, contactez-nous à [votre email].

---

*ORDO - La productivité, réinventée.*
