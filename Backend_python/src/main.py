import os

from src.data_esp32.extract_json_data import load_navigation_data, display_navigation_data
import src.data_esp32.call_data as call_data
from src.utils.GPS.distance_tracker import calculate_distances
from src.utils.GPS.speed_operation import calculate_speeds
from src.API_OpenSeaMap.plot_gps import plot_gps_route

if __name__ == '__main__':
    json_file_path = os.path.join(os.path.dirname(__file__), "../data/json_data_files/navigation_data.json")
    navigation_data = load_navigation_data(json_file_path)
    display_navigation_data(navigation_data)
    calculate_distances(navigation_data)
    calculate_speeds(navigation_data)

