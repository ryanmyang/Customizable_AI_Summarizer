import React from 'react';
import { FormControl, InputLabel, MenuItem, Select } from '@mui/material';
import fs from 'fs';
import path from 'path';

const FileDropdown: React.FC = () => {
  // Function to fetch the list of files from the "files" folder
  const getAvailableFiles = () => {
    const filesFolder = path.join(process.cwd(), '../../backend/refs');
    try {
      const files = fs.readdirSync(filesFolder);
      return files;
    } catch (error) {
      console.error('Error reading files:', error);
      return [];
    }
  };

  // Get the list of available files
  const availableFiles = getAvailableFiles();

  return (
    <div>
      <h1>Select a File:</h1>
      <FormControl fullWidth variant="outlined">
        <InputLabel>Files</InputLabel>
        <Select label="Files">
          {availableFiles.map((file) => (
            <MenuItem key={file} value={file}>
              {file}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </div>
  );
};

export default FileDropdown;
