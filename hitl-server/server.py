from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from uuid import uuid4
import uvicorn

app = FastAPI()

# In-memory storage
approvals: Dict[str, Dict] = {}

# Pydantic models
class ApprovalCreate(BaseModel):
    tool_name: str
    agent_id: str
    session_id: str
    status: Optional[bool] = None

class ApprovalUpdate(BaseModel):
    status: bool

class Approval(BaseModel):
    id: str
    tool_name: str
    agent_id: str
    session_id: str
    status: Optional[bool] = None

# Routes
@app.get("/approvals", response_model=list[Approval])
def get_approvals():
    return list(approvals.values())

@app.post("/approvals", response_model=Approval)
def create_approval(approval: ApprovalCreate):
    approval_id = str(uuid4())
    new_approval = Approval(id=approval_id, **approval.dict())
    approvals[approval_id] = new_approval.dict()
    return new_approval

@app.get("/approvals/{id}", response_model=Approval)
def get_approval(id: str):
    if id not in approvals:
        raise HTTPException(status_code=404, detail="Approval not found")
    return approvals[id]

@app.patch("/approvals/{id}", response_model=Approval)
def update_approval(id: str, update: ApprovalUpdate):
    if id not in approvals:
        raise HTTPException(status_code=404, detail="Approval not found")

    current = approvals[id]
    updated_data = update.dict(exclude_unset=True)
    current.update(updated_data)
    approvals[id] = current
    return current

if __name__ == "__main__":
    uvicorn.run("server:app", host="localhost", port=8005, reload=True)

