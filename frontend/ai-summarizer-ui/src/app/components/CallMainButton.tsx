'use client';

import React from 'react';


const CallMainButton: React.FC = () => {
  const handleClick = async () => {
    try {
      const response = await fetch('/api/');
      const data = await response.json();
      console.log(data); // Display the response in the console (you can update the state or display it on the UI)
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <button onClick={handleClick}>Call Test Function</button>
  );
};

export default CallMainButton;
