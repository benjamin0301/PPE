import os

from src.data_esp32.extract_json_data import load_navigation_data, display_navigation_data, choose_file
from src.data_esp32.call_data_from_esp import call_data_from_esp
from src.utils.GPS.distance_tracker import calculate_distances
from src.utils.GPS.speed_operation import calculate_speeds
from src.API_OpenSeaMap.plot_gps import plot_gps_route

if __name__ == '__main__':
    call_data_from_esp()
    navigation_data = choose_file()
    calculate_distances(navigation_data)
    calculate_speeds(navigation_data)
    plot_gps_route(navigation_data)
