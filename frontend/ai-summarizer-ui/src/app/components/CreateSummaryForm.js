'use client';
import React, { useState } from "react";
import { useAuthContext } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import UploadFileButton from "@/app/components/UploadDocumentButton";
import PageContainer from '@/app/components/PageContainer';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import { Typography } from "@mui/material";
import { useToast } from './ToastContext';

const CreateSummaryForm = () => {
const { user } = useAuthContext()
const router = useRouter()
  const [selectedFile, setSelectedFile] = useState(null);
  const showToast = useToast();

  const handleFileChange = (event) => {
    const file = event.target.files && event.target.files[0];

    if (file) {
      const fileType = file.type;
      if (fileType === 'text/plain') {
        setSelectedFile(file);
      } else {
        showToast('Please upload a text file', 'error');
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
      showToast('Document Uploaded', 'success');
      setSelectedFile(null);
    } catch (error) {
      showToast('Upload Error', 'error');
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

    React.useEffect(() => { 
        if (user == null) router.push("/")
    }, [user])
    console.log("User ID: "+user['uid']);
    console.log(user);

    const [extractions, setExtractions] = useState(3); // Default value for Extractions
    const [combinations, setCombinations] = useState(2); // Default value for Combinations

    const handleFetchButtonClick = () => {
        // Construct the URL with query parameters
        const queryParams = `?extractions=${extractions}&combinations=${combinations}`;
        const apiUrl = `/api/test-api${queryParams}`;

        // Perform the API fetch or action
        // For demonstration, we'll log the apiUrl
        console.log(apiUrl);
    };

    return (
        <div>
            <Typography variant="body" color="black">
            <input
            type="file"
            accept=".txt"
            onChange={handleFileChange}
        />
        {selectedFile && <p>Selected file: {selectedFile.name}</p>}

            {/* Advanced section */}
            <Box sx={{ border: 1, p: 2, mt: 3 , m: 2}}>
                <h2>Advanced</h2>
                <div>
                    <h3>Extractions</h3>
                    <Slider
                        value={extractions}
                        onChange={(event, newValue) => setExtractions(newValue)}
                        valueLabelDisplay="auto"
                        step={1}
                        marks
                        min={1}
                        max={5}
                    />
                </div>
                <div>
                    <h3>Combinations</h3>
                    <Slider
                        value={combinations}
                        onChange={(event, newValue) => setCombinations(newValue)}
                        valueLabelDisplay="auto"
                        step={1}
                        marks
                        min={1}
                        max={3}
                    />
                </div>
            </Box>

            {/* Fetch button */}
            <Button variant="contained" onClick={handleFetchButtonClick}>
                Create Summary
            </Button>
            <Button variant="contained" onClick={handleFetchButtonClick}>
                Finish Later
            </Button>
            </Typography>
        </div>
    );
}

export default CreateSummaryForm;