import whisper
import os

audio_file_path = os.path.abspath(r"C:\Users\HP\Documents\EPITA S3\Action Learning\music-source-separation\model\test.mp3")

model = whisper.load_model("base")
result = model.transcribe(audio_file_path,fp16=False, verbose = True)


