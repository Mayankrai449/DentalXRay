import React from 'react';
import { motion } from 'framer-motion';
import './RightPanel.css';

const RightPanel = ({ response }) => {
  const variants = {
    initial: { y: -20, opacity: 0 },
    animate: { y: 0, opacity: 1, transition: { duration: 0.5, ease: 'easeOut' } },
    exit: { y: 50, opacity: 0, transition: { duration: 0.3, ease: 'easeIn' } },
  };

  return (
    <motion.div
      className="right-panel"
      variants={variants}
      initial="initial"
      animate="animate"
      exit="exit"
    >
      {response && (
        <div className="report-container">
          <h2 className="report-title">Diagnostic Report</h2>
          <h3 className="section-title">Diagnosis</h3>
          <p className="section-text">{response.diagnostic_report.Diagnosis}</p>
          <h3 className="section-title">Details</h3>
          <ol className="detail-list">
            {response.diagnostic_report.Details.map((detail, index) => (
              <li key={index} className="detail-item">
                <p><strong>Pathology:</strong> {detail.pathology}</p>
                <p><strong>Location:</strong> {detail.location}</p>
              </li>
            ))}
          </ol>
          <h3 className="section-title">Clinical Advice</h3>
          <ul className="advice-list">
            {response.diagnostic_report.ClinicalAdvice.map((advice, index) => (
              <li key={index}>{advice}</li>
            ))}
          </ul>
        </div>
      )}
    </motion.div>
  );
};

export default RightPanel;