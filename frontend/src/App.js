import React, { useState } from 'react';
import './App.css';
import Navbar from './components/Navbar';
import LeftPanel from './components/LeftPanel';
import RightPanel from './components/RightPanel';
import UploadSection from './components/UploadSection';
import Spinner from './components/Spinner';
import api from './api';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState(null);
  const [error, setError] = useState(null);
  const [showPlaceholder, setShowPlaceholder] = useState(true);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      handleUpload(selectedFile);
    }
  };

  const handleUpload = async (selectedFile) => {
    setLoading(true);
    setError(null);
    setShowPlaceholder(false);

    setMessage('uploading...');
    const timer1 = setTimeout(() => setMessage('getting annotations...'), 1000);
    const timer2 = setTimeout(() => setMessage('generating report...'), 3000);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const res = await api.post('/detect/', formData);
      setResponse(res.data);
    } catch (err) {
      setError('An error occurred while processing the image.');
    } finally {
      setLoading(false);
      clearTimeout(timer1);
      clearTimeout(timer2);
    }
  };

  const triggerFileInput = () => {
    document.getElementById('fileInput').click();
  };

  return (
    <div className="app-container">
      <Navbar />
      <div className="main-content">
        {showPlaceholder && !loading && !response && !error && (
          <div className="placeholder-container">
            <p className="placeholder-text">Upload your dentals for AI powered diagnosis</p>
          </div>
        )}
        {(response || error) && !loading && (
          <div className="panels-container">
            <LeftPanel response={response} error={error} fileName={file ? file.name : ''} />
            <RightPanel response={response} />
          </div>
        )}
        {loading && <Spinner message={message} />}
        <UploadSection
          handleFileChange={handleFileChange}
          triggerFileInput={triggerFileInput}
          loading={loading}
        />
      </div>
    </div>
  );
}

export default App;