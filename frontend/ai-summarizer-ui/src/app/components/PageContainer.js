import { Container, Grid } from '@mui/material';
import Header from '@/app/components/Header'

const PageContainer = ({ children }) => {
    return (
        <Grid container direction="column">
          <Grid item>
            <Header />
          </Grid>
          <Grid item container style={{ marginTop: '20px' }}>
            <Container>{children}</Container>
          </Grid>
        </Grid>
      );
};

export default PageContainer;