from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text
import pandas as pd
import os
# Change to your project root directory
os.chdir(r'c:\users\ermias.tadesse\10x\Centralize-Ethiopian-medical-business-data')
from scripts.db_connection import DBConnection

# Initialize FastAPI
app = FastAPI()

# Initialize DBConnection
db = DBConnection(dbname='Central_Medical_Warehouse', user='postgres', password='Ermi@123')
db.connect()

# Define a Pydantic model for the detection result
class Detection(BaseModel):
    media_id: int
    object_class: str
    confidence: float
    bounding_box: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Object Detection API"}

@app.get("/detections/{media_id}", response_model=list[Detection])
def get_detections(media_id: int):
    # Query to retrieve detection data for a specific media_id
    query = """
    SELECT 
        media_id, 
        object_class, 
        confidence, 
        bounding_box 
    FROM 
        detections 
    WHERE 
        media_id = :media_id;
    """
    try:
        # Load the detection data into a pandas DataFrame
        df_detections = pd.read_sql_query(query, db.engine, params={"media_id": media_id})
        
        # Convert DataFrame to list of dictionaries
        detections = df_detections.to_dict(orient='records')
        return detections
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
