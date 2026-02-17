from huggingface_hub import HfApi
import sys

def find_musicgen_spaces():
    api = HfApi()
    print("Searching for MusicGen spaces...")
    try:
        spaces = api.list_spaces(search="MusicGen", sort="likes", direction=-1, limit=10)
        for space in spaces:
            print(f"Space: {space.id}, Likes: {space.likes}, Status: {getattr(space, 'runtime', 'N/A')}")
    except Exception as e:
        print(f"Error searching spaces: {e}")

if __name__ == "__main__":
    find_musicgen_spaces()
