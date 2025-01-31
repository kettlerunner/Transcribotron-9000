# Audio Transcription Script

## Description
This script transcribes audio files (MP3 format) using OpenAI's Whisper model. It processes audio files located in a specified directory, splits them into manageable segments if needed, and generates Markdown files containing the transcriptions.

## Features
- Scans a specified directory for MP3 files.
- Splits large audio files into 10-minute segments.
- Uses OpenAI's Whisper model to transcribe audio.
- Saves transcriptions as Markdown (.md) files.

## Requirements
- Python 3.x
- OpenAI API Key
- Required Python packages:
  - `openai`
  - `pydub`

## Installation
1. Clone or download this repository.
2. Install the required dependencies using pip:
   ```sh
   pip install openai pydub python-docx
   ```
3. Ensure `ffmpeg` is installed (required by `pydub`).
   - On Ubuntu:
     ```sh
     sudo apt install ffmpeg
     ```
   - On MacOS (using Homebrew):
     ```sh
     brew install ffmpeg
     ```
   - On Windows, download and install FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html).
4. Set your OpenAI API key as an environment variable:
   ```sh
   export OPENAI_API_KEY='your-api-key-here'
   ```
   (For Windows, use `set OPENAI_API_KEY='your-api-key-here'` in Command Prompt.)

## Usage
1. Place MP3 files into the `meetings` directory.
2. Run the script:
   ```sh
   python script.py
   ```
3. The transcriptions will be saved as `.md` files in the same directory as the original audio files.

## File Structure
```
project_folder/
│-- script.py        # The transcription script
│-- meetings/        # Directory containing MP3 files
│-- meetings/segments/  # Generated audio segments
│-- transcriptions/  # Output folder for transcription (optional)
```

## Notes
- The script automatically creates a `segments` directory for audio chunks.
- Ensure your API key is valid and has access to OpenAI's Whisper model.
- If an audio file is too long, it is split into 10-minute segments to improve processing.

## License
This project is open-source and can be modified or distributed under the applicable license terms.

