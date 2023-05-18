import os
import moviepy.editor as mp
import shutil
import re
import discord
import time
import traceback

from discord.ext import commands

from functions.image_downloader import download_images
from functions.tts import get_api_key, generate_tts
from functions.script import generate_script
from functions.extract import extract_info
from functions.write import write_files
from functions.zoom import zoom_in_effect
from functions.resize_images import resize_images
from functions.music import download_music

TOKEN = 'ODIwMTQ2NjIzMDk5MDQzODYx.G_rSrT.bROHLlYvMQo0ZNdOArKKtc8QpA8DxMjXJl8Pzk'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Define function to make video from images
def make_video(folder, output_filename, audio_file, music_file):
    image_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.png')]
    image_files = sorted(image_files)  # Sort the image file names
    num_images = len(image_files)
    clips = []

    audio_clip = mp.AudioFileClip(audio_file)
    music_clip = mp.AudioFileClip(music_file).volumex(0.05)
    total_duration = audio_clip.duration
    image_duration = total_duration / num_images

    for image_path in image_files:
        clip = mp.ImageClip(image_path, duration=image_duration).resize(height=1280, width=720)
        clip = zoom_in_effect(clip)  # Apply zoom-in effect
        clips.append(clip)

    final_clip = mp.concatenate_videoclips(clips, method="chain").set_position(("center", "center"))

    # Combine text-to-speech audio and background music
    audio = mp.CompositeAudioClip([audio_clip.set_start(0), music_clip.set_start(0)])
    final_clip = final_clip.set_audio(audio)
    final_clip = final_clip.set_duration(total_duration)
    final_clip = final_clip.resize(height=1280, width=720)
    final_clip = final_clip.set_position(("center", "center"))
    final_clip = final_clip.set_fps(24)

    try:
        final_clip.write_videofile(output_filename)
    except IndexError as e:
        print(f"An error occurred while writing the video, expected though, so continue on :)")

    return

progress_message = None
async def send_progress_message(channel, message):
    global progress_message

    if progress_message is None:
        progress_message = await channel.send(message)
    else:
        await progress_message.edit(content=message)

    if message == "Video Created Successfully!":
        progress_message = None


async def handle_error(channel, error):
    error_message = f"An error occurred while creating the video:\n```{error}```"
    await channel.send(error_message)


with open('prompt.txt', 'r') as f:
    gptprompt = f.read()

@bot.event
async def on_message(message):
    try:
        if message.content.startswith('!short'):
            apikey = get_api_key()
            print(f'Using API key: {apikey}')

            videoinput = message.content.split(' ')[1:]
            prompt = gptprompt + "" + ' '.join(videoinput)

            channel = message.channel
            await send_progress_message(channel, "Script Generation In Progress...")
            print('Generating Script...')
            script = generate_script(prompt)
            await send_progress_message(channel, "Script Generated!")
            print('Script Generated!')

            title, music, desc, tags, script = extract_info(script)
            await send_progress_message(channel, "Separated Information From Script!")
            print('Separated Information!')

            titlefix = re.sub(r'[^\w\s-]', '', title)

            await send_progress_message(channel, "Downloading Music...")
            music_file = download_music(music)
            await send_progress_message(channel, "Music Downloaded!")
            print('Music Downloaded!')
        
            write_files(titlefix, desc, tags)

            await send_progress_message(channel, "Generating Images...")
            folder = f'{titlefix}_images'
            while True:
                updated_script = download_images(script, folder)
                if updated_script == script:
                    break
                script = updated_script
            await send_progress_message(channel, "Images Generated!")

            # Resize images and add black padding
            resize_images(folder)
            await send_progress_message(channel, "Images Resized!")
            print('Images Resized!')

            await send_progress_message(channel, "Generating Text to Speech...")
            audio_file = generate_tts(script)
            print('Text to Speech Generated!')
            await send_progress_message(channel, "Text to Speech Generated!")

            # Make video from images and audio with background
            output_filename = f'{titlefix}.mp4'
            await send_progress_message(channel, "Creating video...")
            make_video(folder, output_filename, audio_file, music_file)
            await send_progress_message(channel, "Video Created Successfully!")
            print('Video created Successfully!')

            # Create a video folder
            if not os.path.exists(f'videos/{titlefix}'):
                os.makedirs(f'videos/{titlefix}')

            # Move files to video folder
            shutil.move(output_filename, f'videos/{titlefix}')
            shutil.move(f'{titlefix}_desc.txt', f'videos/{titlefix}')
            shutil.move(f'{titlefix}_tags.txt', f'videos/{titlefix}')
            print('Everything Moved to Videos Folder!')

            # Send files to Discord channel
            await channel.send(file=discord.File(f'videos/{titlefix}/{output_filename}'))
            await channel.send(f"Title: ```{title}```")
            await channel.send(f"Video Description: ```{desc}```")
            await channel.send(f"Video Tags: ```{tags}```")
            print('Sent Video to Discord!')

            # Delete downloaded images, audio file, and image folder
            for filename in os.listdir(folder):
                if filename.endswith('.png'):
                    os.remove(f'{folder}/{filename}')
            os.remove(audio_file)
            os.rmdir(folder)
            time.sleep(3)
            os.remove(music_file)
            print('Temporary Files Deleted!')
    except Exception as e:
        channel = message.channel
        error_traceback = traceback.format_exc()
        await handle_error(channel, error_traceback)

bot.run(TOKEN)