from google import genai
import json

client = genai.Client(api_key="AQ.Ab8RN6I2KpRbCrPUp0f9tT9mR6gCvbZqsU3MgjO6Zvii2vitxA")

prompt = f"""
You are an assistant that helps Indian citizens find government services.

User requirements:
- Country: India

Find government services relevant to the user's requirements

Rules:
- Prefer official Indian government websites.
- Never invent URLs.
- If you are unsure whether a URL is official, mark it as unverified.
- Return direct link of the speicifc web where related need is mentioned.
- link1 return in this format and only the link.
- Return only one most legit link.
"""

def find_government_services(service, state, dist=None):

    response = client.models.generate_content(
        model = "gemini-3.5-flash-lite",
        contents = prompt + f"\nService: {service}, \nState: {state}, \nDistrict: {dist or "Not specified"}",
    )

    return response.text
