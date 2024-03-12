import folium


india_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)


transportation_lines = 'TAMIL NADU_STATE.geojson'

folium.GeoJson(transportation_lines, name='geojson').add_to(india_map)

india_map.save('india_transportation_map.html')