import os
import requests
from PIL import Image

def download_images(script, folder):
    i = 1
    while True:
        if f'[Image: ' not in script:
            break
        img_desc = script.split(f'[Image: ')[1].split(']')[0]
        img_url = 'http://132.145.62.136:5000/generateportrait'
        img_data = {'text': img_desc}
        response = requests.post(img_url, json=img_data)
        img_url = response.json()['url']
        img_data = requests.get(img_url).content
        os.makedirs(folder, exist_ok=True)
        with open(f'{folder}/{i}.webp', 'wb') as handler:
            handler.write(img_data)
        webp_image = Image.open(f'{folder}/{i}.webp')
        png_image = webp_image.convert('RGBA')
        png_image.save(f'{folder}/{i}.png', 'PNG')
        os.remove(f'{folder}/{i}.webp')
        
        # Remove the [Image: {img_desc}] part from the script
        script = script.replace(f'[Image: {img_desc}]', '')
        
        print(f'Image {i} Generated!')
        i += 1
    return script