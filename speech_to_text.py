import whisper
from summarizer import Summarizer

model = whisper.load_model("base")

# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio("audio.mp3")
audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio).to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
options = whisper.DecodingOptions()
result = whisper.decode(model, mel, options)

# print the recognized text
print(result.text)


# create the summarizer
summarizer = Summarizer()

# get the full text
full_text = result.text

# summarize the text
summary = summarizer(full_text, ratio=0.05)  # adjust the ratio as needed to get 100 words

# print the summary
print(summary)
