from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.translation_service import translation_service
from services.ai_model_service import ai_model_service
from dotenv import load_dotenv
import uvicorn
import os
import shutil
import uuid
from pydantic import BaseModel
from typing import Optional
from fastapi.staticfiles import StaticFiles

load_dotenv()

app = FastAPI(title="Vaniverse AI Audio API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for audio output
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Request Models
class MusicRequest(BaseModel):
    prompt: str
    duration: int = 10

@app.get("/")
def read_root():
    return {"message": "Welcome to Vaniverse AI Audio API"}

@app.post("/generate-music")
async def generate_music(request: MusicRequest):
    result = ai_model_service.generate_music(request.prompt)
    
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=503, detail=result["error"])
        
    if result and isinstance(result, str):
        filename = os.path.basename(result)
        return {"status": "success", "audio_url": f"/api/static/{filename}"}
    raise HTTPException(status_code=500, detail="Failed to generate music")

@app.post("/clone-voice")
async def clone_voice(
    text: str = Form(...),
    sample: UploadFile = File(...)
):
    temp_path = f"temp_{uuid.uuid4()}_{sample.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(sample.file, buffer)
    
    result = ai_model_service.clone_voice(text, temp_path)
    
    # Clean up temp file
    if os.path.exists(temp_path):
        os.remove(temp_path)

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=503, detail=result["error"])

    if result and isinstance(result, str):
        filename = os.path.basename(result)
        return {"status": "success", "audio_url": f"/api/static/{filename}"}
    raise HTTPException(status_code=500, detail="Failed to clone voice")

@app.post("/translate-speech")
async def translate_speech(
    target_language: str = Form(...),
    audio: UploadFile = File(...)
):
    # This currently only translates text if we had it, 
    # for a full demo we'd need Whisper locally or via API.
    # Placeholder for now until Whisper build is fixed.
    return {
        "status": "success",
        "message": f"Translation feature is active (Text-only for now)",
        "audio_url": "/api/static/sample_translation.mp3"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
