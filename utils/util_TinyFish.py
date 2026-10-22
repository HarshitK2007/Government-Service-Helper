from tinyfish import TinyFish, BrowserProfile
from dotenv import load_dotenv
from pathlib import Path
import streamlit as st
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

client = TinyFish(api_key=os.getenv("TINYFISH_API_KEY") or st.secrets.get("TINYFISH_API_KEY"))

LABELS = {
    "English": {
        "dept": "Responsible Department",
        "elig": "Eligibility and Criteria",
        "deadline": "Deadline",
        "docs": "Required Documents",
        "steps": "Application Procedure",
        "na": "Information not available on the source website.",
    },
    "Hindi": {
        "dept": "संबंधित विभाग",
        "elig": "पात्रता और मानदंड",
        "deadline": "अंतिम तिथि",
        "docs": "आवश्यक दस्तावेज़",
        "steps": "आवेदन प्रक्रिया",
        "na": "स्रोत वेबसाइट पर जानकारी उपलब्ध नहीं है।",
    },
}

LANG_DESC = {
    "English": "English",
    "Hindi": "Hindi written ONLY in Devanagari script (हिन्दी). "
             "Never use Roman letters or Hinglish for Hindi words.",
}


def build_prompt(lang):
    L = LABELS[lang]
    return f"""
You are an information extraction system for Indian government services.

Extract accurate, practical information about the requested service from the supplied official website.

Write the ENTIRE answer in {LANG_DESC[lang]}
Keep these unchanged (do not translate): URLs, form numbers, official abbreviations,
document IDs (e.g. Aadhaar, PAN), and fee amounts.

Use this exact structure, with these exact headings:

# [Service Name in {lang}]

### {L['dept']}

[Department or government authority]

### {L['elig']}

* [Eligibility requirement]
* [Age, income, or residency requirement, if applicable]
* **{L['deadline']}:** [Application deadline, if specified]

### {L['docs']}

* [Document name]
* [Accepted alternatives or special instructions, if applicable]

### {L['steps']}

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
* If information is unavailable, write "{L['na']}"
* Do not mix requirements from different services.
* Avoid lengthy explanations and unnecessary sections.
* Return only the formatted Markdown. Do not return JSON, code fences, or introductory text.

also make sure to use least least amount of words possible to write answer, and do not i repeat do not use complex words,
reponse must be shortest and with easy language, while maintaining whole context
"""


def ask_tinyfish(url, service, state, dist, lang="English",response_speed=""):
    
    if lang not in LABELS:
        lang = "English"

    final_note = (
        "\n\nIMPORTANT: The website is in English, but your FINAL ANSWER must be written "
        "entirely in Hindi using Devanagari script (e.g. आवेदन करें, not 'aavedan karein'). "
        "Translate all headings, steps and sentences."
        if lang == "Hindi" else ""
    )
    if response_speed == "Lite":
        return client.agent.run(
            goal=build_prompt(lang) + f"\nService = {service}\nState = {state}\nDistrict = {dist}" + final_note,
            url=url,
            browser_profile=BrowserProfile.LITE,
        )
    else:
        return client.agent.run(
            goal=build_prompt(lang) + f"\nService = {service}\nState = {state}\nDistrict = {dist}" + final_note,
            url=url,
            browser_profile=BrowserProfile.STEALTH,
        )
