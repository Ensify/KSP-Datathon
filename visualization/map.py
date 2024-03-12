import plotly.graph_objs as go
import plotly.express as px

india_states = px.data.gapminder().query("country == 'India'")

fig = go.Figure(data=go.Choropleth(
    locations=india_states['iso_alpha'],
    z=india_states['pop'],
    text=india_states['country'],
    colorscale='Viridis',
    autocolorscale=False,
    marker_line_color='white', 
    colorbar_title="Population"
))

fig.update_layout(
    title_text='Population of India by State',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    )
)

fig.show()
