import os
import re
from openai import OpenAI
from pydub import AudioSegment

# 1) Initialize OpenAI
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# 2) Function to extract MP3 audio from each video in 'videos' folder
def extract_audio_from_videos(video_directory, meetings_directory):
    # Create the meetings folder if it doesn't exist
    if not os.path.exists(meetings_directory):
        os.makedirs(meetings_directory)

    # Common video file extensions; adjust as needed
    video_extensions = ('.mp4', '.mov', '.mkv', '.avi', '.wmv', '.flv')
    
    # List all files in video_directory that match video_extensions
    videos = [
        f for f in os.listdir(video_directory)
        if os.path.isfile(os.path.join(video_directory, f)) and f.lower().endswith(video_extensions)
    ]
    
    if not videos:
        print(f"No video files found in '{video_directory}'.")
        return
    
    print(f"Found {len(videos)} video file(s) in '{video_directory}'. Extracting audio now...\n")

    for filename in videos:
        full_path = os.path.join(video_directory, filename)
        print(f"  - Extracting audio from '{filename}'")
        
        # Load the video file via pydub
        audio_segment = AudioSegment.from_file(full_path)
        
        # Build an output MP3 path in the meetings folder
        mp3_filename = os.path.splitext(filename)[0] + ".mp3"
        mp3_out_path = os.path.join(meetings_directory, mp3_filename)
        
        # Export audio to MP3
        audio_segment.export(mp3_out_path, format="mp3")
        print(f"    -> Saved MP3 to '{mp3_out_path}'\n")

    print("Audio extraction complete.\n")

# 3) Main transcription function 
def list_files_and_transcribe(directory):
    """
    Finds all MP3 files in the given directory, chunks them,
    transcribes each chunk using OpenAI, and writes the transcript to Markdown.
    """
    # Gather .mp3 files
    mp3_files = [
        f for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f)) and f.lower().endswith('.mp3')
    ]
    
    if not mp3_files:
        print(f"No MP3 files found in '{directory}'.")
        return

    print(f"Found {len(mp3_files)} MP3 file(s) in '{directory}' to process:\n")
    for mp3_file in mp3_files:
        full_path = os.path.join(directory, mp3_file)
        print(f"  -> Processing MP3: '{mp3_file}'")
        transcribe_audio(full_path, directory)
        print(f"     Finished processing '{mp3_file}'\n")


def transcribe_audio(file_path, directory):
    """
    Splits the MP3 into 10-minute segments, sends each to OpenAI for transcription,
    and writes all segment texts to a Markdown file.
    """
    # Load the mp3 file
    print("    Loading MP3 audio...")
    audio = AudioSegment.from_mp3(file_path)
    segment_length = 10 * 60 * 1000  # 10 minutes in milliseconds

    # Create or use existing 'segments' subdirectory
    segments_dir = os.path.join(directory, "segments")
    if not os.path.exists(segments_dir):
        os.makedirs(segments_dir)

    # Split the file into segments and save them
    print("    Splitting into 10-minute segments...")
    segment_paths = []
    total_length = len(audio)
    index = 0

    while index < total_length:
        segment_end = min(index + segment_length, total_length)
        segment = audio[index:segment_end]
        
        # By default, each chunk is named: originalFileName_<chunkIndex>.mp3
        # The code below adds '+1*10' which sets the chunk number to 10, 20, 30, etc.
        chunk_index = (index // segment_length + 1) * 10

        segment_name = f"{os.path.splitext(os.path.basename(file_path))[0]}_{chunk_index}.mp3"
        segment_path = os.path.join(segments_dir, segment_name)
        
        segment.export(segment_path, format='mp3')
        segment_paths.append(segment_path)
        
        index += segment_length

    print(f"    Created {len(segment_paths)} segment(s) in '{segments_dir}'.\n")

    # Transcribe each segment and write to Markdown file
    print("    Transcribing segments with OpenAI...")
    markdown_content = []
    for idx, segment_path in enumerate(segment_paths, start=1):
        print(f"      - Transcribing segment {idx}/{len(segment_paths)}: '{os.path.basename(segment_path)}'")
        with open(segment_path, 'rb') as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            segment_text = transcription.text
        markdown_content.append(segment_text)

    print("    Finished transcribing all segments.\n")

    # Create Markdown file with the same base name as the MP3 file
    markdown_file_path = os.path.splitext(file_path)[0] + '.md'
    print(f"    Writing transcript to '{markdown_file_path}'...")
    with open(markdown_file_path, 'w', encoding='utf-8') as md_file:
        for segment_text in markdown_content:
            md_file.write(segment_text + '\n\n')

    print(f"    Done writing transcript for '{os.path.basename(file_path)}'.\n")

# 4) Run everything
if __name__ == '__main__':
    videos_directory = 'videos'
    meetings_directory = 'meetings'

    print("Starting audio extraction from video files...\n")
    extract_audio_from_videos(videos_directory, meetings_directory)

    print("Starting transcription of all MP3 files in the meetings folder...\n")
    list_files_and_transcribe(meetings_directory)

    print("\nAll steps complete. Program finished.")
