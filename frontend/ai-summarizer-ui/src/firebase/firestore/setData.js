import firebase_app from "../config";
import { getFirestore, doc, setDoc } from "firebase/firestore";

const db = getFirestore(firebase_app)
export default async function setData(collection, id, data) {
    let result = null;
    let error = null;

    try {
        result = await setDoc(doc(db, collection, id), data, {
            merge: true,
        });
    } catch (e) {
        error = e;
        console.log("setData Error: " + e)
    }

    return { result, error };
}
