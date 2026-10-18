import streamlit as st
from utils import util_StateDist as uSD
from utils import util_Google as uGO
from utils import util_TinyFish as uTF
from utils import util_UrlManager as uUM

statedistDict = uSD.geo_data()

st.title("Government service helper")

need = st.text_input(label = "Enter the service you need:")

need = need.strip().lower()

state = st.selectbox(label = "Select the state:", options = statedistDict.keys(), index = None)

dist = None

if state:
    dist = st.selectbox(label = f"Select district of {state}", options = statedistDict[state], index = None)

if need and state and dist:

    if st.button("Search"):

        try:
            with st.spinner("Finding government website..."):

                url = uUM.get_url(need, state, dist)

                if not(url):
                    url = uGO.find_website(need, state, dist)
                    
                    if "https:" not in url:
                        raise ValueError("No valid website URL was returned.")
                        
                    uUM.save_url(need, state, dist, url)

        except Exception as e:
            st.error(f"Error in finding the government website, {e}")
            st.stop()

        try:
            with st.spinner(f"TinyFish is reading {url}"):
                    temp = uTF.ask_tinyfish(url, need, state, dist)

            response = temp.result["result"]
            st.markdown(response)
            
        except Exception as e:
            print(f"TinyFish error: {e}")
            st.error("Something did not work right")
else:
    st.info("Enter a service and select a state and district.")
