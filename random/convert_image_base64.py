"""
example usage
python convert_image_base64.py --image="" --save=""
"""
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--image', required=True, type=str, 
                    help='Image to convert')
parser.add_argument('--save', required=True, type=str, 
                    help='Save Location')
args = parser.parse_args()

# unpack
image_location = args.image
save_location = args.save

import base64

with open(image_location, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

f = open(save_location,"wb")
f.write(encoded_string)
f.close()