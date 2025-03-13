from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from api.database import health_collection
from api.models import HealthData
from api.ocr import extract_text_from_pdf, extract_text_from_image
from api.pdf_generator import generate_pdf

router = APIRouter()

# ✅ Store Health Data
@router.post("/health")
async def store_health_data(data: HealthData):
    new_entry = await health_collection.insert_one(data.dict())
    return {"message": "Health data stored successfully", "entry_id": str(new_entry.inserted_id)}

# ✅ Get User Health Data
@router.get("/health/{user_id}")
async def get_health_data(user_id: str):
    data = await health_collection.find({"user_id": user_id}).to_list(100)
    return {"user_id": user_id, "health_data": data}

@router.post('/upload_report')
async def upload_report(file: UploadFile = File(...)):
    file_extension = file.filename.split(".")[-1].lower()
    file_path = f"uploads/{file.filename}"
    
    with open(file_path, "wb") as f:
        f.write(file.file.read())
        
    if file_extension in ["jpg", "jpeg", "png"]:
        extracted_text = extract_text_from_image(file_path)
    elif file_extension in ["pdf"]:
        extracted_text = extract_text_from_pdf(file_path)
    else:
        return {"error": "Unsupported file format"}
    
    return {"extracted_text": extracted_text}

@router.get('/download_report/{user_id}', response_class=FileResponse)
async def download_report(user_id: str):
    # fetch user health data from mongoDB
    user_health_data = await health_collection.find_one({"user_id": user_id})
    
    print(user_health_data)
    
    if not user_health_data:
        raise HTTPException(status_code=404, detail="No health data found")
    
    # generate PDF report
    pdf_path = generate_pdf(user_id, user_health_data)
    
    return FileResponse(
        pdf_path, 
        media_type="application/pdf", 
        filename=f"{user_id}_report.pdf"
    )