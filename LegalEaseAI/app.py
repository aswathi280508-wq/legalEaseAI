import os
import io
import textwrap
import requests
import streamlit as st

from docx import Document
from fpdf import FPDF
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)


# Streamlit page configuration
st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


# Title
st.title("⚖️ LegalEase")

st.subheader(
    "AI-Powered Legal Document Generator"
)

st.write(
    "Create customizable legal documents using AI."
)


# Document type
document_type = st.selectbox(
    "Select Document Type",
    [
        "Employment Contract",
        "NDA",
        "Residential Lease"
    ]
)


# Parties
parties = st.text_area(
    "Parties",
    placeholder=(
        "Example: Employer: ABC Company; "
        "Employee: John"
    ),
    height=120
)


# Terms
terms = st.text_area(
    "Terms",
    placeholder=(
        "Enter the important terms separated by semicolons"
    ),
    height=120
)


# Effective date
effective_date = st.date_input(
    "Effective Date"
)


# Generate button
if st.button(
    "Generate Document",
    type="primary"
):

    # Validate parties
    if not parties.strip():
        st.warning(
            "Please enter the parties."
        )
        st.stop()

    # Validate terms
    if not terms.strip():
        st.warning(
            "Please enter the terms."
        )
        st.stop()

    # API payload
    payload = {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "effective_date": str(effective_date)
    }

    try:

        # Call FastAPI backend
        with st.spinner(
            "Generating legal document..."
        ):

            response = requests.post(
                f"{BACKEND_URL}/generate",
                json=payload,
                timeout=120
            )

        # Successful response
        if response.status_code == 200:

            data = response.json()

            # Get generated document
            document_text = data.get(
                "document",
                data.get(
                    "content",
                    ""
                )
            )

            # Check empty response
            if not document_text.strip():

                st.error(
                    "Backend returned an empty document."
                )

                st.stop()

            # Success message
            st.success(
                "Document generated successfully!"
            )

            # Document preview
            st.subheader(
                "Document Preview"
            )

            # Editable document
            edited_document = st.text_area(
                "Edit your document",
                value=document_text,
                height=500
            )

            # ==================================================
            # TXT DOWNLOAD
            # ==================================================

            st.download_button(
                "Download TXT",
                data=edited_document,
                file_name="LegalEase_document.txt",
                mime="text/plain"
            )

            # ==================================================
            # DOCX DOWNLOAD
            # ==================================================

            doc = Document()

            for line in edited_document.split("\n"):
                doc.add_paragraph(line)

            docx_buffer = io.BytesIO()

            doc.save(docx_buffer)

            docx_buffer.seek(0)

            st.download_button(
                "Download DOCX",
                data=docx_buffer.getvalue(),
                file_name="LegalEase_document.docx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                )
            )

            # ==================================================
            # PDF DOWNLOAD
            # ==================================================

            pdf = FPDF()

            pdf.set_auto_page_break(
                auto=True,
                margin=15
            )

            pdf.add_page()

            pdf.set_font(
                "Arial",
                size=12
            )

            for line in edited_document.split("\n"):

                if not line.strip():
                    pdf.ln(5)
                    continue

                # Convert unsupported Unicode characters
                clean_line = line.encode(
                    "latin-1",
                    "replace"
                ).decode(
                    "latin-1"
                )

                clean_line = " ".join(
                    clean_line.split()
                )

                wrapped_lines = textwrap.wrap(
                    clean_line,
                    width=80,
                    break_long_words=True,
                    break_on_hyphens=False
                )

                for wrapped_line in wrapped_lines:

                    pdf.multi_cell(
                        pdf.epw,
                        8,
                        wrapped_line,
                        new_x="LMARGIN",
                        new_y="NEXT"
                    )

            pdf_bytes = bytes(
                pdf.output()
            )

            st.download_button(
                "Download PDF",
                data=pdf_bytes,
                file_name="LegalEase_document.pdf",
                mime="application/pdf"
            )

        # Backend error
        else:

            st.error(
                f"Backend error: {response.status_code}"
            )

            st.code(
                response.text
            )

    # Backend connection error
    except requests.exceptions.ConnectionError:

        st.error(
            "Cannot connect to LegalEase backend. "
            "Please make sure FastAPI is running on "
            "http://127.0.0.1:8000"
        )

    # Timeout error
    except requests.exceptions.Timeout:

        st.error(
            "Backend request timed out. "
            "Please check whether the FastAPI server "
            "and Gemini API are running correctly."
        )

    # Other errors
    except Exception as e:

        st.error(
            f"Error: {e}"
        )