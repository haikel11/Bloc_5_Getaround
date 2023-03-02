import uvicorn
import pandas as pd 
import json
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile
from joblib import dump, load



description = """
### Welcome to Getaround FastAPI.
Get Around API suggest you the optimal rental price per day of a car.
"""


# initialise API object
app = FastAPI(
    title="GETAROUND API",
    description=description,
    version="1.0",
    openapi_tags= [
    {
        "name": "Home",
        "description": "Get Around API homepage."
    },
    {
        "name": "Predicts",
        "description": "Get Around API with POST or GET method."
    }
]
)


tags_metadata = [
    {
        "name": "Introduction Endpoints",
        "description": "Simple endpoints to try out!",
    },
    {
        "name": "Prediction",
        "description": "Prediction of the rental price based on a machine learning model"
    }
]


class PredictionFeatures(BaseModel):
    model_key: str = "BMW"
    mileage: int = 75515
    engine_power: int = 135
    fuel: str = "diesel"
    paint_color: str = "grey"
    car_type: str = "suv"
    private_parking_available: bool = False
    has_gps: bool = True
    has_air_conditioning: bool = False
    automatic_car: bool = True
    has_getaround_connect: bool = True
    has_speed_regulator: bool = False
    winter_tires: bool = True
    
    
@app.get("/", tags = ["Introduction Endpoint"])
async def index():
    message = "Hello! This `/` is the most simple and default endpoint for the API`"
    return message


@app.get("/preview", tags=["Preview"])
async def preview(rows: int):
    """ Give a preview of the dataset : Number of rows"""
    data = pd.read_csv("get_around_pricing_project.csv")
    preview = data.head(rows)
    return preview.to_dict()


@app.post("/predict", tags = ["Price prediction"])
async def predict(predictionFeatures: PredictionFeatures):
    # Read data 
    data = pd.DataFrame(dict(predictionFeatures), index=[0])
    # Load model
    loaded_model = load("model.joblib")
    # Prediction
    prediction = loaded_model.predict(data)
    # Format response
    response ={"predictions": prediction.tolist()[0]}
    return response

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000, debug=True, reload=True)

