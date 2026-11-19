import json
from pathlib import Path
import streamlit as st
from utils import util_StateDist as uSD
from utils import util_Google as uGO
from utils import util_TinyFish as uTF
from utils import util_UrlManager as uUM
from utils import util_EnglishHindi as uEH
from utils import util_Speak as uSP

RESULT_LANG = {"English": "English", "हिंदी": "Hindi"}

left, center, right = st.columns([1, 2, 1])

with center:
    
    st.image(
        "data/logo.png",
        width=150
    )

language = st.radio("Language / भाषा", ["English", "हिंदी"],index=0)
response_speed = st.radio("Stealth / Lite",["Stealth","Lite"],index=0)

statedistDict = uSD.geo_data(language)

t = uEH.EngToHin()[language]



st.title(t["title"])

need = st.text_input(label = t["need"])

need = need.strip().lower()

state = st.selectbox(label = t["state"], options = statedistDict.keys(), index = None)

if state:
    dist = st.selectbox(label = f"{t["district"].format(state = state)}", options = statedistDict[state], index = None)


if need and state and dist:
    if st.button(t["search"]):
        try:
            with st.spinner(t["finding"]):
                url = uUM.get_url(need, state.lower(), dist.lower())

                if not url:

                    url = uGO.find_website(need, state, dist)
                    if "https:" not in url:
                        raise ValueError(t["error_url"])
                    uUM.save_url(need, state, dist, url)

        except Exception as e:
            st.error(f"{t['error_url']}: {e}")
            st.stop()

        try:
            with st.spinner(t["reading"].format(url=url)):
                temp = uTF.ask_tinyfish(url, need, state, dist, RESULT_LANG[language],response_speed)

            response = temp.result["result"]

            if language == "हिंदी":
                with st.spinner(t["translating"]):
                    response = uGO.ensure_hindi(response) 

            st.markdown(response)

            with st.spinner(t["audio"]):
                st.audio(uSP.speak(response))

        except Exception as e:
            print(e)
            st.error(t["error"])
else:
    st.info(t["info"])
