# vidcrush

Reencodes the specified input video file so that it
has 1/2 the width and height, reducing the video size.

## Requirements

* Python 3
* OS X
* HandBrakeCLI, installed in `/Applications`

## Install

* Clone this repository.
* Open a terminal and `cd` to this repository's directory.
* `pip3 install -r requirements.txt`
* Add this repository to your `$PATH` variable so that `vidcrush.py` can be run from anywhere.

## Usage

```
vidcrush.py my_video.mp4
```

The original video file will be moved to the trash (or recycle bin)
after the new video file has been successfully encoded.

## Running Tests

There aren't any tests yet but you can run the typechecker using:

```
make
```