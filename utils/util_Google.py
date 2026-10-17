from google import genai
from dotenv import load_dotenv
from pathlib import Path
import streamlit as st
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

client = genai.Client(api_key = os.getenv("GOOGLE_GEMINI_API_KEY") or st.secrets.get("GOOGLE_GEMINI_API_KEY"))

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
"""

def find_website(service, state, dist=None):

    response = client.models.generate_content(
        model = "gemini-3.5-flash-lite",
        contents = prompt + f"\nService: {service}, \nState: {state}, \nDistrict: {dist or 'Not specified'}",
    )

    return response.text
