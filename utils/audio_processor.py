import yt_dlp
from pydub import AudioSegment
import os

DOWNLOAD_DIR='downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


### This function convert the video to wav format

def download_youtube_audio(url:str) ->str:
    output_path=os.path.join(DOWNLOAD_DIR,"%(title)s.%(ext)s")
    ydl_opts={
        "format":"bestaudio/best",
        "outtmpl":output_path,
        "postprocessors":[
            {
                "key":"FFmpegExtractAudio",
                "preferredcodec":"wav",
                "preferredquality":"192",
            }
        ],
        "quiet":True,  ## can remove this if we want to see the downloading log bar of the video but preferrable for testing phase
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info=ydl.extract_info(url,download=True)
        filename=ydl.prepare_filename(info).replace(".webm",".wav").replace(".m4a",".wav")
    return filename




###some problems which might occurs are likly related to audio
# that is some of the video may use dual audio which i need to convert to mono audio then to wav format
# the difference of frequency of audio - i am using whishper which has high complatibality with 16 khz

def convert_to_wav(input_path:str)->str:
    """This converts any audio/video file to WAV format using pydub"""
    output_path=os.path.splitext(input_path)[0] + "_converted.wav"
    audio=AudioSegment.from_file(input_path)  ## this automatically detect the type of file such as. mp3,mp4
    audio=audio.set_channels(1).set_frame_rate(16000) ## this change the dual audio to mono audio in 16KHz
    audio.export(output_path,format="wav") ## save to WAV format
    return output_path



## to use wishper ai tool we add the above function , to make it simpler for the tool to use the data


##As we cannot process a large video or audio file at once that is why i am using chunk
# Chunk is meant by slicing the given data by a particular value or time frame
## For example slicing by 10 min each

def chunk_audio(wav_path:str,chunk_minutes : int =10 )-> list:  ## this meant that the chunk are created at each 10 *60*1000 step
    audio =AudioSegment.from_wav(wav_path)
    chunk_ms=chunk_minutes*60*1000 ## we use this calculation because the chunk are accessed in millisecond but we are getting the data in minutes thus to convert we use this 

    chunks=[]

    for i , start in enumerate(range(0,len(audio),chunk_ms)):  ## to take step at each miliseconds in length of audio and using the enumerate to separate the index from value
        chunk =audio[start:start+chunk_ms] 
        chunk_path=f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path,format="wav")

        chunks.append(chunk_path) ## this addd the above loop output to the chunks list

    return chunks



## to call the above function at once we add the below funciton
def process_input(source:str)->str:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected Youtube URL. Downloading audio...")
        wav_path=download_youtube_audio(source)
    else:
        print("Detecting local file, Converting to WAV...")
        wav_path=convert_to_wav(source)

    print("Chunking audio...")
    chunks=chunk_audio(wav_path)
    print(f"Audio ready - {len(chunks)} chunk(s) created.")
    return chunks