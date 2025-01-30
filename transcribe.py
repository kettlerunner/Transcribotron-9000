import os, re
from openai import OpenAI
from pydub import AudioSegment
from docx import Document

# Retrieve the API key from the environment variable
api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

def list_files_and_transcribe(directory):
    # Iterate through all files in directory
    for entry in os.listdir(directory):
        full_path = os.path.join(directory, entry)
        # If entry is a file and has mp3 extension
        if os.path.isfile(full_path) and full_path.lower().endswith('.mp3'):
            transcribe_audio(full_path, directory)

def transcribe_audio(file_path, directory):
    # Load the mp3 file
    audio = AudioSegment.from_mp3(file_path)
    segment_length = 10 * 60 * 1000  # 10 minutes in milliseconds

    # Create or use existing 'segments' subdirectory
    segments_dir = os.path.join(directory, "segments")
    if not os.path.exists(segments_dir):
        os.makedirs(segments_dir)

    # Split the file into segments and save them
    segment_paths = []
    for i in range(0, len(audio), segment_length):
        segment = audio[i:i + segment_length]
        segment_name = f"{os.path.splitext(os.path.basename(file_path))[0]}_{int(i / segment_length) + 1 * 10}.mp3"
        segment_path = os.path.join(segments_dir, segment_name)
        segment.export(segment_path, format='mp3')
        segment_paths.append(segment_path)

    # Transcribe each segment and write to Markdown file
    markdown_content = []
    for segment_path in segment_paths:
        with open(segment_path, 'rb') as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
            markdown_content.append(transcription.text)

    # Create Markdown file with the same name as the mp3 file
    markdown_file_path = os.path.splitext(file_path)[0] + '.md'
    transcript = ""
    with open(markdown_file_path, 'w', encoding='utf-8') as md_file:
        for segment_text in markdown_content:
            transcript += segment_text + '\n\n'
            md_file.write(segment_text + '\n\n')
    

# Specify the 'meetings' directory
meetings_directory = 'meetings'

# Start processing and transcribing
list_files_and_transcribe(meetings_directory)

# Let the user know we're done
print("Done")