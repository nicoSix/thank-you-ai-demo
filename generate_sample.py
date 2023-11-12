import time
from typing import List, Tuple
import requests 
import inquirer

from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")

CHUNK_SIZE = 1024


def _get_available_voices() -> List[dict]:
  headers = {
    "accept": "application/json",
    "xi-api-key": config["API_KEY"]
  }

  get_response = requests.get(f"{config['API_URL']}/v1/voices", headers=headers)

  return [v for v in get_response.json()["voices"] if v["category"] == "cloned"]


def _select_parameters(voices: List[dict]) -> Tuple[dict, str]:
  questions = [
    inquirer.List(
        "mode",
        message="How do you want to use the program?",
        choices=["Free prompt", "Thanking"],
    ),
    inquirer.List(
        "voice",
        message="What voice to dub?",
        choices=[n["name"] for n in voices],
    )
  ]

  answers = inquirer.prompt(questions)

  if answers["mode"] == "Thanking":
      person = input("[?] Who should I thank?: ")
      prompt = f"{config['THANK_PROMPT_START']} {person} {config['THANK_PROMPT_END']}"
  else:
      prompt = input("[?] What should the voice say?: ")

  return [v for v in voices if v["name"] == answers["voice"]][0], prompt


def _query_voice_sample_from_prompt(prompt: str, voice: dict) -> None:
  headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": config["API_KEY"]
  }

  data = {
    "text": prompt,
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
      "stability": 0.3,
      "similarity_boost": 1,
      "style": 1
    }
  }

  ## Measuring time performance of text-to-speech API
  start_time = time.perf_counter()
  post_response = requests.post(f"{config['API_URL']}/v1/text-to-speech/{voice['voice_id']}", json=data, headers=headers)
  end_time = time.perf_counter()
  print("[!] Sample successfully generated in %.3fs" % round(end_time - start_time, 3))

  with open('result.mp3', 'wb') as f:
      for chunk in post_response.iter_content(chunk_size=CHUNK_SIZE):
          if chunk:
              f.write(chunk)

      print("[!] Success: result written in ./result.mp3")


if __name__ == '__main__':
  voices = _get_available_voices()
  selected_voice, prompt = _select_parameters(voices)
  _query_voice_sample_from_prompt(prompt, selected_voice)