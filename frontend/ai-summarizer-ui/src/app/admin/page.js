'use client'
import React from "react";
import { useAuthContext } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import UploadFileButton from "@/app/components/UploadDocumentButton";
import PageContainer from '@/app/components/PageContainer';
import DocumentList from '@/app/components/DocumentList';

function Page() {
    const { user } = useAuthContext()
    const router = useRouter()

    React.useEffect(() => {
        if (user == null) router.push("/")
    }, [user])
    console.log("User ID: "+user['uid']);
    console.log(user);
    return (
        <PageContainer>
            <h1>Only logged in users can view this page</h1>
            <UploadFileButton/>
            <DocumentList/>

        </PageContainer>
    
    
    );
}

export default Page;
