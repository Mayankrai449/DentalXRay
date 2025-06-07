import React from 'react';
import './UploadSection.css';

const UploadSection = ({ handleFileChange, triggerFileInput, loading }) => (
  <div className="upload-section">
    <input
      type="file"
      onChange={handleFileChange}
      className="file-input"
      id="fileInput"
      accept=".dcm,.rvg,image/*"
    />
    <button
      onClick={triggerFileInput}
      className="upload-button"
      disabled={loading}
    >
      Upload
    </button>
  </div>
);

export default UploadSection;