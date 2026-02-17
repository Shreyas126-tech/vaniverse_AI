from gradio_client import Client
import os

class AIModelService:
    def __init__(self):
        self.music_client = None
        self.voice_client = None
        self.initialize_clients()

    def initialize_clients(self):
        # Music Generation Client
        try:
            # Verified working public space
            self.music_client = Client("sanchit-gandhi/musicgen-streaming")
            print("Successfully connected to MusicGen Space")
        except Exception as e:
            print(f"Warning: Could not initialize MusicGen client: {e}")

        # Voice Cloning Client
        try:
            # Verified working public space
            self.voice_client = Client("myshell-ai/OpenVoiceV2")
            print("Successfully connected to OpenVoiceV2 Space")
        except Exception as e:
            print(f"Warning: Could not initialize Voice Cloning client: {e}")

    def generate_music(self, prompt: str):
        if not self.music_client:
            print("MusicGen client not initialized. Attempting re-initialization...")
            self.initialize_clients()
            if not self.music_client:
                return {"error": "Service temporarily unavailable. The AI music generation space is currently down."}

        try:
            # Using the verified API structure for sanchit-gandhi/musicgen-streaming
            result = self.music_client.predict(
                text_prompt=prompt,
                audio_length_in_s=15,
                play_steps_in_s=1.5,
                seed=42,
                api_name="/generate_audio"
            )
            return result
        except Exception as e:
            print(f"Music generation error: {e}")
            return {"error": f"Generation failed: {str(e)}"}

    def clone_voice(self, text: str, voice_sample_path: str):
        if not self.voice_client:
            print("Voice cloning client not initialized. Attempting re-initialization...")
            self.initialize_clients()
            if not self.voice_client:
                return {"error": "Voice cloning service is currently unavailable."}

        try:
            # Using the verified API structure for myshell-ai/OpenVoiceV2
            result = self.voice_client.predict(
                text=text,
                language="English",
                reference_audio=voice_sample_path,
                agree=True,
                api_name="/predict"
            )
            # The API returns a list [info_text, audio_obj, ref_audio_used]
            if isinstance(result, (list, tuple)) and len(result) > 1:
                # The audio result can be a path or a dict with 'name'
                audio_result = result[1]
                if isinstance(audio_result, dict):
                    return audio_result.get('name')
                return audio_result
            return result
        except Exception as e:
            print(f"Voice cloning error: {e}")
            return {"error": f"Cloning failed: {str(e)}"}

ai_model_service = AIModelService()
