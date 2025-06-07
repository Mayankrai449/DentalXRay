import React from 'react';
import { motion } from 'framer-motion';
import './LeftPanel.css';

const LeftPanel = ({ response, error, fileName }) => {
  const variants = {
    initial: { y: -20, opacity: 0 },
    animate: { y: 0, opacity: 1, transition: { duration: 0.5, ease: 'easeOut' } },
    exit: { y: 50, opacity: 0, transition: { duration: 0.3, ease: 'easeIn' } },
  };

  return (
    <motion.div
      className="left-panel"
      variants={variants}
      initial="initial"
      animate="animate"
      exit="exit"
    >
      {error && <p className="error-text">{error}</p>}
      {response && (
        <div className="image-container">
          <img
            src={`data:image/jpeg;base64,${response.image}`}
            alt=""
            className="annotated-image"
          />
          <p className="image-caption">{fileName}</p>
        </div>
      )}
    </motion.div>
  );
};

export default LeftPanel;
