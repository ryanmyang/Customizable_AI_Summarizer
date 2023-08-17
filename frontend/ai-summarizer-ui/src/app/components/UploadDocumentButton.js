import React, { useState } from 'react';
import { useAuthContext } from '@/context/AuthContext';
import getData from '@/firebase/firestore/getData';
import addData from '@/firebase/firestore/addData';

import Button from '@mui/material/Button';

const UploadFileButton = () => {
  const { user } = useAuthContext();
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files && event.target.files[0];

    if (file) {
      const fileType = file.type;
      if (fileType === 'text/plain') {
        setSelectedFile(file);
      } else {
        alert('Please select a text file.');
      }
    }
  };

  const handleUploadButton = () => {
    console.log('Button Pressed');
    getData('users',user.uid).then(
      data => {console.log(data.result.data())}
    )
    if (selectedFile != null) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const content = event.target.result;
        console.log('content: ' + content);
        uploadDoc(content); // Pass content to the uploadDoc function
      };
      reader.readAsText(selectedFile);
    }
  };

  async function uploadDoc(content) {
    try {
      const userDataPromise = await getData('users', user.uid); 
      const userData = userDataPromise.result.data();
      console.log('User data: ' + userData.next_file);
      const n = userData.next_file;
      await addData(`users/${user.uid}/files`, n, { 
        title: selectedFile.name,
        body: content
      });
      const newN = incrementFileString(n);
      await addData('users', user.uid, { next_file: newN });
    } catch (error) {
      console.error('Error uploading document:', error);
    }
  }

  function incrementFileString(originalString) {
    // Convert the original string to a number and increment
    const incrementedNumber = parseInt(originalString, 10) + 1;

    // Determine the length of the original string
    const originalLength = originalString.length;

    // Format the incremented number with leading zeroes to match the original length
    const formattedIncremented = String(incrementedNumber).padStart(originalLength, '0');

    return formattedIncremented;
  }

  return (
    <div>
      <input
        type="file"
        accept=".txt"
        onChange={handleFileChange}
      />
      {selectedFile && <p>Selected file: {selectedFile.name}</p>}
      <Button variant="contained" onClick={handleUploadButton}>
        Upload
      </Button>
    </div>
  );
};

export default UploadFileButton;
