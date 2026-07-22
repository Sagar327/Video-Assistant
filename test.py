from utils.audio_processor import process_input
from Core.transcriber import transcribe_all

source=""

chunks=process_input(source)

print(transcribe_all(chunks))