import folium
import requests


map = folium.Map(location=[12.970633350175412, 80.13969680544938], zoom_start=13)

folium.Marker(
    location=[12.915571678934642, 80.15392507645515],
    tooltip="Junction 1",
    popup= "Cars: 3 | No Issues",
    icon=folium.Icon(icon="cloud", color="pink"),
).add_to(map)

folium.Marker(
    location=[13.026596576258104, 80.12988908353888],
    tooltip= "Junction 2",
    popup="Cars: 5 | No Issues",
    icon=folium.Icon(icon="cloud",color="pink"),
).add_to(map)

folium.PolyLine(
    locations= [
        (12.915571678934642, 80.15392507645515),
        (13.026596576258104, 80.12988908353888)
    ],
    tooltip="Naanum Connection",
    color="red"
).add_to(map)

map.show_in_browser()
# map.save("secret.html")