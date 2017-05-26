# Img Detection
According to requirements:
- Blurry image detection: Given a set of photos, show how many are blurry
- Verify metadata in photos: Given a set of photos, validate the capture time intervals
- JPG validation: Given a set of photos, show how many are corrupt/invalid

The repository has two main scripts, `blurry_corrupted_validation.py` and `intervals_validation.py`, which
use OpenCV, numpy, ExifRead, python-magic libraries to process images

```bash
# processing a blurred or damaged files
python blurry_corrupted_validation.py -i blurry_set/ -s blurry_corrupted_results.json -t 250

# validating time intervals
python intervals_validation.py -i intervals_set/ -s results_intervals.json -t 2
```

The `blurry_corrupted_validation.py` script produces a json file with current image information and status.

```json
{
    "input_dir": "blurry_set/", 
    "results": [
        {
            "image_info": "JPEG image data, JFIF standard 1.02, resolution (DPI), density 72x72, segment length 16, Exif Standard: [TIFF image data, little-endian, direntries=14, height=9899, bps=182, compression=LZW, PhotometricIntepretation=RGB, orientation=upper-left, width=14824], baseline, precision 8, 14824x9899, frames 3", 
            "input_path": "blurry_set/san_rafael_rock_quarry_orthophoto_2016_10_0MotionBlur.jpg", 
            "is_blurred": true, 
            "is_corrupted": false, 
            "laplacian_score": 1.3622026771118867
        }, 
        {
            "image_info": "data", 
            "input_path": "blurry_set/some_corrupted_image.jpg", 
            "is_blurred": false, 
            "is_corrupted": "cannot identify image file 'blurry_set/some_corrupted_image.jpg'", 
            "laplacian_score": ""
        }
    ], 
    "threshold": 250.0
}
```
The `intervals_validation.py` script produces a json file with current information about capture time intervals.

```json
{
    "input_dir": "intervals_set/", 
    "results": [
        {
            "Lag detected": true, 
            "current_img": "intervals_set/IMG_20170526_093848.jpg", 
            "current_time": "2017:05:26 09:38:49", 
            "difference_sec": 2.5166666666666666, 
            "next_img": "intervals_set/IMG_20170526_094120.jpg", 
            "next_time": "2017:05:26 09:41:20"
        }, 
        {
            "Lag detected": true, 
            "current_img": "intervals_set/IMG_20170526_094120.jpg", 
            "current_time": "2017:05:26 09:41:20", 
            "difference_sec": 7.7, 
            "next_img": "intervals_set/IMG_20170526_094901.jpg", 
            "next_time": "2017:05:26 09:49:02"
        }
    ], 
    "threshold": 2.0
}
```