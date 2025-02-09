import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [coverImage, setCoverImage] = useState(null); // For embedding
  const [stegoImage, setStegoImage] = useState(null); // For retrieving
  const [text, setText] = useState('');
  const [stegoImageUrl, setStegoImageUrl] = useState(null);
  const [extractedText, setExtractedText] = useState('');

  const handleEmbed = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('image', coverImage); // Use coverImage for embedding
    formData.append('text', text);

    try {
      const response = await axios.post('http://localhost:5000/embed', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      setStegoImageUrl(url); // Set the stego image URL
    } catch (error) {
      console.error('Error embedding text:', error);
    }
  };

  const handleRetrieve = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('stego_image', stegoImage); // Use stegoImage for retrieving

    try {
      const response = await axios.post('http://localhost:5000/retrieve', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setExtractedText(response.data.text); // Set the extracted text
    } catch (error) {
      console.error('Error retrieving text:', error);
    }
  };

  return (
    <div className="App">
      <h1>Steganography App</h1>

      {/* Embed Section */}
      <form onSubmit={handleEmbed}>
        <h2>Embed Text</h2>
        <input
          type="file"
          onChange={(e) => setCoverImage(e.target.files[0])} // Set coverImage
          required
        />
        <input
          type="text"
          placeholder="Enter text to embed"
          value={text}
          onChange={(e) => setText(e.target.value)}
          required
        />
        <button type="submit">Embed Text</button>
      </form>

      {stegoImageUrl && (
        <div>
          <h2>Stego Image</h2>
          <img src={stegoImageUrl} alt="Stego" width="300" />
          <a href={stegoImageUrl} download="stego_image.png">Download Stego Image</a>
        </div>
      )}

      {/* Retrieve Section */}
      <form onSubmit={handleRetrieve}>
        <h2>Retrieve Text</h2>
        <input
          type="file"
          onChange={(e) => setStegoImage(e.target.files[0])} // Set stegoImage
          required
        />
        <button type="submit">Retrieve Text</button>
      </form>

      {extractedText && (
        <div>
          <h2>Extracted Text</h2>
          <p>{extractedText}</p>
        </div>
      )}
    </div>
  );
}

export default App;