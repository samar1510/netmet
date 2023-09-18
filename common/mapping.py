# Create a world map to show distributions of users
import folium
from folium.plugins import MarkerCluster

from common.default import TP1_ANCHORS_PATH, TP1_PROBES_PATH, TP1_RESULTS_PATH
from common.file_utils import load_json

ANCHOR_RADIUS = 0.2
PROBES_RADIUS = 0.1


def set_folium_marker(coordinates: list, radius: int) -> None:
    """get list of coordinates set marker on folium map"""
    for coordinate in coordinates:
        lat = coordinate[0]
        lon = coordinate[1]

        folium.CircleMarker(location=[lat, lon], radius=radius, fill=True).add_to(
            marker_cluster
        )  # show the map


if __name__ == "__main__":
    probes = load_json(TP1_PROBES_PATH)
    anchors = load_json(TP1_ANCHORS_PATH)

    # empty map
    ripe_atlas_map = folium.Map(tiles="cartodbpositron")
    marker_cluster = MarkerCluster().add_to(ripe_atlas_map)

    anchors_coordinates = [anchor["geometry"]["coordinates"] for anchor in anchors]
    set_folium_marker(anchors_coordinates, ANCHOR_RADIUS)

    probe_coordinates = [probe["geometry"]["coordinates"] for probe in probes]
    set_folium_marker(probe_coordinates, PROBES_RADIUS)

    ripe_atlas_map.save(TP1_RESULTS_PATH / "ripe_atlas_map.html")
