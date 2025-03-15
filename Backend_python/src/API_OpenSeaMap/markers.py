import folium
from folium import IFrame

from src.API_OpenSeaMap.sidebar import add_sidebar


def add_markers(m, navigation_data):
    """
    Ajoute les marqueurs et génère les informations de la sidebar.
    """
    times = navigation_data.get("time", [])
    latitudes = navigation_data.get("latitude", [])
    longitudes = navigation_data.get("longitude", [])
    yaws = navigation_data.get("yaw", [])
    pitches = navigation_data.get("pitch", [])
    rolls = navigation_data.get("roll", [])
    wind_speeds = navigation_data.get("wind_speed", [])
    wind_directions = navigation_data.get("wind_direction", [])

    sidebar_content = ""  # Stockera les informations affichées dans la sidebar

    for idx in range(len(latitudes)):
        # --- Contenu HTML pour la popup ---
        html = f"""
            <div style="width:240px; font-family: Arial, sans-serif; font-size: 13px; color: #333; line-height: 1.8;">
                <div style="text-align: center; margin-bottom: 2px;">
                    <h4 style="margin: 0 auto; padding: 0; color:#007bff;">Point GPS {idx + 1}</h4>
                </div>

                <p style="margin: 0; padding: 0;"><strong>Heure :</strong> {times[idx].strftime('%H:%M:%S')}</p>

                <p style="margin: 0; padding: 0;"><strong>Coord :</strong> Lat : {latitudes[idx]} | Long : {longitudes[idx]}</p>

                <p style="margin: 0; padding: 0;"><strong>Orientation :</strong></p>
                <p style="margin: 0; padding: 0;">Yaw : {yaws[idx]} | Pitch : {pitches[idx]} | Roll : {rolls[idx]}</p>

                <p style="margin: 0; padding: 0;"><strong>Vent :</strong> Speed : {wind_speeds[idx]} km/h | Dir : {wind_directions[idx]}</p>
            </div>
        """

        iframe = IFrame(html, width=250, height=160)
        popup = folium.Popup(iframe, max_width=265, parse_html=True)

        # --- Ajout du marqueur ---
        marker_color = "blue" if idx != len(latitudes) - 1 else "red"
        folium.Marker(
            location=[latitudes[idx], longitudes[idx]],
            popup=popup,
            icon=folium.Icon(color=marker_color)
        ).add_to(m)

        # --- Ajout des infos dans la sidebar ---
        sidebar_content += f"""
        <div style="padding: 5px; border-bottom: 1px solid #ddd;">
            <a href="#" onclick="showInfo({idx})">Point GPS {idx + 1}</a>
            <div id="info-{idx}" style="display:none;">
                <p><strong>Heure :</strong> {times[idx]}</p>
                <p><strong>Orientation :</strong> Yaw {yaws[idx]}, Pitch {pitches[idx]}, Roll {rolls[idx]}</p>
                <p><strong>Vent :</strong> {wind_speeds[idx]} km/h, Dir: {wind_directions[idx]}</p>
            </div>
        </div>
        """

    # Ajouter la sidebar après avoir généré le contenu
    add_sidebar(m, sidebar_content)
