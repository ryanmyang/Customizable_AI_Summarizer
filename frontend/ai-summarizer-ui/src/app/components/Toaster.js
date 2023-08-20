import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export const showToastSuccess = (message, type = 'success') => {
  // Customize the toast options
  const options = {
    type,
    autoClose: 1000, // Adjust the display duration (2 seconds)
    hideProgressBar: true, // Remove the progress bar
  };

  toast(message, options);
};

export const showToastError = (message, type = 'error') => {
    // Customize the toast options
    const options = {
      type,
      autoClose: 1000, // Adjust the display duration (2 seconds)
      hideProgressBar: false, // Remove the progress bar
    };
  
    toast(message, options);
  };

  export const showToastInfo = (message, type = 'info') => {
    // Customize the toast options
    const options = {
      type,
      autoClose: 1000, // Adjust the display duration (2 seconds)
      hideProgressBar: true, // Remove the progress bar
    };
  
    toast(message, options);
  };