from gradio_client import Client
import sys

SPACES = [
    "facebook/musicgen-large",
    "facebook/musicgen-medium",
    "facebook/musicgen-small",
    "facebook/musicgen-melody",
    "facebook/audiogen-medium",
    "myshell-ai/OpenVoiceV2",
    "myshell-ai/OpenVoice",
    "amansrivastava/MusicGen",
    "suno/bark-gradio",
]

def test_spaces():
    for space in SPACES:
        print(f"Testing space: {space}...")
        try:
            client = Client(space)
            print(f"  Successfully connected to {client.src}")
            return space
        except Exception as e:
            print(f"  Failed: {str(e)[:100]}...")
    return None

if __name__ == "__main__":
    working_space = test_spaces()
    if working_space:
        print(f"\nRecommended working space: {working_space}")
    else:
        print("\nNo working spaces found.")
