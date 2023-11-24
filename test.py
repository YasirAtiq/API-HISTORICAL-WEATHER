from datetime import datetime
import plotly.express as px
import streamlit as st
from json import decoder
import requests

st.title("Historical API for Train Station Weather")

years_to_include = []
for i in range(1756, 2023):
    years_to_include.append(i)

station_numbers = []
for i in range(1, 25829):
    station_numbers.append(i)

st.selectbox(label="Year to select:", options=years_to_include, key="year")
st.selectbox(label="Station number:", options=station_numbers,
             key="station no.")
st.text_input(label="API Key: ", value="demo_key", key="api_key",
              type="password")

api_url = f"http://127.0.0.1:5000/api/all_data_for_station_annual/" \
          f"{st.session_state['station no.']}/{st.session_state['year']}/" \
          f"api_key={st.session_state['api_key']}"

response = requests.get(api_url)
try:
    api = response.json()
except decoder.JSONDecodeError:
    api = ""
if api == []:
    st.info("The record you were asking wasn't available.", icon="⚠️")
else:
    graph_details = {'x': [], 'y': []}
    if api == "":
        st.info("The record you were asking wasn't available" \
                " or API key was incorrect.", icon="⚠️")
    else:
        for record in api:
            date = datetime.strptime(record["date"], "%Y-%m-%d")
            temperature = record["temperature"]
            graph_details["x"].append(date)
            graph_details["y"].append(temperature)

        line_graph = px.line(x=graph_details["x"], y=graph_details["y"],
                            labels={"x": "Date", "y": "Temperature"})
        st.plotly_chart(line_graph)