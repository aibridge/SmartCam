import argparse
import cv2
import os

parser = argparse.ArgumentParser(description="Equalize histogram")
parser.add_argument('--input', type= str, help='Input image path', required=True)
parser.add_argument('--output', type=str, help='Output image path', required=True)

args= parser.parse_args()
INPUT_PATH=args.input
OUTPUT_PATH= args.output

img = cv2.imread(INPUT_PATH,0)
img_equ = cv2.equalizeHist(img)
cv2.imwrite(os.path.join(OUTPUT_PATH,'result.jpg'),img_equ)