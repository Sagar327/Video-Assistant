from dotenv import load_dotenv
load_dotenv()

from utils.audio_processor import process_input
from Core.transcriber import transcribe_all
import os
print("KEY LOADED:", os.getenv("SARVAM_API_KEY"))
print("CWD:",os.getcwd())

source="https://www.youtube.com/watch?v=tplWXd_T7YQ"
language="hinglish" # change to hinglish to test sarvam

chunks=process_input(source)
transcript=transcribe_all(chunks,language=language)

print("\n=== TRANSCRIPT ===\n")
print(transcript)