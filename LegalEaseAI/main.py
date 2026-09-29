from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="LegalEase API",
    description="AI-Powered Legal Document Generator",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    effective_date: str


@app.get("/")
def root():
    return {
        "message": "Welcome to LegalEase API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/generate")
def generate_document(request: DocumentRequest):

    document = f"""
{request.document_type.upper()}

Effective Date: {request.effective_date}

PARTIES
{request.parties}

TERMS AND CONDITIONS
{request.terms}

AGREEMENT

This document is prepared based on the information provided by
the user.

The parties agree to the terms and conditions stated above.

This document is intended as a generated draft for review.
Users should review the document carefully before using it
for any legal purpose.
"""

    return {
        "success": True,
        "document": document
    }