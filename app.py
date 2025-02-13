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

if 'Year' not in data.columns:
    st.error("The dataset must contain a 'Year' column.")
    st.stop()


min_year = int(data['Year'].min())
max_year = int(data['Year'].max())


st.title("Climate Change Tracker")


climate_indicator = st.sidebar.selectbox(
    "Select Climate Indicator", 
    ("Sea Level Rise", "Glacier Retreat", "Deforestation")
)
year_range = st.sidebar.slider(
    "Select the range of years:",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year) 
)

data_filtered = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])]


def add_bg_from_url():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(https://static.israel21c.org/www/uploads/2019/01/shutterstock_globalwarming-1520x855.jpg);
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_url()


def create_animation(data, y_label, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(data.index.min(), data.index.max())
    ax.set_ylim(data.min() * 0.9, data.max() * 1.1)  
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
    result=function()

if climate_indicator == "Sea Level Rise":
    if 'Sea_Level_Rise' in data_filtered.columns:
        avg_sea_level_rise = data_filtered.groupby('Year')['Sea_Level_Rise'].mean()
        st.subheader(f"Average Sea Level Rise from {year_range[0]} to {year_range[1]}")
        ani = create_animation(avg_sea_level_rise, 'Average Sea Level Rise (mm)', 'Average Sea Level Rise Over Years')
    else:
        st.error("Column 'Sea_Level_Rise' not found in the dataset.")
        st.stop()

elif climate_indicator == "Glacier Retreat":
    if 'Glacier_Retreat' in data_filtered.columns:
        avg_glacier_retreat = data_filtered.groupby('Year')['Glacier_Retreat'].mean()
        st.subheader(f"Average Glacier Retreat from {year_range[0]} to {year_range[1]}")
        ani = create_animation(avg_glacier_retreat, 'Average Glacier Retreat (km²)', 'Average Glacier Retreat Over Years')
    else:
        st.error("Column 'Glacier_Retreat' not found in the dataset.")
        st.stop()

elif climate_indicator == "Deforestation":
    if 'Deforestation' in data_filtered.columns:
        avg_deforestation = data_filtered.groupby('Year')['Deforestation'].mean()
        st.subheader(f"Average Deforestation from {year_range[0]} to {year_range[1]}")
        ani = create_animation(avg_deforestation, 'Average Deforestation (hectares)', 'Average Deforestation Over Years')
    else:
        st.error("Column 'Deforestation' not found in the dataset.")
        st.stop()


writer = PillowWriter(fps=2)
with NamedTemporaryFile(delete=False, suffix=".gif") as temp_file:
    ani.save(temp_file.name, writer=writer)
    st.image(temp_file.name)
    
    
