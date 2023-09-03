import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import os
import json

load_dotenv()
service_account_key = os.getenv("SERVICE_ACCOUNT_KEY")
cred = credentials.Certificate(json.loads(service_account_key))
firebase_admin.initialize_app(cred)

db = firestore.client()

def add_data(collection, data):
    db.collection(collection).add(data)
    print(f'Added data "{data}" to {collection}')

def get_document(collection, doc_id):
    doc_ref = db.collection(collection).document(doc_id)
    doc = doc_ref.get()
    
    if doc.exists:
        # The document exists, you can access its data using doc.to_dict()
        return doc.to_dict()
    else:
        # The document doesn't exist
        print(f"Get_Document failed, doc with id {doc_id} doesn't exist in collection {collection}")
        return None

if __name__ == '__main__':
    # Adding test: value
    print('Adding test:value')
    add_data('users/kfMkPJYQCEaHuamphApNeN8YcSy1/files', {'test':'value'})
    document = get_document('users/kfMkPJYQCEaHuamphApNeN8YcSy1/files','044')
    print(document['body'])
