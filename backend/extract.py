import re

def extract_email_and_phone(text: str) -> dict:
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_regex, text, re.IGNORECASE)

    phone_regex = r'\b(?:\+?(\d{1,3}))?[-.\s]?\(?(?:(\d{3})\)?[-.\s]?)?(\d{3})[-.\s]?(\d{4})\b'
    phones = re.findall(phone_regex, text)
    formatted_phones = [''.join(filter(None, phone)) for phone in phones]

    return {"emails": emails, "phones": formatted_phones}