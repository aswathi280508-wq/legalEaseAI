import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ LegalEase")
st.subheader("AI-Powered Legal Document Generator")

st.write(
    "Create customizable legal documents using AI."
)

document_type = st.selectbox(
    "Select Document Type",
    [
        "Employment Contract",
        "NDA",
        "Residential Lease"
    ]
)

parties = st.text_area(
    "Parties",
    placeholder="Example: Employer: ABC Company; Employee: John"
)

terms = st.text_area(
    "Terms",
    placeholder="Enter the important terms separated by semicolons"
)

effective_date = st.date_input(
    "Effective Date"
)

if st.button("Generate Document", type="primary"):

    if not parties.strip():
        st.warning("Please enter the parties.")
        st.stop()

    if not terms.strip():
        st.warning("Please enter the terms.")
        st.stop()

    payload = {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "effective_date": str(effective_date)
    }

    try:
        with st.spinner("Generating legal document..."):

            response = requests.post(
                f"{BACKEND_URL}/generate",
                json=payload,
                timeout=120
            )

        if response.status_code == 200:

            data = response.json()

            document_text = data.get(
                "document",
                data.get("content", "")
            )

            st.success("Document generated successfully!")

            st.subheader("Document Preview")

            edited_document = st.text_area(
                "Edit your document",
                value=document_text,
                height=500
            )

            st.download_button(
                "Download TXT",
                edited_document,
                file_name="LegalEase_document.txt",
                mime="text/plain"
            )

        else:
            st.error(
                f"Backend error: {response.status_code}"
            )
            st.code(response.text)

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to LegalEase backend. "
            "Please make sure FastAPI is running on "
            "http://127.0.0.1:8000"
        )

    except Exception as e:
        st.error(f"Error: {e}")