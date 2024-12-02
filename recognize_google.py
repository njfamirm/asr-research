import speech_recognition as sr

def recognize_speech_from_audio_file(file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        print("Reading audio file...")
        audio = recognizer.record(source)

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio, language="fa-IR")
        print("You said: " + text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    recognize_speech_from_audio_file("./voice_01.wav")
