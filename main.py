from fastapi import FastAPI
from fastapi import UploadFile, File
import os
import fitz

app = FastAPI()

@app.get("/")
def home():
    return {"Message": "API is Running"}

user_db={}
@app.post("/register")
def register(username: str, password: str):
    if username in user_db:
        return {"message": "Username already exists!"}
    user_db[username] = password
    return {"message": "User registered successfully!"}


@app.post("/login")
def login(username: str, password: str):
    if username not in user_db:
        return {"message": "User not found!"}
    user = user_db.get(username)
    if user!=password:
        return {"message": "Incorrect password!"}
    return {"message": "User logged in!"}

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

documents_db={}

@app.post("/document_upload")
def upload_file(file: UploadFile = File(...)):
    file_path=os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path,'wb') as f:
        f.write(file.file.read())
    doc = fitz.open(file_path)
    text=""
    for page in doc:
        text+=page.get_text()
    documents_db[file.filename] = text
    return {"message": "File uploaded successfully", "file": file.filename}

@app.get("/search")
def search(query: str):
    result=[]
    for filename, content in documents_db.items():
        if query.lower() in content.lower():
            result.append(filename)
    return {"result": result}


@app.post("/rag/search")
def search(query: str):
    result=[]
    for filename, content in documents_db.items():
        if query.lower() in content.lower():
            result.append({
                "filename": filename,
                "matched_text": content[:200]
            })
    return {"result": result}


