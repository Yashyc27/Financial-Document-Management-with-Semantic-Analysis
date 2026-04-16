from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid, uvicorn, database, rag_engine
from pydantic import BaseModel

app = FastAPI(title="Financial Management API")
rag = rag_engine.FinancialRAG()

def get_db():
    db = database.SessionLocal()
    try: yield db
    finally: db.close()

class SearchReq(BaseModel): query: str
class UserAuth(BaseModel): username: str; password: str; role: str = "Client"
class RoleUpdate(BaseModel): user_id: int; role: str


@app.post("/auth/register")
def register(user: UserAuth, db: Session = Depends(get_db)):
    db_user = database.User(username=user.username, password=user.password, role=user.role)
    db.add(db_user); db.commit(); return {"message": "User registered"}

@app.post("/auth/login")
def login(user: UserAuth): return {"token": "dummy_jwt_token"}

@app.post("/roles/create")
def create_role(name: str): return {"message": f"Role {name} created"}

@app.post("/users/assign-role")
def assign_role(up: RoleUpdate, db: Session = Depends(get_db)):
    u = db.query(database.User).filter(database.User.id == up.user_id).first()
    if u: u.role = up.role; db.commit()
    return {"message": "Role assigned"}

@app.get("/users/{id}/roles")
def get_roles(id: int, db: Session = Depends(get_db)):
    u = db.query(database.User).filter(database.User.id == id).first()
    return {"roles": [u.role] if u else []}

@app.get("/users/{id}/permissions")
def get_perms(id: int, db: Session = Depends(get_db)):
    u = db.query(database.User).filter(database.User.id == id).first()
    perms = {"Admin": "Full", "Analyst": "Upload/Edit", "Auditor": "Review", "Client": "View"}
    return {"permissions": perms.get(u.role, "None")}
@app.post("/documents/upload")
async def upload(title: str, company: str, doc_type: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    doc_id = str(uuid.uuid4())
    content = (await file.read()).decode("utf-8")
    new_doc = database.Document(document_id=doc_id, title=title, company_name=company, document_type=doc_type, uploaded_by="Admin")
    db.add(new_doc); db.commit()
    rag.index_document(content, doc_id)
    return {"document_id": doc_id, "status": "Indexed"}

@app.get("/documents")
def list_docs(db: Session = Depends(get_db)): return db.query(database.Document).all()

@app.get("/documents/{document_id}")
def get_doc(document_id: str, db: Session = Depends(get_db)):
    return db.query(database.Document).filter(database.Document.document_id == document_id).first()

@app.delete("/documents/{document_id}")
def delete_doc(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(database.Document).filter(database.Document.document_id == document_id).first()
    if doc: db.delete(doc); db.commit(); rag.remove_document(document_id)
    return {"message": "Deleted"}


@app.post("/rag/index-document")
async def index_rag(text: str):
    rag.index_document(text, str(uuid.uuid4()))
    return {"message": "Text stored in Vector DB"}

@app.post("/rag/search")
def semantic_search(req: SearchReq):
    results = rag.search_pipeline(req.query)
    return {"results": [{"content": r.page_content, "metadata": r.metadata} for r in results]}

@app.get("/rag/context/{document_id}")
def get_context(document_id: str): return {"document_id": document_id, "context": "Financial data"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)