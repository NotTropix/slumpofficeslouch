from PIL import Image, ImageOps
import os

def resize_images(folder):
    for filename in os.listdir(folder):
        if filename.endswith('.png'):
            with Image.open(f'{folder}/{filename}') as im:
                width, height = im.size
                if height > width:
                    new_height = 1280
                    new_width = int((new_height/height)*width)
                    im_resized = im.resize((new_width, new_height))
                else:
                    new_width = 720
                    new_height = int((new_width/width)*height)
                    im_resized = im.resize((new_width, new_height))
                # Add black padding
                left = int((720 - new_width) / 2)
                right = 720 - new_width - left
                top = int((1280 - new_height) / 2)
                bottom = 1280 - new_height - top
                im_padded = ImageOps.expand(im_resized, border=(left, top, right, bottom), fill='black')
                im_padded.save(f'{folder}/{filename}')
