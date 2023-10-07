'use client';
import React, { useState } from "react";
import { useAuthContext } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import getData from '@/firebase/firestore/getData';
import setData from '@/firebase/firestore/setData';
import addData from '@/firebase/firestore/addData';

import UploadFileButton from "@/app/components/UploadDocumentButton";
import PageContainer from '@/app/components/PageContainer';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';
import { Typography } from "@mui/material";
import { ToastContainer, toast } from 'react-toastify';
import { showToastError, showToastSuccess } from './Toaster'


const CreateSummaryForm = () => {
  const { user } = useAuthContext()
  const router = useRouter()
  const [selectedFile, setSelectedFile] = useState(null);
  const [extractions, setExtractions] = useState(3); // Default value for Extractions
  const [combinations, setCombinations] = useState(2); // Default value for Combinations

  const handleFileChange = (event) => {
    const file = event.target.files && event.target.files[0];

    if (file) {
      const fileType = file.type;
      if (fileType === 'text/plain') {
        setSelectedFile(file);
      } else {
        showToastError('Please upload a text file');
      }
    }
  };


  // FINISH LATER

  const handleFinishLater = () => {
    console.log('Button Pressed');
    getData('users',user.uid).then(
      data => {console.log(data.result.data())}
    )
    if (selectedFile === null) {
      showToastError('Upload a file');
      return;
    }

      const reader = new FileReader();
      reader.onload = (event) => {
        const content = event.target.result;
        console.log('content: ' + content);
        uploadDoc(content, 'unfinished'); // Pass content to the uploadDoc function
      };
      reader.readAsText(selectedFile);
    // const encodedUri = encodeURIComponent('uploaded');
    router.push(`/summaries`);
  };
//test
  // CREATE SUMMARY
  const handleCreateSummary = () => {
    if (selectedFile === null) {
      showToastError('Upload a file');
      return;
    }
    const reader = new FileReader();
    reader.onload = (event) => {
      const content = event.target.result;
      console.log('content: ' + content);
      uploadDoc(content, 'processing').then(([n, title]) => {
        try {
            const docref = addData(`users/${user.uid}/jobs`, {
              parent_doc:`${n}`,
              parent_title:`${title}`,
              status: 0,
              extractions: `${extractions}`,
              combinations: `${combinations}`

            })
          // OLD CODE - Called api directly with json data
          // console.log('handleCreateSummary-->uploadDoc-->then Try Block');

          // fetch('/api/openai', {
          //   method: 'POST',
          //   headers: {
          //     Authorization: `Bearer ${user.uid}`,
          //     'Content-Type': 'application/json',
          //   },
          //   body: JSON.stringify({
          //      doc_id: `${n}`,
          //      extractions: `${extractions}`,
          //      combinations: `${combinations}`
          //   }),
          // })
          // .then(response => response.json())
          // .then(data => {
          //     console.log("RESPONSE: " + data.transcript)
          //     if (message == "Job starting") {
          //       console.log("Job Starting")
          //     }
          // })

        } catch (error) {
          console.log('Error occurred');
        }

      }) // Pass content to the uploadDoc function
    };
    reader.readAsText(selectedFile);

    // Onload will run here

    // const encodedUri = encodeURIComponent('uploaded');


    

  }

  async function uploadDoc(content, stat) {
    
    try {
      const { result, error } = await addData(`users/${user.uid}/files`, { 
        title: selectedFile.name,
        body: content
      });
      showToastSuccess('Document Uploaded!');
      return [result.id, selectedFile.name];
    } catch (error) {
      showToastError('Upload Error');
      console.error('Error uploading document:', error);
    }
    return [null, null];
  }

  // function incrementFileString(originalString) {
  //   // Convert the original string to a number and increment
  //   const incrementedNumber = parseInt(originalString, 10) + 1;

  //   // Determine the length of the original string
  //   const originalLength = originalString.length;

  //   // Format the incremented number with leading zeroes to match the original length
  //   const formattedIncremented = String(incrementedNumber).padStart(originalLength, '0');

  //   return formattedIncremented;
  // }

    React.useEffect(() => { 
        if (user == null) router.push("/")
    }, [user])
    console.log("User ID: "+user['uid']);
    // console.log(user);

    

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
            {/* <ToastContainer/> */}
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
            <Button variant="contained" onClick={handleCreateSummary}>
                Create Summary
            </Button>
            <Button variant="contained" onClick={handleFinishLater}>
                Finish Later
            </Button>
            </Typography>
        </div>
    );
}

export default CreateSummaryForm;