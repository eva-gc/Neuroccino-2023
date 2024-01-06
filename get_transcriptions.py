import sys
import os
import whisper
from moviepy.editor import *


def get_transcriptions(folder_path):
    selected_episodes = []
    with open("2023_neuroccinos_id.txt", "r") as txt_file:
        file_ids= txt_file.read().split(',')

        for filename in os.listdir(folder_path):
            for file_id in file_ids:
                if filename.startswith(file_id) and filename.endswith(".mp4"):
                    selected_episodes.append(os.path.join(folder_path, filename))

    for episode in selected_episodes:
        print(episode)
        audio_file = extract_audio(episode)
        transcribe(audio_file)

def extract_audio(input_file):
    output_file = os.path.splitext(input_file)[0] + ".wav"
    file_extension = os.path.splitext(input_file)[1].lower()

    if not os.path.isfile(output_file):
        video = VideoFileClip(input_file)
        video.audio.write_audiofile(output_file, codec="pcm_s16le", verbose=False)
        print(f"File was converted to audio")
    
    return output_file

def transcribe(audio_file):
    if not os.path.isfile(os.path.splitext(audio_file)[0] + ".txt"):
        model = whisper.load_model("small")
        print(f"Starting transcription...")
        result = model.transcribe(audio_file)
        print(f"Transcription done")
        text_output = result["text"]
        save_transcription_to_txt(audio_file, text_output)

def save_transcription_to_txt(audio_file, text):
     txt_file_path = os.path.splitext(audio_file)[0] + ".txt"
     with open(txt_file_path, "w") as txt_file:
         txt_file.write(text)
     print(f"Transcription saved")

if __name__ == "__main__":
    folder_path = './' #Enter path with files named by video id
    get_transcriptions(folder_path)