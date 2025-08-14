from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from extract import extract_email_and_phone

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextData(BaseModel):
    text: str

@app.post("/extract")
async def extract_data(data: TextData):
    if not data.text.strip():
        raise HTTPException(status_code=400, detail="No text provided")
    return extract_email_and_phone(data.text)