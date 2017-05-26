#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import json
import argparse
import logging

import cv2
import numpy
import magic

from blur_detection import estimate_blur

from PIL import Image


def find_images(input_dir):
    extensions = [".jpg", ".png", ".jpeg"]

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if os.path.splitext(file)[1].lower() in extensions:
                yield os.path.join(root, file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='run blur detection on a single image')
    parser.add_argument('-i', '--input_dir', dest="input_dir", type=str, required=True, help="directory of images")
    parser.add_argument('-s', '--save_path', dest='save_path', type=str, required=True, help="path to save output")
    # parameters
    parser.add_argument("-t", "--threshold", dest='threshold', type=float, default=200.0, help="blurry threshold")
    # options
    parser.add_argument("-v", "--verbose", dest='verbose', help='set logging level to debug', action="store_true")
    parser.add_argument("-d", "--display", dest='display', help='display images', action="store_true")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    results = []

    for input_path in find_images(args.input_dir):

    	is_corrupted = False
    	is_blurred = False
    	img_info = ""
    	laplacian_score = ""

    	#Get Advanced image info
        try:
        	img_info = magic.from_file(input_path)
        except Exception as e:
        	img_info = str(e)

    	#Check for image basic corruption
        try:
        	img = Image.open(input_path) 
        	img.verify()
        	img = Image.open(input_path)       	
        	img.load()
        	logging.info("Input path: {0}, is_corrupted: {1}".format(input_path, is_corrupted))
        except Exception as e:
        	is_corrupted = str(e)
        	logging.info("Input path: {0}, is_corrupted: {1}".format(input_path, e))
        	results.append({"input_path": input_path, "laplacian_score": laplacian_score, "image_info": img_info, "is_corrupted": is_corrupted, "is_blurred": is_blurred})
        	continue

       	#Blurry check
        try:
            logging.info("processing {0}".format(input_path))
            input_image = cv2.imread(input_path)            

            blur_map, laplacian_score, is_blurred = estimate_blur(input_image, args.threshold)

            logging.info("input_path: {0}, laplacian_score: {1}, is_blurred: {2}".format(input_path, laplacian_score, is_blurred))

            if args.display:
                cv2.imshow("input", input_image)
                cv2.imshow("result", pretty_blur_map(blur_map))
                cv2.waitKey(0)
        except Exception as e:
            is_blurred = str(e)

        results.append({
        	"input_path": input_path, 
        	"laplacian_score": laplacian_score, 
        	"image_info": img_info, 
        	"is_corrupted": is_corrupted, 
        	"is_blurred": is_blurred, 
        	})

    logging.info("writing results to {0}".format(args.save_path))

    assert os.path.splitext(args.save_path)[1] == ".json"

    with open(args.save_path, 'w') as outfile:
        data = {"input_dir": args.input_dir, "threshold": args.threshold, "results": results}
        json.dump(data, outfile, sort_keys=True, indent=4)
        outfile.write("\n")