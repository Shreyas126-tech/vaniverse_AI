from services.ai_model_service import ai_model_service
import sys

def test_music_gen():
    print("Testing music generation...")
    result = ai_model_service.generate_music("A cheerful acoustic guitar melody")
    if result:
        print(f"Music generation successful! Result saved at: {result}")
    else:
        print("Music generation failed.")

if __name__ == "__main__":
    test_music_gen()
