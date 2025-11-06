// Fonction pour charger le footer
document.addEventListener('DOMContentLoaded', function() {
    fetch('footer.html')
        .then(response => response.text())
        .then(data => {
            const footerContainer = document.createElement('div');
            footerContainer.innerHTML = data;
            
            // Insérer le footer avant la fermeture du body
            const footer = footerContainer.querySelector('footer');
            if (footer) {
                document.body.appendChild(footer);
                
                // Ajouter les styles du footer
                const style = footerContainer.querySelector('style');
                if (style) {
                    document.head.appendChild(style);
                }
            }
        })
        .catch(error => {
            console.error('Erreur lors du chargement du footer:', error);
            // Afficher un footer minimal en cas d'erreur
            const fallbackFooter = document.createElement('footer');
            fallbackFooter.style.padding = '20px';
            fallbackFooter.style.textAlign = 'center';
            fallbackFooter.style.borderTop = '1px solid #000';
            fallbackFooter.innerHTML = `
                <p>© ${new Date().getFullYear()} Ordo — Tous droits réservés</p>
                <p><a href="confidentialite.html">Politique de confidentialité</a> | 
                <a href="legal.html">Mentions légales</a></p>
            `;
            document.body.appendChild(fallbackFooter);
        });
});
