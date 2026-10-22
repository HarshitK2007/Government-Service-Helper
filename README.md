# Government Service Helper 🇮🇳

### Making government services easier to understand, one search at a time.   

Finding the right government website is only half the problem. Even after reaching the correct portal, people may struggle to understand eligibility rules, required documents, application steps, and which department handles their request.

**Government Service Helper** is a Streamlit-based project developed by our team to make this process simpler. Users enter the government service they need, select their state and district, and get a structured explanation of relevant service information from a government website.

Built for **AZINHACK '26**, this project combines Gemini-powered website discovery with TinyFish-powered web browsing and information extraction.

---

## 💡 The Problem

Government services in India are spread across different central, state, and local portals. Finding the correct page can take time, and important information is not always easy to understand at first glance.

A person looking for a service may need to figure out:

- Which website should they be visiting?
- Which department is responsible?
- Who is eligible to apply?
- Which documents are required?
- What steps should they follow?

Our team wanted to explore how AI and web automation could help bring these details together in one place.

## 🚀 What the Project Does

The current application follows a simple workflow:

1. **Enter a service:** The user types the government service they are looking for.
2. **Choose a location:** The user selects their state and district.
3. **Find a relevant website:** The application checks its saved URL data first. If no match is found, it asks Gemini to identify a relevant government website.
4. **Read the website with TinyFish:** TinyFish browses the selected page and attempts to extract information relevant to the requested service.
5. **Display structured information:** The extracted information is presented in Markdown, covering the responsible department, eligibility, required documents, and application procedure where the source provides those details.

The goal is to reduce the effort required to go from searching for a service to understanding where to start.

## 🧠 How Gemini and TinyFish Work Together

Both tools have different responsibilities in this project.

### Gemini — Website Discovery

The Google Gemini API helps identify a relevant website based on the requested service and the selected location.

The prompt instructs Gemini to prefer official or officially authorized portals and return `NOT_FOUND` when a suitable website cannot be verified.

### TinyFish — Web Browsing and Extraction

TinyFish is used to browse the selected website and extract useful information from its content.

The extraction prompt requests a structured response containing:

- Service name
- Responsible department
- Eligibility and criteria
- Required documents
- Application procedure
- Relevant source links

The prompt also instructs the agent not to invent requirements, deadlines, fees, documents, or URLs.

**Why use both?** Website discovery and information extraction are separate tasks. Gemini helps find a relevant starting point, while TinyFish handles the browsing and extraction step.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | User interface |
| Google Gemini API | Government website discovery |
| TinyFish SDK | Website browsing and information extraction |
| JSON | State/district data and saved website mappings |
| python-dotenv | Local environment-variable configuration |

## 📁 Project Structure

```text
Government-Service-Helper/
│
├── main.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── StateAndDistrict.json
│   └── government_urls.json
│
└── utils/
    ├── __init__.py
    ├── util_Google.py
    ├── util_StateDist.py
    ├── util_TinyFish.py
    └── util_UrlManager.py
```

### What each file does

- `main.py` — Runs the Streamlit interface and coordinates the search workflow.
- `util_Google.py` — Uses Gemini to discover a relevant government website.
- `util_TinyFish.py` — Sends the website and extraction instructions to TinyFish.
- `util_StateDist.py` — Loads the state and district data.
- `util_UrlManager.py` — Retrieves and saves website mappings in a local JSON file.
- `StateAndDistrict.json` — Provides the location options shown in the interface.
- `government_urls.json` — Stores previously saved website mappings to avoid repeating some discovery requests.

## 🔍 Example Use Case

Imagine someone wants to learn about applying for a PAN card.

They enter `PAN card`, select their state and district, and search. The application attempts to find a relevant website, uses TinyFish to read the selected page, and displays the available service information in a structured format.

The same workflow can be tried with other services, provided a suitable website can be found and accessed.

*The result depends on the website returned, the information available on that page, and the success of the API calls.*

## 🌱 Current Scope and Future Improvements

This is a project in development, and our team sees several opportunities to improve its reliability and usefulness:

- Better validation of government website URLs before using or saving them.
- More reliable handling of unavailable websites and failed API requests.
- Clearer source attribution so users can easily verify extracted information.
- Support for multiple relevant official sources when one page does not contain everything.
- Improved handling of different spellings and names for the same service.
- A more accessible interface for people who are not comfortable navigating complex portals.
- Deployment with secure API-key management and persistent storage.

## 🔐 Responsible Use

Government-service information can affect important decisions. This application is intended to help users discover and understand information, not to replace government authorities or official application portals.

AI-extracted information may be incomplete or outdated. Users should verify important details directly with the relevant government department before acting on them.

The application does not claim to submit applications or guarantee eligibility.

## 👥 About the Project

Government Service Helper was developed by our team to explore how AI-powered website discovery and browser automation can make public-service information easier to navigate.

Our focus is on a practical problem: helping people find relevant information without having to manually search through multiple pages first.

**Built for AZINHACK '26 — Open Innovation**
