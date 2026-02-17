import os
import requests
import uuid
import time

# Use the router URL or the api-inference URL. 
# router.huggingface.co is the new standard for serverless inference.
# If it requires token, we can try api-inference.huggingface.co which also might, but acts differently.
# However, previous logs showed 503 on router, so it IS accessible but loading.
HF_API_URL = "https://router.huggingface.co/hf-inference/models"
HF_TOKEN = os.environ.get("HF_TOKEN")

def _headers():
    h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    if HF_TOKEN:
        h["Authorization"] = f"Bearer {HF_TOKEN}"
    return h

class AIModelService:
    def __init__(self):
        # Music model on HF Inference API (serverless)
        self.music_model = "facebook/musicgen-small"
        # TTS model for voice cloning fallback
        self.tts_model = "facebook/mms-tts-eng"
        print(f"AI Service initialized. HF_TOKEN set: {bool(HF_TOKEN)}")

    def initialize_clients(self):
        pass # Not needed for REST API

    def generate_music(self, prompt: str, retries: int = 15):
        if not HF_TOKEN:
             # Depending on the model, it might require a token. 
             # We try regardless, but if it fails with auth error, we know why.
             pass

        url = f"{HF_API_URL}/{self.music_model}"
        payload = {"inputs": prompt}

        for attempt in range(retries + 1):
            try:
                print(f"[MusicGen] Attempt {attempt+1}: calling {url}")
                resp = requests.post(url, headers=_headers(), json=payload, timeout=120)

                # Check for HTML (login page) usually indicates auth needed
                if "text/html" in resp.headers.get("Content-Type", ""):
                    print("[MusicGen] Received HTML response (likely login page). Token required.")
                    return {"error": "Hugging Face API Token required. Please set HF_TOKEN in environment."}

                if resp.status_code == 503:
                    body = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
                    wait = body.get("estimated_time", 20)
                    print(f"[MusicGen] Model loading, waiting {wait}s...")
                    time.sleep(min(wait, 30))
                    continue
                
                if resp.status_code in [401, 403]:
                    return {"error": "Hugging Face API Token invalid or missing."}

                if resp.status_code != 200:
                    error_text = resp.text[:300]
                    print(f"[MusicGen] Error {resp.status_code}: {error_text}")
                    if attempt < retries:
                        time.sleep(5)
                        continue
                    return {"error": f"Music generation failed (HTTP {resp.status_code}). The model may be unavailable."}

                # Success — response body is raw audio bytes (FLAC usually)
                output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
                os.makedirs(output_dir, exist_ok=True)
                # Ensure .flac extension as MusicGen usually returns FLAC
                filename = f"music_{uuid.uuid4()}.flac"
                filepath = os.path.join(output_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(resp.content)
                print(f"[MusicGen] Success! Saved to {filepath} ({len(resp.content)} bytes)")
                return filepath

            except requests.exceptions.Timeout:
                print(f"[MusicGen] Timeout on attempt {attempt+1}")
                if attempt < retries:
                    continue
                return {"error": "Music generation timed out. Please try again."}
            except Exception as e:
                print(f"[MusicGen] Unexpected error: {e}")
                return {"error": f"Generation failed: {str(e)}"}

        return {"error": "Music generation failed after retries."}

    def clone_voice(self, text: str, voice_sample_path: str, retries: int = 5):
        url = f"{HF_API_URL}/{self.tts_model}"
        payload = {"inputs": text}

        for attempt in range(retries + 1):
            try:
                print(f"[TTS] Attempt {attempt+1}: calling {url}")
                resp = requests.post(url, headers=_headers(), json=payload, timeout=60)

                if resp.status_code == 503:
                    body = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
                    wait = body.get("estimated_time", 20)
                    print(f"[TTS] Model loading, waiting {wait}s...")
                    time.sleep(min(wait, 30))
                    continue

                if resp.status_code != 200:
                    error_text = resp.text[:300]
                    print(f"[TTS] Error {resp.status_code}: {error_text}")
                    if attempt < retries:
                        time.sleep(5)
                        continue
                    return {"error": f"Voice generation failed (HTTP {resp.status_code})."}

                output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
                os.makedirs(output_dir, exist_ok=True)
                filename = f"clone_{uuid.uuid4()}.flac"
                filepath = os.path.join(output_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(resp.content)
                print(f"[TTS] Success! Saved to {filepath} ({len(resp.content)} bytes)")
                return filepath

            except requests.exceptions.Timeout:
                print(f"[TTS] Timeout on attempt {attempt+1}")
                if attempt < retries:
                    continue
                return {"error": "Voice generation timed out. Please try again."}
            except Exception as e:
                print(f"[TTS] Unexpected error: {e}")
                return {"error": f"Cloning failed: {str(e)}"}

        return {"error": "Voice generation failed after retries."}

ai_model_service = AIModelService()
