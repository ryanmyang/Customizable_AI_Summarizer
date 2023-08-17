import React from 'react';
import { AppBar, Toolbar, Typography } from '@mui/material';

const Header = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6">My App</Typography>
        {/* Add menu bar or navigation links here */}
      </Toolbar>
    </AppBar>
  );
};

export default Header;
