import React from 'react';
import { FormControl, InputLabel, MenuItem, Select } from '@mui/material';


const FileDropdown: React.FC = () => {
  // Function to fetch the list of files from the "files" folder
  const getAvailableFiles = () => {

  };

  // Get the list of available files
  const availableFiles = getAvailableFiles();

  return (
    <div>
      <h1>Select a File:</h1>
      <FormControl fullWidth variant="outlined">
        <InputLabel>Files</InputLabel>
        <Select label="Files">
        </Select>
      </FormControl>
    </div>
  );
};

export default FileDropdown;
