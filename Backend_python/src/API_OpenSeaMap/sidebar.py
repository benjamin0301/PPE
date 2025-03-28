from folium import Element

from folium import Element

def add_sidebar(m, sidebar_content):
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
      <div id="sidebar-content">
        {sidebar_content}
      </div>
    </div>
    <script>
      function updateSidebar(content) {{
          document.getElementById("sidebar-content").innerHTML = content;
      }}
      window.addEventListener("load", function() {{
          if(window.map_9d9aaabb2dcd26a8bf3a05e4b00bd102){{
              window.map_9d9aaabb2dcd26a8bf3a05e4b00bd102.on('popupopen', function(e) {{
                  updateSidebar(e.popup.getContent());
              }});
          }}
      }});
    </script>
    """
    m.get_root().html.add_child(Element(sidebar_html))
