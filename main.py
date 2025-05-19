from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
import shutil
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load trained YOLOv9 model
weapon_model = YOLO("weapon_model.pt")
drug_model = YOLO("drug_model.pt")

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Save uploaded image
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run both predictions
    weapon_results = weapon_model.predict(temp_file_path, conf=0.5)
    drug_results = drug_model.predict(temp_file_path, conf=0.5)

    # Get detection results
    weapon_detected = len(weapon_results[0].boxes) > 0
    drug_detected = len(drug_results[0].boxes) > 0

    # Clean up temp file
    os.remove(temp_file_path)

    # Decide response
    if weapon_detected and drug_detected:
        return {"status": "Illegal weapon and drug detected"}
    elif weapon_detected:
        return {"status": "Illegal weapon detected"}
    elif drug_detected:
        return {"status": "Illegal drug detected"}
    else:
        return {"status": "NO"}
