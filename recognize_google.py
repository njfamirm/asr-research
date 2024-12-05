import os
import speech_recognition as sr
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from pydub import AudioSegment

def recognize_speech_from_audio_file(file_path):
    recognizer = sr.Recognizer()

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

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
        if "Bad Request" in str(e):
            print("Bad request error: Please check your audio file and try again.")
        else:
            print(f"Could not request results from Google Speech Recognition service; {e}")

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Hi! Send me a voice message or audio file, and I will recognize the speech.')

MIME_TYPE_TO_EXTENSION = {
    'audio/mpeg': 'mp3',
    'audio/ogg': 'ogg',
    'audio/wav': 'wav',
    'audio/x-wav': 'wav',
    'audio/x-m4a': 'm4a',
    'audio/mp4': 'm4a',
    # Add more mappings as needed
}

async def recognize_speech(update: Update, context: CallbackContext) -> None:
    recognizer = sr.Recognizer()
    # Determine if the message contains a voice, audio, or document file
    if update.message.voice:
        file_id = update.message.voice.file_id
        new_filename = 'temp_audio.ogg'
    elif update.message.audio:
        file_id = update.message.audio.file_id
        mime_type = update.message.audio.mime_type
        file_extension = MIME_TYPE_TO_EXTENSION.get(mime_type, mime_type.split('/')[-1])
        new_filename = f'temp_audio.{file_extension}'
    elif update.message.document:
        mime_type = update.message.document.mime_type
        if mime_type and mime_type.startswith('audio/'):
            file_id = update.message.document.file_id
            file_extension = MIME_TYPE_TO_EXTENSION.get(mime_type, mime_type.split('/')[-1])
            new_filename = f'temp_audio.{file_extension}'
        else:
            await update.message.reply_text("Please send an audio file.")
            return
    else:
        await update.message.reply_text("Please send a voice message or audio file.")
        return

    try:
        file = await context.bot.get_file(file_id)
        await file.download_to_drive(new_filename)
    except Exception as e:
        await update.message.reply_text(f"Failed to download file: {e}")
        return

    # Convert audio file to WAV
    try:
        audio = AudioSegment.from_file(new_filename)
        audio.export('temp_audio.wav', format='wav')
    except Exception as e:
        await update.message.reply_text(f"Failed to convert audio file: {e}")
        return

    with sr.AudioFile('temp_audio.wav') as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data, language="fa-IR")
        await update.message.reply_text(f'You said: {text}')
    except sr.UnknownValueError:
        await update.message.reply_text("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        if "Bad Request" in str(e):
            await update.message.reply_text("Bad request error: Please check your audio file and try again.")
        else:
            await update.message.reply_text(f"Could not request results from Google Speech Recognition service; {e}")
    except BrokenPipeError:
        await update.message.reply_text("Network error: Broken pipe. Please try again later.")

def main() -> None:
    application = Application.builder().token("2047905694:AAFZaZqTRc-9i1a3fq7Wr5vvim_CBeO7kFk").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, recognize_speech))

    application.run_polling()

if __name__ == "__main__":
    main()
