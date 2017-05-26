#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import json
import argparse
import logging

from datetime import datetime
from datetime import timedelta

from PIL import Image


def get_date_taken(img_path):
    return Image.open(img_path)._getexif()[36868]

def validate_time_intervals(datetime_array, threshold, validated_array):
    for i in range(len(datetime_array)-1):

        current_img_date = datetime_array[i]['result']
        current_img_date_parsed = datetime.strptime(current_img_date, '%Y:%m:%d %H:%M:%S')
        next_img_date = datetime_array[i+1]['result']
        next_img_date_parsed = datetime.strptime(next_img_date, '%Y:%m:%d %H:%M:%S')

        interval_difference = (next_img_date_parsed - current_img_date_parsed).total_seconds() / 60

        if interval_difference > threshold:
            validated_array.append({
                "current_img": datetime_array[i]['input_path'], 
                "current_time": datetime_array[i]['result'],
                "next_img": datetime_array[i+1]['input_path'],
                "next_time": datetime_array[i+1]['result'],
                "difference_sec": interval_difference,
                "Lag detected": True
                })
        else:
            validated_array.append({
            "current_img": datetime_array[i]['input_path'], 
            "current_time": datetime_array[i]['result'],
            "next_img": datetime_array[i+1]['input_path'],
            "next_time": datetime_array[i+1]['result'],
            "difference_sec": interval_difference,
            "Lag detected": False
            })

    return validated_array


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
    parser.add_argument("-t", "--threshold", dest='threshold', type=float, default=1, help="Seconds threshold")
    # options
    parser.add_argument("-v", "--verbose", dest='verbose', help='set logging level to debug', action="store_true")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    results_exif_datetimes = []
    validated_array = []
    results = []

    for input_path in find_images(args.input_dir):
 
        #Extracting exif       	
        try:
        	exif_date = get_date_taken(input_path)
        except Exception as e:
        	exif_date = str(e)

              
        results.append({"input_path": input_path, "result": exif_date})
        
    #Sorting results 
    results_sorted = sorted(results, key=lambda x: datetime.strptime(x['result'], '%Y:%m:%d %H:%M:%S'), reverse=False)

    #Validating time intervals
    result = validate_time_intervals(results_sorted, args.threshold, validated_array)

    logging.info("writing results to {0}".format(args.save_path))

    assert os.path.splitext(args.save_path)[1] == ".json"

    with open(args.save_path, 'w') as outfile:
        data = {"input_dir": args.input_dir, "results": result, "threshold": args.threshold}
        json.dump(data, outfile, sort_keys=True, indent=4)
        outfile.write("\n")