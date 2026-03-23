from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from services.ticket import create_ticket

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/chat")
def chat(request: dict, db: Session = Depends(get_db)):
    message = request["message"]

    # Simple bot logic
    if "refund" in message.lower():
        return {"response": "Your refund is being processed."}

    # If unresolved → create ticket
    ticket = create_ticket(db, message)

    return {
        "response": "Issue escalated to support.",
        "ticket_id": ticket.id,
        "category": ticket.category,
        "severity": ticket.severity
    }