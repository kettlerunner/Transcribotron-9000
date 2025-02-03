# Audio Transcription Script

## Description
This script automates transcription of **video files** and **audio files** using OpenAI's Whisper model. It:

1. Scans the `videos` folder for common video formats and extracts the audio as MP3.  
2. Moves these MP3 files into the `meetings` folder.  
3. Splits each MP3 into 10-minute segments (if needed).  
4. Sends each segment to OpenAI Whisper for transcription.  
5. Saves the transcriptions as Markdown (`.md`) files alongside the MP3.

## Features
- Scans a specified `videos` directory for common video files (`.mp4`, `.mov`, `.mkv`, etc.).  
- Extracts audio and automatically places MP3 files in the `meetings` directory.  
- Optionally processes any existing MP3 files directly in `meetings`.  
- Splits large audio into 10-minute segments to avoid timeouts or memory issues.  
- Uses **OpenAI Whisper** for transcription via the OpenAI API.  
- Outputs transcripts as `.md` files, stored in the same location as the MP3.

## Requirements
- **Python 3.x**
- **OpenAI API Key**  
- **FFmpeg** (required by pydub for audio conversions)
- **Python packages**:
  - `openai`
  - `pydub`

You can install these packages via:
```bash
pip install openai pydub
```
*(The script also references `python-docx` in the old README, but it’s not used in the updated code. You can omit it if not needed.)*

### Installing FFmpeg
- On **Ubuntu**:
  ```bash
  sudo apt-get install ffmpeg
  ```
- On **macOS** (with Homebrew):
  ```bash
  brew install ffmpeg
  ```
- On **Windows**, download from [ffmpeg.org/download.html](https://ffmpeg.org/download.html) and ensure `ffmpeg.exe` is in your PATH.

## Setup
1. **Clone or download** this repository.  
2. **Set your OpenAI API key** as an environment variable:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   *On Windows (Command Prompt):*
   ```bash
   set OPENAI_API_KEY="your-api-key-here"
   ```
3. Verify your directory structure:
   ```
   project_folder/
   ├── script.py         # The main transcription script
   ├── videos/           # Directory containing video files
   ├── meetings/         # Directory to store extracted MP3s and final transcripts
   └── ...
   ```

## Usage
1. **Place your video files** (e.g., `.mp4`, `.mov`, `.mkv`) into the `videos` folder.  
   - The script will extract their audio into the `meetings` folder.  
2. **(Optional)** If you already have MP3 files you want to transcribe, place them in `meetings` instead of `videos`.  
3. **Run the script**:
   ```bash
   python script.py
   ```
4. **Monitor output** as the script:
   - Extracts audio from each video into MP3 format  
   - Splits MP3s into 10-minute chunks  
   - Transcribes each chunk using OpenAI  
   - Creates `.md` files containing the complete transcript

When complete, each MP3 in the `meetings` folder will have a corresponding `.md` file with the transcription text.

## File Structure
After running, you might see:
```
project_folder/
├── script.py
├── videos/
│   ├── my_video.mp4
│   └── ...
├── meetings/
│   ├── my_video.mp3
│   ├── my_video.md
│   └── segments/
│       ├── my_video_10.mp3
│       ├── my_video_20.mp3
│       └── ...
└── ...
```
- **`videos/`**: Original video files.  
- **`meetings/`**: Extracted MP3 files, plus `.md` transcripts.  
- **`meetings/segments/`**: Subfolder containing the 10-minute chunked segments.

## Notes
- Ensure your **OpenAI API key** is valid and Whisper access is available.
- If a single audio file exceeds 10 minutes, it’s automatically split into smaller segments to improve processing reliability.
- You can adjust the **segment length** or the **video file extensions** recognized in the script as needed.
- To avoid clutter, the script stores segment files in a `segments` folder inside `meetings`.

## License
This project is open-source and can be modified or distributed under the applicable license terms. Feel free to adapt it to your workflow needs.
