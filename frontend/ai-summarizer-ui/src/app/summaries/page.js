'use client'
import React from "react";
import { useAuthContext } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import UploadFileButton from "@/app/components/UploadDocumentButton";
import PageContainer from '@/app/components/PageContainer';
import DocumentList from '@/app/components/DocumentList';
import Button from '@mui/material/Button';
import { Container, Grid } from '@mui/material';


function Page() {
    const { user } = useAuthContext()
    const router = useRouter()

    React.useEffect(() => {
        if (user == null) router.push("/")
    }, [user])
    console.log("User ID: "+user['uid']);
    console.log(user);

    const handleNewSummaryButton = () => {
        router.push("/summaries/new");
    }
    return (
        <PageContainer>
      <Grid container justifyContent="flex-end" mb={2}>
        <Button onClick={handleNewSummaryButton} variant="contained">
          New Summary
        </Button>
      </Grid>
      <DocumentList />
    </PageContainer>
    
    
    );
}

export default Page;
