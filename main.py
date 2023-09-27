from fastapi import FastAPI, Body, File, UploadFile, HTTPException,Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from database import db
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import uvicorn 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def getRoutes():
    return ['/notes', '/notes/{ID}']  # Use curly braces for path parameters

@app.get("/notes")
def getNotes():
    notes = db.sql('SELECT * FROM notesapp.notes ORDER BY __updatedtime__ DESC')
    return notes

@app.get("/notes/{id}")
def getNote(id: str):
    notes = db.search_by_hash('notesapp', 'notes', [id], get_attributes=['*'])
    if notes:
        return notes[0]
    else:
        raise HTTPException(status_code=404, detail="Note not found")

@app.post("/notes")
def addNotes(data: dict = Body(...)):
    note = {
        "candidate": data.get('candidate'),
        "name": data.get('name'),
        "age": data.get('age'),
        "joinDate": data.get('joinDate'),
        "rate": data.get('rate'),
        "dRate": data.get('dRate')
    }
    db.insert('notesapp', 'notes', [note])
    notes = db.sql('SELECT * FROM notesapp.notes')
    return notes


@app.put("/notes/{id}")
def updateNote(id: str, data: dict = Body(...)):
    global overall_defect_percentage
    overall_defect_percentage = 0.0  # Reset the overall_defect_percentage value to zero

    note = {
        "id": id,
        "candidate": data.get('candidate'),
        "name": data.get('name'),
        "age": data.get('age'),
        "joinDate": data.get('joinDate'),
        "rate": data.get('rate'),
        "dRate": data.get('dRate')
    }
    db.update('notesapp', 'notes', [note])
    notes = db.sql('SELECT * FROM notesapp.notes')
    return notes

#search
@app.get("/search", response_model=List[dict])
def search_notes(
    candidate: str = Query(None),
    name: str = Query(None),
    age: int = Query(None),
    joinDate: str = Query(None),
    rate: float = Query(None),
    dRate: float = Query(None)
):
    notes = db.sql('SELECT * FROM notesapp.notes')  # Fetch all notes from the database
    results = []

    for note in notes:
        # Check if the note matches the search criteria
        if (
            (candidate is None or note["candidate"] == candidate) and
            (name is None or note["name"] == name) and
            (age is None or note["age"] == age) and
            (joinDate is None or note["joinDate"] == joinDate) and
            (rate is None or note["rate"] == rate) and
            (dRate is None or note["dRate"] == dRate)
        ):
            results.append(note)

    return results


@app.delete("/notes/{id}")
def deleteNote(id: str):
    db.delete('notesapp', 'notes', [id])
    notes = db.sql('SELECT * FROM notesapp.notes')
    return notes

MODEL = tf.keras.models.load_model('./model/final_model.h5')
CLASS_NAMES = ["apple_pie", "baby_back_ribs", "baklava", "cheesecake", 
               "chicken_curry", "chicken_quesadilla", "chicken_wings", 
               "chocolate_cake", "chocolate_mousse", "churros", "club_sandwich", 
               "crab_cakes", "creme_brulee", "croque_madame", "cup_cakes", 
               "deviled_eggs", "donuts", "dumplings", "eggs_benedict", 
               "escargots", "falafel", "filet_mignon", "fish_and_chips"]

@app.get("/ping")
async def ping():
    return "Hello, I am alive"

def read_file_as_image(data) -> np.ndarray:
    try:
        image = Image.open(BytesIO(data))
        # Resize image to (256, 256)
        image = image.resize((256, 256))
        image = np.array(image)
        return image
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image file")

prediction_counter = 0
defect_counter = 0
overall_defect_percentage = 0.0

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    global prediction_counter, defect_counter, overall_defect_percentage

    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)

    predictions = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]


    confidence = np.max(predictions[0])
    response = {
        'class': predicted_class,
        'confidence': float(confidence)
    }


    return response

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=7000)