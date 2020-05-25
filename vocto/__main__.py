import argparse

from __init__ import *

parser = argparse.ArgumentParser(
    description='Create images from a VOC dataset')
parser.add_argument('--input_dir', '-i', default='./data', required=False)
parser.add_argument('--output_dir', '-o', default='./output', required=False)

args = parser.parse_args()

if __name__ == "__main__":
    write_images(get_dataset(args.input_dir),
                 args.output_dir)
