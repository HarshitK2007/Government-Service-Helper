import streamlit as st
from utils import util_StateDist as uSD
from utils import util_Google as uGO
from utils import util_TinyFish as uTF
from utils import util_UrlManager as uUM

statedistDict = uSD.geo_data()

st.title("Government service helper")

need = st.text_input(label = "Enter the service you need:")

state = st.selectbox(label = "Select the state:", options = statedistDict.keys(), index = None)

if state:
    dist = st.selectbox(label = f"Select district of {state}", options = statedistDict[state], index = None)

need = need.strip().lower() 



if state and dist:

    if st.button("Search"):

        with st.spinner("Finding government website..."):

            try:
                url = uUM.get_url(need, state, dist)

                if not(url):
                    url = uGO.find_website(need, state, dist)
                    uUM.save_url(need, state, dist, url)

            except Exception as e:
                st.error(f"Error in finding the government website, {e}")

        try:
            if url:

                with st.spinner(f"TinyFish is reading {url}"):
                        temp = uTF.ask_tinyfish(url, need, state, dist)

                response = temp.result["result"]
                st.markdown(response)

        except:
            st.error("Somthing did not work right")
else:
    st.info("Enter a service and select a state and district.")
