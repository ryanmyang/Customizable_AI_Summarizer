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

def add_data(collection, data: dict):
    # Add returns reference https://cloud.google.com/python/docs/reference/firestore/latest/collection
    # reference 


    doc_ref = db.collection(collection).add(data)
        
    
    print(f'Added data "{data}" to {collection}')
    path = doc_ref[1].path
    print(path)
    return path

def set_data(path, data, merge = True):
    path_elements = path.split('/')
    doc_id=path_elements.pop(-1)
    collection_path = '/'.join(path_elements)
    doc_ref = db.collection(collection_path).document(doc_id)
    doc_ref.set(data, merge)

def get_data(collection, doc_id):
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
    document = get_data('users/kfMkPJYQCEaHuamphApNeN8YcSy1/files','044')
    # print(document['body'])
