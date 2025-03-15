from folium import Element

def add_sidebar(m, sidebar_content):
    """
    Ajoute la sidebar statique contenant les informations de chaque checkpoint.
    """
    sidebar_html = f"""
    <div id="sidebar" style="
         position: absolute;
         top: 0;
         left: 0;
         width: 20%;
         height: 100%;
         background-color: rgba(255,255,255,0.9);
         z-index: 9999;
         overflow: auto;
         padding: 10px;
         box-shadow: 2px 0 5px rgba(0,0,0,0.3);
         ">
      <h3 style="margin-top:0;">Infos Checkpoint</h3>
      {sidebar_content}
    </div>

    <script>
    // Fonction pour afficher/masquer les informations détaillées des checkpoints
    function showInfo(idx) {{
        var infoDiv = document.getElementById("info-" + idx);
        if (infoDiv.style.display === "none") {{
            infoDiv.style.display = "block";
        }} else {{
            infoDiv.style.display = "none";
        }}
    }}
    </script>
    """
    m.get_root().html.add_child(Element(sidebar_html))
