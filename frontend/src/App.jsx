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