# FastAPI Food Prediction and Nutrition Information System

A comprehensive system designed to empower users with the ability to predict the category of food based solely on an uploaded image. Beyond merely classifying food items, the system is also adept at delivering relevant nutritional information associated with the recognized food category. This dual functionality aims to make dietary choices transparent and well-informed, bridging the gap between mere recognition and in-depth understanding.

## 🚀 Features

1. **Image-based Food Prediction**: Users can upload an image of a food item, and the system will predict the category of the food leveraging a robust deep learning model.
2. **Nutritional Information Retrieval**: Following a successful food prediction, the system promptly fetches the corresponding nutritional information from a pre-stored dataset, offering users deeper insights into their dietary choices.

## 🎯 Getting Started

### Prerequisites

- Python 3.8 or newer.
- FastAPI and Uvicorn for robust API functionalities.
- TensorFlow to enable machine learning capabilities.
- PIL (Python Imaging Library) for image processing.

### Installation

```bash
# Clone the Repository:
git clone [Your Repository URL]
cd [Your Repository Directory]

# Set Up a Virtual Environment:
python -m venv env
source env/bin/activate  # On Windows use: .\env\Scripts\activate

# Install Required Packages:
pip install -r requirements.txt

# Ensure Data File Presence:
# Confirm the existence of `food_nutrition_data.pkl` in the root directory.

# Run the Application:
uvicorn main:app --reload
