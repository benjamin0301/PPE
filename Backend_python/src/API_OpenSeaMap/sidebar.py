from folium import Element

def add_sidebar(m, sidebar_content):
    """
    Ajoute la sidebar statique contenant les informations de chaque checkpoint
    et la boussole dynamique affichant le cap du bateau.
    """
    sidebar_html = f"""
    <script src="../../src/JS/compass.js"></script>
    <script>
    // Initialisation de la carte pour permettre l'accès à 'map' en JS
    var map = window.map || null; // Crée une variable 'map' si elle n'existe pas déjà

    document.addEventListener("DOMContentLoaded", function () {{
        if (map) {{
            map.on('popupopen', function(e) {{
                const heading = e.popup._content.match(/Yaw : (\d+(\.\d+)?)/)[1];
                showInfo(0, heading);  // Remplace l'index si nécessaire
            }});
        }} else {{
            console.error("❌ La variable 'map' n'est pas définie.");
        }}
    }});
    </script>
    <div id="sidebar" style="
         position: absolute;
         top: 0;
         left: 0;
         width: 20%;
         height: 100%;
         background-color: rgba(255,255,255,0.9);
         z-index: 9999;
         overflow: auto;
         padding: 5px;
         box-shadow: 2px 0 5px rgba(0,0,0,0.3);
         ">
      <h3 style="margin-top:0;">Infos Checkpoint</h3>
      {sidebar_content}

      <!-- Boussole -->
      <div style="margin-top: 10px; text-align: center;">
          <h4 style="margin: 0 0 5px 0;">Cap du Bateau</h4>
          <div id="compass-container" style="
              position: relative;
              width: 90%;
              height: 200px;
              margin: 0 auto;
              border: 1px solid #ccc;
              border-radius: 10px;
              overflow: hidden;
          ">
              <img src="..\\Images\\compas.png" 
                   alt="boussole" style="width:100%; height:100%; object-fit: cover;">
              <div id="compass-needle" style="
                  position: absolute;   
                  top: 50%;
                  left: 50%;
                  width: 4px;
                  height: 50%;
                  background-color: red;
                  transform-origin: bottom center;
                  transform: translate(-50%, -100%) rotate(0deg);
              "></div>
          </div>
      </div>
    </div>

    <!-- Import du fichier JavaScript externe -->
    """
    m.get_root().html.add_child(Element(sidebar_html))
