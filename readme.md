# Automated Transcription System

## Description
The **Automated Transcription System** is an application designed to transcribe audio and video files into text. The system uses **OpenAI's Whisper model** for automatic transcription of media files. It can extract audio from video files and perform real-time transcription on newly added files in a specific directory. This project aims to make transcription easier and more efficient, especially for users working with large amounts of media content.The Samples files used in this project are Ai generated.

### Key Features:
- **Audio Extraction**: Automatically extracts audio from video files.
- **Real-time Transcription**: Uses the Whisper model to transcribe audio to text in real-time.
- **File Monitoring**: Monitors a specific directory for new media files and processes them automatically.
- **Format Support**: Supports common audio and video formats, including `.mp3`, `.wav`, `.mp4`, `.mkv`, `.avi`, etc.

## Tech Stack
- **Python**: The core language used for implementation.
- **Whisper**: OpenAI's Whisper model for automatic transcription.
- **ffmpeg**: Used for extracting audio from video files.
- **Watchdog**: Monitors the specified directory for new files and triggers processing.
- **JSON**: Stores information about processed files to avoid re-processing.
  
### Requirements:
- Python 3.x
- ffmpeg (for audio extraction)
- Whisper model (for transcription)


Future Scope
Multiple Language Support: Implement transcription for multiple languages using the Whisper model.

Web Interface: Create a simple web interface where users can upload their media files for transcription.

Audio Enhancement: Implement audio enhancement techniques to improve transcription accuracy.

Batch Processing: Enable batch processing of multiple files at once, with an option to upload and transcribe in bulk.

Cloud Integration: Allow users to upload files directly from cloud storage services (e.g., Google Drive, AWS S3) and get transcriptions.