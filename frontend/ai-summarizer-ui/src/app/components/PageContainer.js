import { Container, Grid } from '@mui/material';
import Header from '@/app/components/Header'
import { ToastProvider } from './ToastContext';
import { ToastContainer } from 'react-toastify';

const PageContainer = ({ children }) => {
    return (
        <div>
            <ToastContainer/>
            <Grid container direction="column">
                <Grid item>
                    <Header />
                </Grid>
                <Grid item container style={{ marginTop: '20px' }}>
                    <Container>{children}</Container>
                </Grid>
            </Grid>
        </div>
        
      );
};

export default PageContainer;