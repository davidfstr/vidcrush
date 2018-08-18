#!/usr/bin/env python3

import argparse
import os
import os.path
import re
from send2trash import send2trash  # type: ignore  # mypy can't find it
import subprocess
import sys
import tempfile
from typing import Any, Dict, List, Optional, Tuple


def main() -> None:
    parser = argparse.ArgumentParser(description=
        'Reencode video files at a smaller size.')
    parser.add_argument(
        '-s', '--scale', dest='scale', type=float, default=0.5,
        help='fraction to multiply the original video dimensions by')
    parser.add_argument(
        '-r', '--replace', dest='replace', action='store_true',
        help='replaces the original video file')
    parser.add_argument('video_filepaths', nargs='+')
    args = parser.parse_args()
    video_filepaths = args.video_filepaths  # type: List[str]
    scale = args.scale                      # type: float
    
    for video_filepath in video_filepaths:
        if not os.path.isfile(video_filepath):
            sys.exit('file not found: ' + video_filepath)
            return
    
    hb = find_handbrake()
    if hb is None:
        sys.exit('could not find HandBrakeCLI')
        return
    
    if len(video_filepaths) == 1:
        crush(hb, video_filepath, scale, replace=args.replace, quiet=False)
    else:
        for video_filepath in video_filepaths:
            print(video_filepath)
            crush(hb, video_filepath, scale, replace=args.replace, quiet=True)


Handbrake = str  # filepath to Handbrake binary

def find_handbrake() -> Optional[Handbrake]:
    for (dirpath, dirnames, filenames) in os.walk('/Applications'):
        dirnames[:] = reversed(sorted(
            [dn for dn in dirnames if dn.startswith('HandBrake')]))
        if 'HandBrakeCLI' in filenames:
            return os.path.join(dirpath, 'HandBrakeCLI')
    return None  # not found


def crush(hb: Handbrake, old_video_filepath: str, scale: float, *, replace: bool, quiet: bool) -> None:
    width_height = get_video_size(hb, old_video_filepath)
    if width_height is None:
        sys.exit('not a video file: ' + old_video_filepath)
        return
    (width, height) = width_height
    
    # Calculate new video filepath
    NEW_VIDEO_FILENAME_SUFFIX = '-%s' % scale
    prefix, dot, suffix = old_video_filepath.rpartition('.')
    if prefix == '':
        suffix += NEW_VIDEO_FILENAME_SUFFIX
    else:
        prefix += NEW_VIDEO_FILENAME_SUFFIX
    new_video_filepath = prefix + dot + suffix

    old_video_fileext = os.path.splitext(old_video_filepath)[1]
    with tempfile.NamedTemporaryFile(
            suffix=old_video_fileext,
            delete=False) as new_video_file:
        reencode_video_to_size(
            hb,
            old_video_filepath,
            new_video_file.name,
            (int(width * scale), int(height * scale)),
            quiet)
        if replace:
            move_to_trash(old_video_filepath)
            os.rename(new_video_file.name, old_video_filepath)
        else:
            os.rename(new_video_file.name, new_video_filepath)


def get_video_size(hb: Handbrake, video_filepath: str) -> Optional[Tuple[int, int]]:
    output_bytes = subprocess.check_output(
        [hb, '--scan', '-i', video_filepath],
        stderr=subprocess.STDOUT)
    output = output_bytes.decode('utf-8')
    
    m = re.search(r'\n  \+ size: ([0-9]+)x([0-9]+),', output)
    if not m:
        return None
    (width_str, height_str) = m.groups()
    (width, height) = (int(width_str), int(height_str))
    return (width, height)


def reencode_video_to_size(
        hb: Handbrake,
        old_video_filepath: str,
        new_video_filepath: str,
        size: Tuple[int, int],
        quiet: bool) -> None:
    (width, height) = size
    extra_kwargs = dict(
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    ) if quiet else {}  # type: Dict[str, Any]
    subprocess.check_call([
        hb,
        '-i', old_video_filepath,
        '-o', new_video_filepath,
        '-w', str(width),
        '-l', str(height),
        '--preset', 'Normal',
    ], **extra_kwargs)


def move_to_trash(filepath: str) -> None:
    send2trash(filepath)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
