import streamlit as st
import pandas as pd
import altair as alt

st.title("UFO Sightings Report")
st.write("This app looks at when UFO sightings are reported, using the UFO sightings dataset.")

url = "https://github.com/UIUC-iSchool-DataViz/is445_data/raw/main/ufo-scrubbed-geocoded-time-standardized-00.csv"

@st.cache_data
def load_data():
    ufo = pd.read_csv(url, header=None)
    ufo.columns = ['datetime', 'city', 'state', 'country', 'shape', 'duration_seconds',
                   'duration', 'comments', 'date_posted', 'latitude', 'longitude']
    ufo['datetime'] = pd.to_datetime(ufo['datetime'], format='%m/%d/%Y %H:%M')
    ufo['hour'] = ufo['datetime'].dt.hour
    ufo['month'] = ufo['datetime'].dt.month_name()
    return ufo

ufo = load_data()

st.header("UFO Sightings by Hour of Day")

shape = st.selectbox("Pick a shape:", ['all', 'light', 'triangle', 'circle', 'fireball', 'sphere', 'disk'])

if shape == 'all':
    data = ufo
else:
    data = ufo[ufo['shape'] == shape]

hourly = data.groupby('hour').size().reset_index(name='count')

chart1 = alt.Chart(hourly).mark_bar().encode(
    x=alt.X('hour:O', title='Hour of Day (0 = midnight)'),
    y=alt.Y('count:Q', title='Number of Sightings'),
    tooltip=['hour', 'count']
)

st.altair_chart(chart1, use_container_width=True)

st.write("This bar chart shows how many UFO sightings were reported during each hour of the day. The main feature it highlights is that sightings are much more common at night: they peak at 9 PM (hour 21) with over 11,000 reports and drop to their lowest around 8 AM with only about 800. I used bars because each hour is a separate category, and I treated hour as an ordinal variable so the bars stay in order from midnight to 11 PM. The number of sightings is quantitative on the y-axis. The dropdown lets you filter the chart by reported shape, which shows that the nighttime peak holds for every shape, including fireballs, which also peak at 9 PM. I kept the default single color since color isn’t encoding any variable here. If I had more time, I would color the bars by day versus night to make the pattern stand out even more, and add a second dropdown to filter by year.")

st.header("UFO Sightings by Month")

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

monthly = ufo.groupby('month').size().reset_index(name='count')

chart2 = alt.Chart(monthly).mark_line(point=True).encode(
    x=alt.X('month:O', title='Month', sort=months),
    y=alt.Y('count:Q', title='Number of Sightings'),
    tooltip=['month', 'count']
)

st.altair_chart(chart2, use_container_width=True)

st.write("This line chart shows the total number of UFO sightings reported in each month of the year. The feature I wanted to highlight is the seasonal pattern: sightings are highest in the summer, peaking in July with about 9,500 reports, and lowest in February with about 4,700, roughly half as many. I used a line with points because the line makes the rise and fall across the year easy to follow, while the points mark the exact value for each month. Month is ordinal and kept in calendar order, and the number of sightings is quantitative. If I had more time, I would add the same shape dropdown as the first plot so you could see whether every shape follows the summer peak, and I would compare the pattern across different decades.")
st.write("Both of these plots are new and were not used in my Homework #5.")
