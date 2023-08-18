import React from "react";
import { useAuthContext } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import UploadFileButton from "@/app/components/UploadDocumentButton";
import PageContainer from '@/app/components/PageContainer';
import CreateSummaryForm from '@/app/components/CreateSummaryForm';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Slider from '@mui/material/Slider';

function Page() {
    
    

    return (
        <PageContainer>
            {/* Existing content */}
            <CreateSummaryForm/>
        </PageContainer>
    );
}

export default Page;
