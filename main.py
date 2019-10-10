import argparse
import subprocess
import os
from PIL import Image
from Utility import *

parser = argparse.ArgumentParser(description="Smart camera CLI program")
parser.add_argument('--input', type=str, help='Input image path', default=os.path.join('Input', 'test.jpg'),
                    required=False)
parser.add_argument('--output', type=str, help='Output path', default=os.path.join('Output'), required=False)
parser.add_argument('--hist', type=str, help='Histogram equalization: [True,(False)]', default='false')
parser.add_argument('--colorize', type=str, help='Colorize old BW images: [True,(False)]', default='false')
parser.add_argument('--super', type=str, help='4X super resolution: [True,(False)]', default='false')
parser.add_argument('--enhance', type=str, help='Image enhancement: [True,(False)]', default='false')

args = parser.parse_args()
INPUT_PATH = args.input
OUTPUT_PATH = args.output
IS_HIST = str2bool(args.hist)
IS_COLORIZE = str2bool(args.colorize)
IS_SUPER = str2bool(args.super)
IS_ENHANCE = str2bool(args.enhance)

CURRENT_DIR = os.getcwd()

HIST_FILE = os.path.join(CURRENT_DIR, 'hist', 'main.py')
COLORIZE_FILE = os.path.join(CURRENT_DIR, 'colorize', 'test.py')
SUPER_FILE = os.path.join(CURRENT_DIR, 'super', 'test.py')
ENCHANCE_FILE = os.path.join(CURRENT_DIR, 'enhance', 'test.py')
PYTHON = 'python' if os.name == 'nt' else 'python3'
if not os.path.exists(INPUT_PATH):
    os.mkdir(INPUT_PATH)
if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)
if not os.path.isabs(INPUT_PATH):
    INPUT_PATH = os.path.join(CURRENT_DIR, INPUT_PATH)
if not os.path.isabs(OUTPUT_PATH):
    OUTPUT_PATH = os.path.join(CURRENT_DIR,OUTPUT_PATH)

subprocess.call(['cp', INPUT_PATH, os.path.join(OUTPUT_PATH, 'result.jpg')])

if IS_COLORIZE:
    subprocess.call(['cp', os.path.join(OUTPUT_PATH, 'result.jpg'), os.path.join('colorize', 'test2014'), ])
    subprocess.call([PYTHON, COLORIZE_FILE])
    subprocess.call(['cp', os.path.join(CURRENT_DIR,'colorize', 'summary', 'test', 'images', 'result.jpg'),os.path.join(OUTPUT_PATH, 'result.jpg')])
    CropColorizedImage(os.path.join(OUTPUT_PATH, 'result.jpg'),OUTPUT_PATH)

if IS_SUPER:
    subprocess.call(['cp', os.path.join(OUTPUT_PATH, 'result.jpg'), os.path.join('super', 'LR')])
    os.system('python super/test.py')
    # subprocess.call([PYTHON, SUPER_FILE])
    subprocess.call(['cp', os.path.join('super', 'results','result_rlt.png'),os.path.join(OUTPUT_PATH, 'result.jpg')])
if IS_HIST:
    subprocess.call([PYTHON, HIST_FILE, '--input', INPUT_PATH, '--output', OUTPUT_PATH])

if IS_ENHANCE:
    subprocess.call([PYTHON, './enhance/rgb2raw.py','--src_path',os.path.join(OUTPUT_PATH),'--dst_path',os.path.join(CURRENT_DIR, 'enhance','input'),'--n_folders','1','--read_noise','0'])
    subprocess.call(['sh',os.path.join('./test_tenet2-dn-df2k.sh')])
    subprocess.call(['cp', os.path.join('enhance', 'output', 'result.tiff'),os.path.join(OUTPUT_PATH, 'result.jpg')])