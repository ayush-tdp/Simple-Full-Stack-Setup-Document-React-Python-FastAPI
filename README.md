# React + Python + FastAPI

A simple full-stack app that takes text input, extracts **emails** and **phone numbers** using regex, and displays the results.

* **Frontend**: React (Vite)
* **Backend**: FastAPI (Python)

---

## 🚀 Quick Start

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/react-python.git
cd react-python
```

---

## 🖥 Backend Setup (FastAPI)

```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1   # On Windows PowerShell

# Add dependencies
echo fastapi[standard] >> requirements.txt
echo uvicorn >> requirements.txt

pip install -r requirements.txt
```

**`extract.py`**

```python
import re

def extract_email_and_phone(text: str) -> dict:
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_regex, text, re.IGNORECASE)

    phone_regex = r'\b(?:\+?(\d{1,3}))?[-.\s]?\(?(?:(\d{3})\)?[-.\s]?)?(\d{3})[-.\s]?(\d{4})\b'
    phones = re.findall(phone_regex, text)
    formatted_phones = [''.join(filter(None, phone)) for phone in phones]

    return {"emails": emails, "phones": formatted_phones}
```

**`main.py`**

```python
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
```

**Run Backend**

```bash
uvicorn main:app --reload
```

Backend runs at: **[http://localhost:8000](http://localhost:8000)**

---

## 🌐 Frontend Setup (React + Vite)

```bash
cd ../frontend
npm create vite@latest . --template react
npm install
npm install axios
```

**`src/App.jsx`**

```jsx
import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [emails, setEmails] = useState([]);
  const [phones, setPhones] = useState([]);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    try {
      const res = await axios.post('http://localhost:8000/extract', { text: inputText });
      setEmails(res.data.emails);
      setPhones(res.data.phones);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error processing data');
    }
  };

  return (
    <div className="App">
      <h1>Text Extractor</h1>
      <textarea
        rows="10"
        cols="50"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Enter text here..."
      />
      <br />
      <button onClick={handleSubmit}>Extract Emails & Phones</button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <h2>Emails:</h2>
      <ul>{emails.map((email, i) => <li key={i}>{email}</li>)}</ul>
      <h2>Phones:</h2>
      <ul>{phones.map((phone, i) => <li key={i}>{phone}</li>)}</ul>
    </div>
  );
}

export default App;
```

**Run Frontend**

```bash
npm run dev
```

Frontend runs at: **[http://localhost:5173](http://localhost:5173)**

---

## 📌 How to Run

Open **two terminals**:

**Terminal 1 (Backend)**

```bash
cd backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

**Terminal 2 (Frontend)**

```bash
cd frontend
npm run dev
```

---

## 🧪 Test

1. Visit **[http://localhost:5173](http://localhost:5173)**
2. Enter:

   ```
   Contact: test@example.com, +1 234 567 8901
   ```
3. Click **Extract Emails & Phones**
4. Results will be displayed below.

---

## 🌍 Hosting Guide — Backend on Render & Frontend on Vercel

This setup uses:

* **Backend (FastAPI)** → Render (Free tier)
* **Frontend (React + Vite)** → Vercel (Free tier)

---

### **1️⃣ Hosting the Backend on Render**

#### Step 1 — Prepare Backend

* Inside `backend/requirements.txt` make sure you have:

  ```txt
  fastapi[standard]
  uvicorn
  ```
* Your backend **must bind to** `0.0.0.0` and use the `$PORT` environment variable.
  In Render’s Start Command, we’ll set:

  ```bash
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

---

#### Step 2 — Push Backend to GitHub

* Commit and push your backend code to GitHub.
* You can keep frontend and backend in the same repo, but Render will only use the `backend` folder.

---

#### Step 3 — Deploy to Render

1. Go to [Render](https://render.com/).
2. **Create New → Web Service**.
3. Connect your GitHub repo.
4. Settings:

   * **Root Directory** → `backend`
   * **Environment** → Python
   * **Build Command** → (leave blank, Render will auto-install from `requirements.txt`)
   * **Start Command** →

     ```bash
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
5. Click **Create Web Service**.
6. Wait until the deployment finishes — Render will give you a live URL:

   ```
   https://your-backend.onrender.com
   ```

---

### **2️⃣ Hosting the Frontend on Vercel**

#### Step 1 — Update API URL

* In `frontend/src/App.jsx`, replace:

  ```javascript
  const response = await axios.post('http://localhost:8000/extract', { text: inputText });
  ```

  with:

  ```javascript
  const response = await axios.post('https://your-backend.onrender.com/extract', { text: inputText });
  ```

---

#### Step 2 — Push Frontend to GitHub

* Commit and push the `frontend` folder to GitHub (can be same repo as backend).

---

#### Step 3 — Deploy to Vercel

1. Go to [Vercel](https://vercel.com/).
2. Click **Add New → Project**.
3. Import your GitHub repo.
4. Select the `frontend` folder as the root.
5. Build settings:

   * **Framework Preset** → `Vite`
   * **Build Command** → `npm run build`
   * **Output Directory** → `dist`
6. Click **Deploy**.

---

#### Step 4 — Test the Full App

* Visit your **Vercel frontend URL** (e.g. `https://your-frontend.vercel.app`)
* Enter some text containing emails & phone numbers.
* Click **Extract** → data should come from the **Render backend**.

---
