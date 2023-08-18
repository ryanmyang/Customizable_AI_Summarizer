// ToastContext.js
import React, { createContext, useContext } from 'react';
import { toast, ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const ToastContext = createContext();

export const useToast = () => {
  return useContext(ToastContext);
};

export const ToastProvider = ({ children }) => {
  const showToast = (message, type) => {
    // Customize the toast options
    const options = {
      type,
      autoClose: 1000, // Adjust the display duration (2 seconds)
      hideProgressBar: true, // Remove the progress bar
    };

    toast(message, options);
  };

  return (
    <ToastContext.Provider value={showToast}>
      {children}
      <ToastContainer position="bottom-right" />
    </ToastContext.Provider>
  );
};
