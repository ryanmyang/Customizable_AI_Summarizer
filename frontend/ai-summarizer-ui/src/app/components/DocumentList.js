import React, { useState, useEffect } from 'react';
import { useAuthContext } from '@/context/AuthContext';
import { getFirestore, collection, getDocs } from 'firebase/firestore';
import firebase_app from "@/firebase/config";
import '@/app/globals.css'



const DocumentList = () => {
  const { user } = useAuthContext();
  const [documentIds, setDocumentIds] = useState([]);
  const db = getFirestore(firebase_app)

  useEffect(() => {
    // Fetch the list of document IDs
    fetchDocumentIds();
  }, []);

  const fetchDocumentIds = async () => {
    try {
      const filesCollectionRef = collection(db, `users/${user.uid}/files`);
      const filesSnapshot = await getDocs(filesCollectionRef);
        console.log(filesSnapshot);
      const ids = filesSnapshot.docs.map(doc => doc.data().title);
      setDocumentIds(ids);
    } catch (error) {
      console.error('Error fetching document IDs:', error);
    }
  };

  return (
    <div>
      <h2>Document List</h2>
      <ul>
        {documentIds.map(id => (
          <li key={id}>{id}</li>
        ))}
      </ul>
    </div>
  );
};

export default DocumentList;
