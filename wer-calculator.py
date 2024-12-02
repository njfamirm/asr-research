import jiwer
from openai_api import post_process_assistant
from openai import OpenAI
from os import getenv

transcriptFileName = 'avanegar'

with open('output/original.txt', 'r') as file:
    original = file.read()

# Open and read the second file
with open(f"output/{transcriptFileName}.txt", 'r') as file:
    transcrypt = file.read()

# client = OpenAI(api_key=getenv('OPENAI_API_KEY'))

# transcrypt = post_process_assistant(client, transcrypt).choices[0].message.content

print(transcrypt)

transforms = jiwer.Compose(
  [
    jiwer.ExpandCommonEnglishContractions(),
    jiwer.RemoveEmptyStrings(),
    jiwer.ToLowerCase(),
    jiwer.RemoveMultipleSpaces(),
    jiwer.Strip(),
    jiwer.RemovePunctuation(),
    jiwer.ReduceToListOfListOfWords(),
  ]
)

wer = jiwer.wer(
  original,
  transcrypt,
  truth_transform=transforms,
  hypothesis_transform=transforms,
)

accuracy = round(1 - wer, 2) * 100
print(f"Word Error Rate (WER): {wer}")
print(f"Accuracy: {accuracy}%")