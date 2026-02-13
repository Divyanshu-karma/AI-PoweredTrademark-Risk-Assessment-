import os
import json
import streamlit as st
import pdfplumber
import requests
from dotenv import load_dotenv

# Load Groq API key
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Constants
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"

# Streamlit setup
st.set_page_config(page_title="Trademark Input Processor (Groq)", layout="wide")
st.title("📑 AI Trademark Converter — Powered by Groq")
st.markdown("Converts Trademark PDF → Structured JSON with Groq LLM")

# ----------------------------
# PDF TEXT EXTRACTION (UNCHANGED)
# ----------------------------
def extract_text_from_pdf(uploaded_file):
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

# ----------------------------
# STRUCTURED OBJECT
# ----------------------------
class TrademarkApplication:
    def __init__(self, data: dict):
        self.mark = data["mark_info"]["literal"]
        self.mark_type = data["mark_info"]["type"]
        self.register = data["mark_info"]["register"]

        self.filing_basis = data["filing_basis"]["basis_type"]
        self.use_in_commerce = data["filing_basis"]["use_in_commerce"]

        self.classes = [g["class_id"] for g in data["goods_and_services"]]
        self.goods_map = {
            g["class_id"]: g["description"]
            for g in data["goods_and_services"]
        }

        self.owner_name = data["owner"]["name"]
        self.owner_entity = data["owner"]["entity"]
        self.owner_citizenship = data["owner"]["citizenship"]

        self.serial_number = data["identifiers"]["serial_number"]
        self.registration_number = data["identifiers"]["registration_number"]

        self.specimen_provided = data["specimen"]["provided"]
        self.disclaimer_text = data["disclaimer"]["text"]

    def to_dict(self):
        return self.__dict__

# ----------------------------
# CALL GROQ
# ----------------------------
def call_groq_llm(raw_text):

    system_prompt = f"""
You are a legal data extraction assistant.

Task: Analyze the following Trademark Document text and extract the specific details into a JSON object according to the TARGET JSON STRUCTURE.

STRICT RULES:
1. Return ONLY valid JSON. No markdown, no explanations.
2. Do NOT include any fields outside TARGET JSON STRUCTURE.
3. Use null if any field is not found.
4. Format ALL dates as YYYY-MM-DD where possible.

TARGET JSON STRUCTURE:
{{
  "mark_info": {{
    "literal": "",
    "type": "",
    "register": ""
  }},
  "filing_basis": {{
    "basis_type": "",
    "use_in_commerce": null
  }},
  "goods_and_services": [
    {{
      "class_id": "",
      "description": ""
    }}
  ],
  "owner": {{
    "name": "",
    "entity": "",
    "citizenship": ""
  }},
  "dates": {{
    "filing_date": "",
    "first_use": "",
    "first_use_in_commerce": ""
  }},
  "identifiers": {{
    "serial_number": "",
    "registration_number": ""
  }},
  "mark_features": {{
    "is_standard_character": null,
    "is_design_mark": null,
    "contains_color_claim": null,
    "translation_statement": null,
    "transliteration_statement": null
  }},
  "disclaimer": {{
    "present": null,
    "text": null
  }},
  "specimen": {{
    "provided": null,
    "description": null,
    "type": null
  }},
  "claimed_prior_registrations": []
}}

TRADEMARK DOCUMENT TEXT:
{raw_text}
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt}
        ],
        "max_tokens": 2048,
        "temperature": 0.1
    }

    response = requests.post(GROQ_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return None, f"API Error {response.status_code}: {response.text}"

    try:
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        return content, None
    except Exception as e:
        return None, f"Parsing Error: {e}"

# ----------------------------
# STREAMLIT UI


uploaded_file = st.file_uploader("Upload Trademark PDF", type=["pdf"])

if uploaded_file:
    raw_text = extract_text_from_pdf(uploaded_file)

    if raw_text:
        with st.expander("📄 Raw Extracted Text"):
            st.text(raw_text)

        # Step 1: Generate JSON
        if st.button("Generate Logical JSON"):
            with st.spinner("Calling Groq LLM..."):
                llm_output, error = call_groq_llm(raw_text)

                if error:
                    st.error(error)
                else:
                    try:
                        parsed_json = json.loads(llm_output)

                        # Save to session state
                        st.session_state["parsed_json"] = parsed_json

                        st.success("✅ JSON Parsed Successfully")
                        st.json(parsed_json)

                        st.download_button(
                            "Download JSON",
                            data=json.dumps(parsed_json, indent=2),
                            file_name="logical_input.json",
                            mime="application/json"
                        )

                    except json.JSONDecodeError:
                        st.error("Invalid JSON from model output")
                        st.code(llm_output)

        # Step 2: Run RAG (only if JSON exists)
        if "parsed_json" in st.session_state:
            if st.button("Run Risk Analysis"):

                with st.spinner("Running RAG Analysis..."):
                    try:
                        response = requests.post(
                            "http://127.0.0.1:8000/analyze",
                            json={"data": st.session_state["parsed_json"]},
                            timeout=60
                        )

                        if response.status_code == 200:
                            result = response.json()

                            st.subheader("📊 RAG Risk Analysis")
                            st.write(result["analysis"])

                        else:
                            st.error(f"Backend Error: {response.text}")

                    except Exception as e:
                        st.error(f"Connection Error: {str(e)}")

    else:
        st.warning("No text extracted — PDF may be scanned images.")
