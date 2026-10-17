from tinyfish import TinyFish, BrowserProfile
from dotenv import load_dotenv
from pathlib import Path
import streamlit as st
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

client = TinyFish(api_key = os.getenv("TINYFISH_API_KEY") or st.secrets.get("TINYFISH_API_KEY"))

prompt = """
You are an information extraction system for Indian government services.

Extract accurate, practical information about the requested service from the supplied official website.

Return the result in **Markdown format**, ready to display directly using Streamlit's `st.markdown()`.

Use this exact structure:

# [Service Name]

### Responsible Department

[Department or government authority]

### Eligibility and Criteria

* [Eligibility requirement]
* [Age, income, or residency requirement, if applicable]
* **Deadline:** [Application deadline, if specified]

### Required Documents

* [Document name]
* [Accepted alternatives or special instructions, if applicable]

### Application Procedure

1. [First action]
2. [Second action]
3. [Continue in the correct order until completion]

Rules:

* Use simple language and short sentences.
* Include only information relevant to the requested service.
* Use only information supported by official sources.
* Never invent eligibility requirements, deadlines, documents, fees, or URLs.
* Include a deadline only when one is explicitly specified. Otherwise, omit it.
* List only required documents. Clearly label conditional documents and accepted alternatives.
* Include online and offline procedures only when officially documented.
* Add relevant official website links using Markdown link syntax: [Link text](URL).
* Include links beside the relevant application steps whenever possible.
* If information is unavailable, write "Information not available on the source website."
* Do not mix requirements from different services.
* Avoid lengthy explanations and unnecessary sections.
* Return only the formatted Markdown. Do not return JSON, code fences, or introductory text.
* Ensure the output is ready to pass directly into Streamlit's `st.markdown()`.
"""


def ask_tinyfish(url, service, state, dist = None):
    response = client.agent.run(
        goal = prompt + f"\nService = {service}, \nState = {state}, \nDistrict = {dist}",
        url = url,
        browser_profile = BrowserProfile.STEALTH,)  # Optional: "lite" or "stealth"
    return response
