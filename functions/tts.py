import random
from elevenlabs import generate, save, set_api_key

def get_api_key():
    apikeys_file = "packages/11Labs/apikeys.txt"
    with open(apikeys_file, "r") as f:
        apikeys = [line.strip() for line in f]
    apikey = random.choice(apikeys)
    set_api_key(apikey)
    return apikey
    
def generate_tts(script, audio_file='tts.mp3'):
    audio = generate(
      text=script,
      voice="Bella",
      model="eleven_monolingual_v1"
    )
    save(audio, audio_file)
    return audio_file