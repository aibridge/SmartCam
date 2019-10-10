from PIL import Image
import os
import argparse

def CropColorizedImage(inputPath, outputPath):

    im = Image.open(inputPath)
    width, height = im.size   # Get dimensions
    new_width=width/3

    left = new_width
    top = 0
    right = (width - new_width)
    bottom = height

    # Crop the center of the image
    im = im.crop((left, top, right, bottom))
    im.save(os.path.join(outputPath,'result.jpg'))

def str2bool(v: str) -> bool:
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')