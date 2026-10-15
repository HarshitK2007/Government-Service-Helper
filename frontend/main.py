import streamlit as st
from statedist import geo_data
from utils_google import find_government_services as fgs
from utils_tinyfish import ask_tinyfish as atf
import urlManager as uM
import json
from time import sleep as s

statedistDict = geo_data()

st.title("Government service helper")

need = st.text_input(label = "Enter the service you need:")

state = st.selectbox(label = "Select the state:", options = statedistDict.keys(), index = None)

search_start = 0
dist = 0

if state:
    dist = st.selectbox(label = f"Select district of {state}", options = statedistDict[state], index = None)
    
if dist:    
    search_start = st.button("Search")

# if search_start:
#     with st.spinner():
#         s(3)
#         st.markdown("ipsum lorem")
    