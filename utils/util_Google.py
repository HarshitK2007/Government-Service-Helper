from google import genai
from dotenv import load_dotenv
from pathlib import Path
import streamlit as st
import os
import re

def ensure_hindi(text):
    """Return text in Devanagari Hindi. Translates only if it isn't already Hindi."""
    dev = len(re.findall(r"[\u0900-\u097F]", text))
    latin = len(re.findall(r"[A-Za-z]", text))
    if dev > latin:
        return text   # already Hindi, no extra Gemini call

    resp = client.models.generate_content(
        model="gemini-2.5-flash",   # same model as in find_website
        contents=(
            "Translate this Markdown into simple Hindi written in Devanagari script only "
            "(no Roman letters, no Hinglish). Keep the Markdown structure exactly the same. "
            "Do NOT translate URLs, link targets, form numbers, or fee amounts. "
            "Return only the translated Markdown.\n\n" + text
        ),
    )
    return resp.text



BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GOOGLE_GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GOOGLE_GEMINI_API_KEY"]
    except Exception:
        st.error(
            "Gemini API key not found. "
            "Check your .streamlit/secrets.toml file."
        )
        st.stop()

client = genai.Client(api_key=api_key)

prompt = f"""
You are an assistant that helps Indian citizens find government services.

User requirements:
- Country: India

Find government services relevant to the user's requirements

Rules:
- Return a URL only if you have sufficient evidence that it belongs to an official government domain or an officially authorized service portal.
- Prefer central government domains such as gov.in and state government domains such as nic.in where applicable.
- Do not assume every website ending in nic.in or gov.in is relevant to the requested service.
- If the exact service page cannot be verified, return NOT_FOUND.
- Return only the URL or NOT_FOUND, with no additional text.
- Prefer official Indian government websites.
- Never invent URLs.
- If you are unsure whether a URL is official, mark it as unverified.
- Return direct link of the speicifc web where related need is mentioned.
- link1 return in this format and only the link.
- Return only one most legit link.
- I have seen few wesbites for some documents are for whole india, 
like i search for pan card state = ap, dist = chittoo, it returned nothing, 
but the offical whole indian wesbite will work perfectly there, 
so in such cases return whole websites that are for whole india
"""

def find_website(service, state, dist):

    response = client.models.generate_content(
        model = "gemini-3.5-flash-lite",
        contents = prompt + f"\nService: {service}, \nState: {state}, \nDistrict: {dist}",
    )

    return response.text
    
def chat_bot(response,query):
    prompt = f"""based on the given reponse, you will have to answer query, you can also verify from internet
    just make sure you dont give any invalid or wrong data, answer must be concise and simple in laguage

    answer = {query}
    """
    response = client.models.generate_content(
        model = "gemini-3.5-flash-lite",
        contents = prompt,)
    return response.text