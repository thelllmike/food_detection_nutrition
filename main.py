from fastapi import FastAPI, Body, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from database import db
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
import uvicorn 
import pandas as pd
from fuzzywuzzy import process

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the nutrition data from the .pkl file
nutrition_data = pd.read_pickle("./model/food_nutrition_data.pkl")

def get_nutrition_info(food_name: str):
    best_match, score = process.extractOne(food_name, nutrition_data['Food Category '].tolist())
    if score < 50:
        return None
    return nutrition_data[nutrition_data['Food Category '] == best_match].iloc[0].to_dict()

# Routes and CRUD operations for 'notes' can remain unchanged...

# Ensure CLASS_NAMES is defined before the prediction endpoint
CLASS_NAMES = ["apple_pie", "baby_back_ribs", "baklava", "cheesecake", 
               "chicken_curry", "chicken_quesadilla", "chicken_wings", 
               "chocolate_cake", "chocolate_mousse", "churros", "club_sandwich", 
               "crab_cakes", "creme_brulee", "croque_madame", "cup_cakes", 
               "deviled_eggs", "donuts", "dumplings", "eggs_benedict", 
               "escargots", "falafel", "filet_mignon", "fish_and_chips"]

MODEL = tf.keras.models.load_model('./model/final_model.h5')

@app.get("/ping")
def ping():
    return "Hello, I am alive"

def read_file_as_image(data) -> np.ndarray:
    try:
        image = Image.open(BytesIO(data))
        image = image.resize((256, 256))
        image = np.array(image)
        return image
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image file")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)

    predictions = MODEL.predict(img_batch)
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])

    nutrition_info = get_nutrition_info(predicted_class)

    response = {
        'class': predicted_class,
        'confidence': float(confidence),
        'nutrition_info': nutrition_info
    }

    return response

if __name__ == "__main__":
    #uvicorn.run(app, host='0.0.0.0', port=7000)

    uvicorn.run(app, host='localhost', port=8001)
