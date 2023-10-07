import firebase_app from "../config";
import { createUserWithEmailAndPassword, getAuth } from "firebase/auth";
import { getFirestore, doc, setDoc } from "firebase/firestore";
import setData from "@/firebase/firestore/setData"

const auth = getAuth(firebase_app);
const db = getFirestore(firebase_app);

export default async function signUp(email, password) {
    let result = null,
        error = null;
    try {
        result = await createUserWithEmailAndPassword(auth, email, password);
        
        // If the user is created successfully, save additional details in Firestore
        if (result.user) {
            const uid = String(result.user.uid);
            
            console.log(uid)

            await setData("users", uid, {
                email: email,
                next_file: '000'
            });
        }

    } catch (e) {
        error = e;
        console.log(e)

    }
    return { result, error };
}
