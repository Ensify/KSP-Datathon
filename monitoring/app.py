from flask import Flask,render_template
import folium

app = Flask(__name__)

@app.route("/")
def home():
    m = folium.Map(location=[12.970633350175412, 80.13969680544938], zoom_start=13)

    m.get_root().width = "800px"
    m.get_root().height = "600px"
    map_iframe = m.get_root()._repr_html_()

    return render_template('home.html',map_iframe = map_iframe)

if __name__ == "__main__":
    app.run(host='localhost',port=5000,debug=True)