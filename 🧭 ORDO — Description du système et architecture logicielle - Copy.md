# **🧭 ORDO — Description du système et architecture logicielle**

Ordo réinvente la productivité : un appareil compact qui démarre instantanément dans un **desktop web minimaliste**, combinant toutes vos applications essentielles dans un environnement contrôlé, local et ultra-fluide. Tout ce dont vous avez besoin pour travailler, créer et organiser vos journées, accessible d’un simple clic.

## **1️⃣ Concept général**

Ordo est un appareil entièrement dédié à la **productivité locale**.  
 Plutôt que de proposer un OS traditionnel avec fenêtres et programmes natifs, Ordo repose entièrement sur le **web** : son interface est un **navigateur**, et toutes les applications sont des **pages web** (HTML, CSS, JS).  
Au démarrage :  
Aucun bureau classique n’apparaît.  
Le navigateur s’ouvre automatiquement en plein écran sur une **page locale** servant de desktop web.  
Cette interface principale gère :  
Les icônes des applications  
Le menu principal  
La navigation entre les apps  
La communication entre modules  
Chaque application s’exécute dans un **iframe ou container isolé**, avec des permissions spécifiques (par exemple, Internet uniquement pour ChatGPT).

## **2️⃣ Structure logicielle globale**

**Système hôte** : Linux minimal (Raspberry Pi OS Lite ou équivalent)  
**Lancement automatique** : boot → navigateur custom en mode kiosk → ouverture automatique de index.html local  
**Langages utilisés** :  
Frontend : HTML, CSS, JavaScript pur (ou framework minimal type Svelte / VanillaJS)  
Backend local : [Node.js](http://node.js) pour gérer fichiers, préférences et cache  
Extensions : API locales pour accès fichiers, stockage, etc.

## **3️⃣ Interface utilisateur principale**

Desktop web épuré, fond fixe, optimisé pour **écran e-ink noir et blanc** afin d’**augmenter l’autonomie**  
Barre de tâches inférieure avec :  
Menu principal  
Heure et date  
Indicateurs système (batterie, réseau)  
Système de fenêtres simplifié : chaque app s’ouvre en pseudo-fenêtre ou plein écran

## **4️⃣ Design & ergonomie**

**Design du desktop** : simple et nostalgique, inspiré de **Windows XP ou Macintosh classique**, mais modernisé pour être **fluide, agréable et intuitif**  
**Design du boîtier** : rétro, rappelant cette époque iconique, tout en restant minimaliste et fonctionnel  
**Écran noir et blanc** : pour un style rétro et une **meilleure autonomie**, idéal pour les sessions longues de travail concentré  
L’interface conserve un équilibre entre **style vintage et modernité**, pour que l’expérience soit **à la fois familière et agréable à utiliser**

## **5️⃣ Liste des applications/modules**

ChatGPT (Assistant IA)  
Gestionnaire de tâches (To-do)  
Timer / Pomodoro  
Smart Timer  
Éditeur Markdown innovant  
Navigateur intégré Ordo  
Gestionnaire de fichiers local (explorateur)  
Daily Feedback Manager  
Agrégateur RSS  
Météo  
Vue du planning quotidien  
Toolbox de sites utiles  
Tableau blanc  
Gamification des objectifs long terme (Missionnaire)  
Toutes ces applications sont des **web apps indépendantes**, accessibles depuis le desktop.

## **6️⃣ Communication et stockage**

**Stockage local** :  
Fichiers apps : /usr/share/ordo/apps/\<nom\_app\>  
Données utilisateur : /home/ordo/data/\<app\_name\>/  
Base locale : IndexedDB ou SQLite  
**Communication entre apps** : via postMessage ou API interne (WebSocket local)  
Exemple : le timer notifie le gestionnaire de tâches en fin de session

## **7️⃣ Expérience au démarrage**

L’utilisateur allume Ordo  
Le système Linux boot → lancement automatique du navigateur  
Chargement de index.html → desktop web  
L’utilisateur ouvre les apps en cliquant sur les icônes  
Chaque app s’ouvre dans une fenêtre HTML simulée ou plein écran  
Toutes les données restent locales, sauf apps nécessitant Internet (ChatGPT)

## **8️⃣ Philosophie du projet**

Ordo n’est pas un OS classique : c’est une **interface web autonome** tournée vers la **concentration et la créativité**.  
 Il combine la puissance du web moderne avec la **sobriété d’un environnement local et contrôlé**, tout en offrant un **design rétro-moderne agréable et intuitif**.

## **9️⃣ Équipe nécessaire et rôles**

**Conception & architecture**  
Chef de projet / Product Owner  
Architecte logiciel  
Architecte hardware / électronique  
**Développement logiciel**  
Développeurs frontend (JS/HTML/CSS)  
Développeur backend / [Node.js](http://node.js)  
Ingénieur navigateur / intégration OS  
**Développement hardware**  
Électronicien / ingénieur embarqué  
Prototypiste / fabricant  
**UX / UI / design**  
Designer UX/UI  
Graphiste  
**Tests & qualité**  
QA / Testeurs logiciels  
Testeur hardware

## **🔟 Grandes phases du projet**

**Phase 1 : Développement logiciel & prototype**  
Spécification de l’architecture logicielle  
Développement des applications web et du navigateur custom  
Tests unitaires et intégration des apps dans le desktop web  
**Phase 2 : Prototypage hardware**  
Conception du boîtier, intégration écran et batterie  
Tests de compatibilité hardware / OS minimal / navigateur  
Validation performances et consommation  
**Phase 3 : Intégration hardware**  
Assemblage complet de l’appareil  
Vérification de l’ergonomie, connectivité et robustesse  
**Phase 4 : Tests & validation**  
Fonctionnels et ergonomie des apps  
Tests hardware : autonomie, robustesse, écran  
Optimisations et corrections  
**Phase 5 : Pré-production / production pilote**  
Fabrication d’un petit nombre d’exemplaires  
Tests terrain pour feedback utilisateurs  
Ajustements avant production finale