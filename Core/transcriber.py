import whisper
import os

WHISPER_MODEL= os.getenv("WHISPER_MODEL","small")

_model=None

def load_model():

    global _model

    if _model is None:
        print(f"loading model ...")
        _model=whisper.load_model(WHISPER_MODEL)
        print("whisper model loaded successfully")

    return _model

def transcribe_chunk(chunk_path:str,translate:bool=False): ## we use translate bool as false because it will be default value from use whether he want to translate the audio
                      #this is for single chunk
    model=load_model()

    task="translate" if translate else "transcribe" #if user give translate as true then return "translate" else if user give false then return "transcribe"

    result=model.transcribe(chunk_path,task=task) # this is function of model which is part of whisper

    return result['text']


def transcribe_all(chunks:list,translate:bool=False)->str:


    full_transcript=""

    for i,chunk in enumerate(chunks): #separate i for index and chunk for chunk
        print(f"Transcribing chunk {i+1}")
        text=transcribe_chunk(chunk,translate=translate)

        full_transcript+=text+" "

    print("Transcription Completed")

    return full_transcript

