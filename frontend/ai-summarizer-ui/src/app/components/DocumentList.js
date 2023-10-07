import React, { useState, useEffect } from 'react';
import { useAuthContext } from '@/context/AuthContext';
import { getFirestore, collection, getDocs } from 'firebase/firestore';
import firebase_app from "@/firebase/config";
import '@/app/globals.css'
import Button from '@mui/material/Button';



const DocumentList = () => {
  const { user } = useAuthContext();
  const [docDatas, setDocDatas] = useState([]);
  const db = getFirestore(firebase_app);

  useEffect(() => {
    // Fetch the list of document IDs
    fetchDocumentIds();
  }, []);

  const fetchDocumentIds = async () => {
    try {
      const filesCollectionRef = collection(db, `users/${user.uid}/jobs`);
      const filesSnapshot = await getDocs(filesCollectionRef);
      const datas = filesSnapshot.docs.map(doc => [doc.data().parent_title,doc.data().parent_doc]);
      setDocDatas(datas);
    } catch (error) {
      console.error('Error fetching document IDs:', error);
    }
  };

  const handleDocumentClick = (documentName) => {
    // Handle the click event here, e.g., open the document
    console.log(`Clicked on document: ${documentName}`);
  };

  return (
    <div>
      <h2>Document List</h2>
      <ul>
        {docDatas.map((id, index) => (
          <li key={index}>
            <Button
              fullWidth
              variant="outlined"
              color="primary"
              onClick={() => handleDocumentClick(id[1])}
              style={{ 

                textTransform: 'none' ,
                justifyContent: "flex-start"
              }}
            >
              {id[0]}
            </Button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DocumentList;