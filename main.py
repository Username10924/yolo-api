from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
import shutil
import os

app = FastAPI()

# Load your trained YOLOv9 model
model = YOLO("best.pt")  # make sure best.pt is inside your project

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Save uploaded image
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run prediction
    results = model.predict(temp_file_path, conf=0.5)
    detections = results[0].boxes

    # Analyze detections
    item_detected = len(detections) > 0

    # Clean up temp file
    os.remove(temp_file_path)

    if item_detected:
        return {"status": "Illegal item detected ✅"}
    else:
        return {"status": "No illegal item detected ❌"}
