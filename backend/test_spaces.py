from gradio_client import Client
import sys

SPACES = [
    "facebook/MusicGen",
    "facebook/audiogen-medium",
    "fffiloni/OpenVoice-v2",
    "myshell-ai/OpenVoiceV2",
    "facebook/MusicGen-Large",
    "enzostvs/musicgen-songwriter"
]

def test_spaces():
    for space in SPACES:
        print(f"Testing space: {space}...")
        try:
            client = Client(space)
            print(f"  Successfully connected to {space}")
            # Try a very short generation to confirm it works
            # result = client.predict("A short beat", "", fn_index=0)
            # print(f"  Generation successful: {result}")
            # return space
        except Exception as e:
            print(f"  Failed to connect to {space}: {e}")
    return None

if __name__ == "__main__":
    working_space = test_spaces()
    if working_space:
        print(f"\nRecommended working space: {working_space}")
    else:
        print("\nNo working spaces found.")
