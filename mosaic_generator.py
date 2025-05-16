from PIL import Image
import numpy as np
import os

def resize_image(image, size):
    return image.resize(size, Image.Resampling.LANCZOS)


def average_color(image):
    np_img = np.array(image)
    w, h, d = np_img.shape
    return tuple(np_img.reshape(w * h, d).mean(axis=0))

def find_best_match(avg_color, fillers_avg):
    distances = [np.linalg.norm(np.array(avg_color) - np.array(f_avg)) for f_avg in fillers_avg]
    return np.argmin(distances)

def generate_photo_mosaic(target_img: Image.Image, filler_imgs: list[Image.Image], grid_size: int = 30) -> Image.Image:
    target_img = target_img.convert('RGB')
    filler_imgs = [img.convert('RGB') for img in filler_imgs]

    tile_w = target_img.width // grid_size
    tile_h = target_img.height // grid_size

    # Resize fillers to tile size and cache average color
    fillers_resized = [resize_image(img, (tile_w, tile_h)) for img in filler_imgs]
    fillers_avg = [average_color(img) for img in fillers_resized]

    result = Image.new('RGB', target_img.size)

    for i in range(grid_size):
        for j in range(grid_size):
            box = (j * tile_w, i * tile_h, (j + 1) * tile_w, (i + 1) * tile_h)
            region = target_img.crop(box)
            region_avg = average_color(region)
            match_idx = find_best_match(region_avg, fillers_avg)
            result.paste(fillers_resized[match_idx], box)

    return result
