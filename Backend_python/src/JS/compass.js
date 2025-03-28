// compass.js
console.log("🧭 Initialisation du compass.js");

function showInfo(idx, heading) {
    console.log(`✅ showInfo appelée avec idx = ${idx} | Cap du bateau = ${heading}`);

    const headingValue = parseFloat(heading);

    if (!isNaN(headingValue)) {
        const needle = document.getElementById("compass-needle");

        if (needle) {
            const rotation = `translate(-50%, -100%) rotate(${headingValue}deg)`;
            needle.style.transform = rotation;
            console.log(`🧭 Mise à jour de l'aiguille : ${rotation}`);
        } else {
            console.error("❌ L'aiguille n'a pas été trouvée dans le DOM.");
        }
    } else {
        console.error("❌ Erreur : 'heading' n'est pas un nombre valide.");
    }
}


