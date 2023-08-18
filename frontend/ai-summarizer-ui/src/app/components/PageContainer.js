import { Container, Grid } from '@mui/material';
import Header from '@/app/components/Header'
import { ToastProvider } from './ToastContext';

const PageContainer = ({ children }) => {
    return (
        <ToastProvider>
            <Grid container direction="column">
                <Grid item>
                    <Header />
                </Grid>
                <Grid item container style={{ marginTop: '20px' }}>
                    <Container>{children}</Container>
                </Grid>
            </Grid>
        </ToastProvider>
        
      );
};

export default PageContainer;