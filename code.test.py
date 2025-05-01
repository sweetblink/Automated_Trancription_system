import whisper
model = whisper.load_model("small")
# result = model.transcribe("C:/Users/Admin/Whisper_project/test_files1.mp3")
result = model.transcribe("C:\Users\Admin\projects\Automated Transcription System\Whisper_project\thetestdata-sample-flac-15.flac")
print(result["text"])
# with open("C:\Users\Admin\projects\Automated Transcription System\Whisper_project", "w", encoding="utf-8") as f:
    # f.write(result["text"])