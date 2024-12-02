import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

# transcribe audio
def transcribe_audio(client, audio_path):
  with open(audio_path, 'rb') as audio_data:
    logger.info('Starting transcription...')
    transcription = client.audio.transcriptions.create(model="whisper-1", file=audio_data, language="fa", prompt='')
    logger.info('Transcription completed.')
    return transcription.text

# post-process assistant
def post_process_assistant(client, full_transcript):
  system_prompt = """You are a helpful assistant that's corrects spelling mistakes. Avoid changing the words or sentence structure. If necessary, use a Persian dictionary to identify ambiguous words. """
  logger.info('Starting punctuation...')
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    temperature=0,
    messages=[
      {
        "role": "system",
        "content": system_prompt
      },
      {
        "role": "user",
        "content": full_transcript
      }
    ]
  )
  logger.info('Post-process completed.')
  return response
