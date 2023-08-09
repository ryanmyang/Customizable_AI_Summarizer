'use client';

import React from 'react';


const CallMainButton: React.FC = () => {
  const handleClick = async () => {
    try {
      const response = await fetch('/api/test-api');
      const data = await response.json();
      console.log(data.response); // Display the response in the console (you can update the state or display it on the UI)
    } catch (error) {
      console.error('Er1ror fetching data:', error);
    }
  };

  return (
    <button onClick={handleClick}>Call Main Function</button>
  );
};

export default CallMainButton;
