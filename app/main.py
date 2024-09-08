from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
import uuid

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# In-memory database (replace with a real database in production)
guestbook_entries = []

class GuestbookEntry(BaseModel):
    id: str
    name: str
    message: str
    timestamp: datetime

@app.get("/", response_class=HTMLResponse)
async def read_guestbook(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "entries": guestbook_entries})

@app.post("/add_entry")
async def add_entry(name: str = Form(...), message: str = Form(...)):
    entry = GuestbookEntry(
        id=str(uuid.uuid4()),
        name=name,
        message=message,
        timestamp=datetime.now()
    )
    guestbook_entries.append(entry)
    return {"message": "Entry added successfully"}

@app.delete("/delete_entry/{entry_id}")
async def delete_entry(entry_id: str):
    for entry in guestbook_entries:
        if entry.id == entry_id:
            guestbook_entries.remove(entry)
            return {"message": "Entry deleted successfully"}
    raise HTTPException(status_code=404, detail="Entry not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)