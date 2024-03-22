from flask import Flask,render_template
import folium

app = Flask(__name__)

@app.route("/")
def home():
    m = folium.Map(location=[12.970633350175412, 80.13969680544938], zoom_start=13)

    folium.Marker(
    location=[12.915571678934642, 80.15392507645515],
    tooltip="Junction 1",
    popup= "Cars: 3 | No Issues",
    icon=folium.Icon(icon="cloud", color="pink"),
    ).add_to(m)

    folium.Marker(
    location=[12.8988, 80.2279],
    tooltip="Junction 2",
    popup= "Cars: 3 | No Issues",
    icon=folium.Icon(icon="cloud", color="red"),
    ).add_to(m)

    folium.Marker(
    location=[12.915571678934642, 80.15392507645515],
    tooltip="Junction 1",
    popup= "Cars: 3 | No Issues",
    icon=folium.Icon(icon="cloud", color="black"),
    ).add_to(m)

    m.get_root().width = "6px"
    m.get_root().height = "500px"
    map_iframe = m.get_root()._repr_html_()

    return render_template('home.html',map_iframe = map_iframe)

if __name__ == "__main__":
    app.run(host='localhost',port=5000,debug=True)


# from flask import Flask, render_template
# import folium
# import json

# app = Flask(__name__)

# # Sample data dictionary containing details for each marker
# marker_details = {
#     "Junction 1": {"Cars": 3, "Issues": "No Issues"},
#     "Junction 2": {"Cars": 5, "Issues": "Traffic Congestion"}
# }

# @app.route("/")
# def home():
#     m = folium.Map(location=[12.970633350175412, 80.13969680544938], zoom_start=13)

#     for junction, details in marker_details.items():
#         popup_content = generate_popup_content(details)
#         folium.Marker(
#             location=[12.915571678934642, 80.15392507645515],
#             tooltip=junction,
#             popup=folium.Popup(popup_content, max_width=300),
#             icon=folium.Icon(icon="cloud", color="pink"),
#         ).add_to(m)

#     m.get_root().width = "6px"
#     m.get_root().height = "500px"
#     map_iframe = m.get_root()._repr_html_()

#     return render_template('home.html', map_iframe=map_iframe, marker_details_json=json.dumps(marker_details))

# def generate_popup_content(details):
#     """
#     Generate HTML content for the popup based on the details dictionary.
#     """
#     content = "<h3>Marker Details</h3>"
#     for key, value in details.items():
#         content += f"<p><strong>{key}:</strong> {value}</p>"
#     return content

# if __name__ == "__main__":
#     app.run(host='localhost', port=5000, debug=True)
