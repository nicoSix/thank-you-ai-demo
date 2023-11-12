# "Thank you!" AI demo

## Summary

A Python script to thank someone for something, using a voice AI API.

This script will : 
- query available cloned voices on the voice AI API (chosen service is ElevenLabs)
- allow the user to select the desired voice
- generate a .mp3 file based on the chosen prompt and voice then save it into result.mp3

NOTE: this script does not handle cloned voice model generation, which can be done on the ElevenLabs dashboard.

## Setup

1. Install required dependencies: inquirer and python-dotenv
2. Setup .env variables
  - API_URL: the ElevenLabs endpoint
  - API_KEY: your secret API key to query the API
  - THANK_PROMPT_START: the beginning of your prompt
  - THANK_PROMPT_END: the end of your prompt
3. Run the script:

  `
    python3 ./generate_sample.py
  `
