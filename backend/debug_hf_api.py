from gradio_client import Client
import sys

def debug_client(space_id):
    print(f"--- Debugging {space_id} ---")
    try:
        client = Client(space_id)
        print(f"Connected to {space_id}")
        # print(f"API info: {client.view_api()}")
        return client
    except Exception as e:
        print(f"Failed to connect to {space_id}: {e}")
        return None

if __name__ == "__main__":
    # music_client = debug_client("facebook/MusicGen")
    voice_client = debug_client("myshell-ai/OpenVoiceV2")
    
    if voice_client:
        print("\nTesting small prediction on Voice Client...")
        try:
            # We need a sample file for OpenVoice, but let's just see the api for now
            print(voice_client.view_api())
        except Exception as e:
            print(f"Error viewing API: {e}")
