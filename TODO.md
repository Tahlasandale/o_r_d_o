# Todo du projet Ordo

- [ ] affichage mode kiosk+ctrl w pour fermer l'app 
- [ ] souci quand on ferme une app et que on veut la rouvrir on peut pas
- [ ] souci persistance memoire

- [ ] Il reste du bleu dans l'app de todo faut tout passer en noir et blanc
- [ ] ajouter la touche alt qui fait comme la touche windows avec le menu démarrer
- [ ] modulariser le code donc separer dans des fichiers differents leds differenters app
- [ ] mettre tt le css dans un seul fichier 
- [ ] developper le navigateur custom en mode kiosk
- [ ] suivre la feuille de route pour dev ttes les features

```
le style doit etre vraiment le mm que celui ci mais reecrit en python:"/* Reset et variables */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}


:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f0f0f0;
    --bg-tertiary: #e0e0e0;
    --text-primary: #000000;
    --text-secondary: #333333;
    --border-color: #000000;
    --shadow: rgba(0, 0, 0, 0.2);
    --highlight: #cccccc;
}


/* Styles de base */
body {
    font-family: 'Courier New', 'Monaco', 'Consolas', monospace;
    overflow: hidden;
    height: 100vh;
    background: var(--bg-primary);
    color: var(--text-primary);
}


/* Desktop */
.desktop {
    width: 100%;
    height: 100vh;
    position: relative;
    display: flex;
    flex-direction: column;
}


.desktop-area {
    flex: 1;
    position: relative;
    overflow: hidden;
}


/* Barre des tâches */
.taskbar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    height: 40px;
    background: var(--bg-secondary);
    border-top: 2px solid var(--border-color);
    display: flex;
    align-items: center;
    padding: 0 10px;
    gap: 5px;
    z-index: 1001;
    /* Assure que la barre des tâches est toujours au-dessus de tout */
    transform: translateZ(0);
    -webkit-transform: translateZ(0);
    will-change: transform;
    box-shadow: 0 -2px 4px var(--shadow);
}


.start-button {
    background: var(--bg-primary);
    border: 2px solid var(--border-color);
    color: var(--text-primary);
    padding: 6px 20px;
    cursor: pointer;
    font-size: 14px;
    font-family: 'Courier New', monospace;
    font-weight: bold;
    transition: all 0.2s;
}


.start-button:hover {
    background: var(--highlight);
    box-shadow: 2px 2px 0 var(--shadow);
}


.start-button:active,
.start-button.active {
    background: var(--bg-tertiary);
    box-shadow: inset 2px 2px 0 var(--shadow);
}


.taskbar-icons {
    display: flex;
    gap: 8px;
    margin-left: 10px;
}


.taskbar-icon {
    width: 32px;
    height: 32px;
    background: var(--bg-primary);
    border: 2px solid var(--border-color);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 16px;
}


.taskbar-icon:hover {
    background: var(--highlight);
    transform: translateY(-2px);
    box-shadow: 3px 3px 0 var(--shadow);
}


/* Menu démarré */
.start-menu {
    position: fixed;
    bottom: 50px;
    left: 10px;
    width: 250px;
    background: var(--bg-secondary);
    border: 2px solid var(--border-color);
    box-shadow: 4px 4px 0 var(--shadow);
    z-index: 1000;
    display: none;
    flex-direction: column;
    max-height: 70vh;
    overflow-y: auto;
    /* Assure que le menu est au-dessus de tout */
    transform: translateZ(0);
    -webkit-transform: translateZ(0);
    will-change: transform;
}


.start-menu.active {
    display: block;
}


@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}


.start-menu-header {
    background: var(--border-color);
    color: var(--bg-primary);
    padding: 10px 15px;
    font-weight: bold;
    border-bottom: 2px solid var(--border-color);
}


.start-menu-items {
    background: var(--bg-primary);
}


.start-menu-item {
    padding: 12px 15px;
    cursor: pointer;
    transition: background 0.2s;
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 1px solid var(--bg-secondary);
}


.start-menu-item:hover {
    background: var(--highlight);
}


.start-menu-item-icon {
    font-size: 18px;
    width: 24px;
    text-align: center;
}


/* Fenêtres applications */
.window {
    position: absolute;
    background: var(--bg-secondary);
    border: 2px solid var(--border-color);
    box-shadow: 4px 4px 0 var(--shadow);
    min-width: 300px;
    min-height: 200px;
    display: flex;
    flex-direction: column;
    z-index: 100;
    resize: both;
    overflow: auto;
    /* Assure que les fenêtres sont en dessous du menu */
    transform: translateZ(0);
    -webkit-transform: translateZ(0);
    will-change: transform;
}


.window.active {
    display: flex;
    animation: windowOpen 0.2s ease-out;
}


@keyframes windowOpen {
    from {
        opacity: 0;
        transform: scale(0.95);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}


.window-header {
    background: var(--bg-tertiary);
    border-bottom: 2px solid var(--border-color);
    padding: 8px 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: move;
    user-select: none;
}


.window-title {
    font-size: 14px;
    font-weight: bold;
}


.window-controls {
    display: flex;
    gap: 6px;
}


.window-control {
    width: 16px;
    height: 16px;
    border: 2px solid var(--border-color);
    background: var(--bg-primary);
    cursor: pointer;
    transition: all 0.2s;
}


.window-control.close:hover {
    background: var(--border-color);
}


.window-content {
    flex: 1;
    padding: 20px;
    overflow: auto;
    background: var(--bg-primary);
}


/* App To-Do */
.todo-input-group {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}


.todo-input {
    flex: 1;
    padding: 8px;
    border: 2px solid var(--border-color);
    font-size: 14px;
    font-family: 'Courier New', monospace;
    background: var(--bg-primary);
}


.todo-input:focus {
    outline: none;
    background: var(--bg-secondary);
}


.todo-btn {
    padding: 8px 16px;
    background: var(--border-color);
    color: var(--bg-primary);
    border: 2px solid var(--border-color);
    cursor: pointer;
    transition: all 0.2s;
    font-family: 'Courier New', monospace;
    font-weight: bold;
}


.todo-btn:hover {
    background: var(--bg-primary);
    color: var(--border-color);
    box-shadow: 2px 2px 0 var(--shadow);
}


.todo-list {
    list-style: none;
}


.todo-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
    border: 1px solid var(--bg-secondary);
    margin-bottom: 5px;
    background: var(--bg-primary);
}


.todo-item:hover {
    background: var(--bg-secondary);
}


.todo-item.completed {
    opacity: 0.5;
}


.todo-item.completed .todo-text {
    text-decoration: line-through;
}


.todo-checkbox {
    width: 16px;
    height: 16px;
    cursor: pointer;
    border: 2px solid var(--border-color);
}


.todo-text {
    flex: 1;
    font-size: 14px;
}


.todo-delete {
    background: var(--border-color);
    color: var(--bg-primary);
    border: 2px solid var(--border-color);
    padding: 4px 8px;
    cursor: pointer;
    font-size: 12px;
    font-family: 'Courier New', monospace;
    transition: all 0.2s;
}


.todo-delete:hover {
    background: var(--bg-primary);
    color: var(--border-color);
}


/* App Timer */
.timer-display {
    text-align: center;
    font-size: 64px;
    font-weight: bold;
    margin: 40px 0;
    color: var(--text-primary);
    font-family: 'Courier New', monospace;
    letter-spacing: 8px;
    border: 3px solid var(--border-color);
    padding: 30px;
    background: var(--bg-secondary);
}


.timer-controls {
    display: flex;
    justify-content: center;
    gap: 15px;
}


.timer-btn {
    padding: 12px 24px;
    font-size: 14px;
    background: var(--border-color);
    color: var(--bg-primary);
    border: 2px solid var(--border-color);
    cursor: pointer;
    transition: all 0.2s;
    font-family: 'Courier New', monospace;
    font-weight: bold;
}


.timer-btn:hover {
    background: var(--bg-primary);
    color: var(--border-color);
    box-shadow: 3px 3px 0 var(--shadow);
}


.timer-complete .timer-display {
    animation: blink 1s infinite;
}


@keyframes blink {
    0%, 100% { 
        background: var(--bg-secondary);
        border-color: var(--border-color);
    }
    50% { 
        background: var(--border-color);
        color: var(--bg-primary);
    }
}


/* App Éditeur */
.editor-textarea {
    width: 100%;
    height: 100%;
    min-height: 350px;
    border: 2px solid var(--border-color);
    padding: 15px;
    font-size: 14px;
    font-family: 'Courier New', monospace;
    resize: vertical;
    background: var(--bg-primary);
}


.editor-status {
    margin-top: 10px;
    font-size: 12px;
    color: var(--text-secondary);
    text-align: right;
    padding: 5px;
    border-top: 1px solid var(--bg-secondary);
}


/* Barre de défilement personnalisée */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}


::-webkit-scrollbar-track {
    background: var(--bg-secondary);
}


::-webkit-scrollbar-thumb {
    background: var(--text-secondary);
    border: 2px solid var(--border-color);
}


::-webkit-scrollbar-thumb:hover {
    background: var(--text-primary);
}" conserver toutes les fonctionnalités fonctionnant de facon comforme```