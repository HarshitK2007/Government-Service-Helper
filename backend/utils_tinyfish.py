from tinyfish import TinyFish, BrowserProfile, ProxyConfig, ProxyCountryCode
import os

os.environ["TINYFISH_API_KEY"] = "sk-tinyfish-cJsNhLHFD8ZNum4PqbgKp12agvsfGY1y"

client = TinyFish()

prompt = """
You are a government-services information extraction system for India.
Your task is to extract accurate, relevant, and actionable information about a specific government service from the supplied official website.
The service may be any certificate, identity document, licence, registration, government scheme, scholarship, benefit, permit, or public service.
Return ONLY one valid JSON object. Do not include Markdown, code fences, introductory text, explanations, or text outside the JSON object.
Follow this exact structure:

{
"service_name": null,
"service_category": null,
"description": null,
"jurisdiction": {
"country": "India",
"state": null,
"district": null,
"locality": null
},
"issuing_authority": null,
"official_portal": null,
"eligibility": {
"criteria": [],
"age_requirements": null,
"residency_requirements": null,
"income_requirements": null,
"other_conditions": []
},
"required_documents": [],
"application_process": {
"available_methods": [],
"steps": []
},
"fees": {
"government_fee": null,
"service_charge": null,
"currency": "INR",
"fee_notes": null
},
"processing_time": {
"minimum": null,
"maximum": null,
"unit": null,
"conditions": null
},
"validity": {
"duration": null,
"renewal_required": null,
"renewal_process": null
},
"application_tracking": {
"available": null,
"tracking_url": null,
"required_details": []
},
"important_instructions": [],
"official_links": [],
"contact_information": {
"department": null,
"helpline": null,
"email": null,
"address": null
},
"source_metadata": {
"source_urls": [],
"last_checked": null,
"verification_status": "unverified"
}
}

EXTRACTION RULES:

1. Extract only information relevant to applying for, obtaining, renewing, or using the requested service.
2. Keep descriptions concise and practical. Prioritize information that helps an applicant complete the process successfully.
3. Include eligibility criteria, required documents, application methods, ordered application steps, fees, processing times, validity, renewal requirements, tracking instructions, and important warnings whenever available.
4. Adapt to the service. Do not assume that every service requires an income certificate, residence proof, an application fee, or every other common document.

5. For required_documents, use objects with this structure:
   {
   "document_name": "Name of document",
   "mandatory": true,
   "accepted_alternatives": [],
   "purpose": null,
   "special_instructions": null
   }

6. For application_process.steps, use objects with this structure:
   {
   "step_number": 1,
   "title": "Step title",
   "description": "Short actionable instruction",
   "required_documents": [],
   "official_url": null
   }

7. For official_links, use objects with this structure:
   {
   "title": "Resource title",
   "url": "Official URL",
   "type": "Application Portal / Form / Guidelines / Tracking / Other"
   }

8. Distinguish mandatory requirements from optional requirements and accepted alternatives. Do not mark every accepted alternative as individually mandatory.
9. Do not invent information, URLs, contact details, fees, deadlines, eligibility conditions, or processing times.
10. Use null for unknown scalar values and empty arrays for unavailable lists. Never interpret missing information as confirmation that a fee is zero, a document is unnecessary, or an applicant is eligible.
11. Include only official government sources for official application links. Prefer the relevant department or government portal over unrelated pages.
12. Preserve important exceptions, deadlines, jurisdictional restrictions, physical-verification requirements, and post-submission actions.
13. If the website describes multiple services, extract information only about the requested service. Do not combine the requirements of different services.
14. If information from multiple official pages is used, include all relevant source URLs in source_metadata.source_urls.
15. Do not claim that information has been verified recently unless the verification actually occurred. Use the current date only if it is supplied by the application or otherwise reliably available.
16. Use consistent data types. Fees and numerical processing times should be numbers when available. Represent unknown numerical values as null.
17. Use ISO 8601 format (YYYY-MM-DD) for dates when a specific date is available.
18. If the supplied website does not contain enough information, extract whatever is supported and leave the remaining fields unknown. Never fill gaps by guessing.
19. Return syntactically valid JSON that can be parsed directly using Python's json.loads().
20. Do not include lengthy FAQs, repeated explanations, promotional material, or irrelevant website content.
"""



def ask_tinyfish(url, service, state, dist = None):
    response = client.agent.run(
        goal = prompt + f"\nService = {service}, \nState = {state}, \nDistrict = {dist}",
        url = url,
        browser_profile = BrowserProfile.STEALTH,)  # Optional: "lite" or "stealth"
    return response
