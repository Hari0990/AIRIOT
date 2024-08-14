import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from tempfile import NamedTemporaryFile

sns.set(style="whitegrid")

try:
    data = pd.read_csv('climate_data.csv')
except FileNotFoundError:
    st.error("CSV file not found. Please check the file path.")
    st.stop()

st.title("Climate Change Tracker")

climate_indicator = st.sidebar.selectbox("Select Climate Indicator", ("Sea Level Rise", "Glacier Retreat", "Deforestation"))
year_range = st.sidebar.slider("Select the range of years:", min_value=2000, max_value=2023, value=(2000, 2023))

data_filtered = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])]

def create_animation(data, y_label, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(data.index.min(), data.index.max())
    ax.set_ylim(data.min() - 0.1 * data.min(), data.max() + 0.1 * data.max())
    ax.set_xlabel('Year')
    ax.set_ylabel(y_label)
    ax.set_title(title)
    line, = ax.plot([], [], marker='o')

    def init():
        line.set_data([], [])
        return line,

    def update(frame):
        x = data.index[:frame]
        y = data.values[:frame]
        line.set_data(x, y)
        return line,

    ani = animation.FuncAnimation(fig, update, frames=len(data), init_func=init, blit=True, interval=200, repeat=False)

    return ani

if climate_indicator == "Sea Level Rise":
    avg_sea_level_rise = data_filtered.groupby('Year')['Sea_Level_Rise'].mean()
    st.subheader("Average Sea Level Rise Over Years")
    ani = create_animation(avg_sea_level_rise, 'Average Sea Level Rise (mm)', 'Average Sea Level Rise Over Years')

elif climate_indicator == "Glacier Retreat":
    avg_glacier_retreat = data_filtered.groupby('Year')['Glacier_Retreat'].mean()
    st.subheader("Average Glacier Retreat Over Years")
    ani = create_animation(avg_glacier_retreat, 'Average Glacier Retreat (km²)', 'Average Glacier Retreat Over Years')

elif climate_indicator == "Deforestation":
    avg_deforestation = data_filtered.groupby('Year')['Deforestation'].mean()
    st.subheader("Average Deforestation Over Years")
    ani = create_animation(avg_deforestation, 'Average Deforestation (hectares)', 'Average Deforestation Over Years')
writer = PillowWriter(fps=2)
with NamedTemporaryFile(delete=False, suffix=".gif") as temp_file:
    ani.save(temp_file.name, writer=writer)
    st.image(temp_file.name)