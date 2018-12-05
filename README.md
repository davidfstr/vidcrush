# vidcrush

Reencodes the specified input video file, reducing the video size, by default at 1/2 width and height.

## Requirements

* Python 3.6+
* macOS 10.14+
* HandBrakeCLI, installed in `/Applications`

## Install

* Clone this repository.
* Open a terminal and `cd` to this repository's directory.
* `pip3 install -r requirements.txt`
* Add this repository to your `$PATH` variable so that `vidcrush.py` can be run from anywhere.

## Usage

```
$ vidcrush.py --help
usage: vidcrush.py [-h] [-s SCALE] [-r] video_filepaths [video_filepaths ...]

Reencode video files at a smaller size.

positional arguments:
  video_filepaths

optional arguments:
  -h, --help            show this help message and exit
  -s SCALE, --scale SCALE
                        fraction to multiply the original video dimensions by
  -r, --replace         replaces the original video file
```

The output video will be scaled to 50% the original size.

The output video will be put in the same directory as the input video with a suffix reflecting how much the video was scaled down. For example a input `video.mp4` would generate an output `video-0.5.mp4` by default.

If `--replace` is specified then the input video will be replaced with the output video, with the input video moved to the trash (or recycle bin).

## Running Tests

There aren't any tests yet but you can run the typechecker using:

```
make
```
