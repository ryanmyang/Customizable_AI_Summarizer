import firebase_app from "../config";
import { createUserWithEmailAndPassword, getAuth } from "firebase/auth";
import { getFirestore, doc, setDoc } from "firebase/firestore";
import addData from "@/firebase/firestore/addData"

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
            
            const currentDate = new Date();
            const date_num = currentDate.getTime();
            console.log(uid)

            await addData("users", "YyNuXTF42xdnnPz3Rqv5lCSixnj2", {
                email: email,
                age: date_num
            });
        }

    } catch (e) {
        error = e;
        console.log(e)

    }
    return { result, error };
}
