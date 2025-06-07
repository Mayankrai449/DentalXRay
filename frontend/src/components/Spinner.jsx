import React from 'react';
import { motion } from 'framer-motion';
import './Spinner.css';

const Spinner = ({ message }) => {
  const variants = {
    initial: { y: 100, opacity: 0 },
    animate: { y: 0, opacity: 1, transition: { duration: 0.5, ease: 'easeOut' } },
    exit: { y: -50, opacity: 0, transition: { duration: 0.3, ease: 'easeIn' } },
  };

  return (
    <motion.div
      className="spinner-container"
      variants={variants}
      initial="initial"
      animate="animate"
      exit="exit"
    >
      <div className="spinner"></div>
      <p className="spinner-text">{message}</p>
    </motion.div>
  );
};

export default Spinner;