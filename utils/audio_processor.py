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


data=download_youtube_audio("https://www.youtube.com/watch?v=7HSSR1n8dgc")


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

print(convert_to_wav(data))