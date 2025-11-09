from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pymongo import MongoClient
from bson import ObjectId
import uvicorn
import os

app = FastAPI()

# MongoDB connection using environment variable
mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
client = MongoClient(mongodb_url)
db = client["todoapp"]
collection = db["todos"]

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    todos = list(collection.find())
    # Convert ObjectId to string for JSON serialization
    for todo in todos:
        todo["_id"] = str(todo["_id"])
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

@app.post("/add")
async def add_todo(title: str = Form(...)):
    todo = {"title": title, "completed": False}
    collection.insert_one(todo)
    return RedirectResponse(url="/", status_code=303)

@app.post("/update/{todo_id}")
async def update_todo(todo_id: str):
    todo = collection.find_one({"_id": ObjectId(todo_id)})
    if todo:
        collection.update_one(
            {"_id": ObjectId(todo_id)},
            {"$set": {"completed": not todo["completed"]}}
        )
        return {"success": True}
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/delete/{todo_id}")
async def delete_todo(todo_id: str):
    result = collection.delete_one({"_id": ObjectId(todo_id)})
    if result.deleted_count:
        return {"success": True}
    raise HTTPException(status_code=404, detail="Todo not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)