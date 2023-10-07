import firebase_app from "../config";
import { getFirestore, collection, addDoc } from "firebase/firestore";

const db = getFirestore(firebase_app)

// Takes collection and data in form of js object(not string)
// Returns result and error, result being a docreference
export default async function addData(c, data) {
    let result = null;
    let error = null;

    try {
        result = await addDoc(collection(db, c), data, {
            merge: true,
        });
    } catch (e) {
        error = e;
        console.log("addData Error: " + e)
    }

    return { result, error };
}
