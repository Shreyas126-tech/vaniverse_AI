from gradio_client import Client
import sys

SPACES = [
    "facebook/MusicGen",
    "facebook/musicgen-large",
    "facebook/musicgen-medium",
    "facebook/musicgen-small",
    "nateraw/musicgen",
    "voodoohop/musicgen-voodoohop",
    "grand-marnier/MusicGen",
    "declare-lab/mustango"
]

def test_musicgen():
    for space in SPACES:
        print(f"Testing MusicGen space: {space}...")
        try:
            client = Client(space)
            print(f"  Successfully connected to {space}")
            return space
        except Exception as e:
            print(f"  Failed: {str(e)[:100]}...")
    return None

if __name__ == "__main__":
    working_space = test_musicgen()
    if working_space:
        print(f"\nRecommended working space: {working_space}")
    else:
        print("\nNo working MusicGen spaces found.")
