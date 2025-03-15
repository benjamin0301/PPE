// sidebar.js
// Lorsqu'une popup s'ouvre, on met à jour la sidebar avec son contenu.
document.addEventListener("DOMContentLoaded", function() {
    // Vérifier que la variable "map" est disponible
    if (typeof map !== "undefined") {
        map.on('popupopen', function(e) {
            var content = e.popup.getContent();
            document.getElementById('dynamic-info').innerHTML = content;
        });
    }
});
