#!/usr/bin/env python3
####################################################################################################
#
# Copyright 2022 Marcus Behel
#
# This file is part of ArPiRobot-CameraStreaming.
# 
# ArPiRobot-CameraStreaming is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# ArPiRobot-CameraStreaming is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with ArPiRobot-CameraStreaming.  If not, see <https://www.gnu.org/licenses/>.
####################################################################################################
# script:      stream_libcamera.py
# description: Starts a stream using the Pi camera using the newer camera stack (libcamera).
#              The system must be configured for the new camera stack (if using buster or older).
# author:      Marcus Behel
# date:        1-2-2022
# version:     v1.0.0
####################################################################################################

import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Starts a stream using the Pi camera using the newer camera stack (libcamera). The system must be configured for the new camera stack (if using buster or older).")
    parser.add_argument("--driver", type=str, choices=["libcamera", "raspicam"], default="libcamera", help="Which input device driver to use. V4L2 supports USB cameras. Libcamera and raspicam only support the pi camera modules (libcamera being the new stack). Default = libcamera")
    parser.add_argument("--device", type=str, default="", help="Device identifier for which camera to use (does not apply to libcamera or raspicam).")
    parser.add_argument("--width", type=int, default=640, help="Width of the video stream (must be a supported resolution). Default = 640")
    parser.add_argument("--height", type=int, default=480, help="Height of the video stream (must be a supported resolution). Default = 480")
    parser.add_argument("--framerate", type=int, default=30, help="Video stream framerate (must be supported for the active resolution). Default = 30")
    parser.add_argument("--format", metavar="FORMAT", type=str, choices=["h264", "mjpeg"], default="h264", help="Format for the stream (h264 or mjpeg). Generally, H.264 is lower bandwidth, while MJPEG is lower latency. Default = h264")
    parser.add_argument("--bitrate", type=int, default=2048000, help="Bitrate for H.264 stream (does not apply to MJPEG). Default = 2048000")
    parser.add_argument("--profile", metavar="PROFILE", type=str, choices=["baseline", "main", "high"], default="baseline", help="Profile for H.264 stream (does not apply to MJPEG, unless using raspicam driver) Either baseline, main, or high. Default = baseline")
    parser.add_argument("--quality", metavar="QUALITY", type=int, choices=range(1, 100), default=50, help="JPEG image quality (1-100) for MPEG stream (does not apply to H.264, does not work with raspicam driver). Default = 50")
    parser.add_argument("--vflip", action='store_true', help="Vertically flip the camera image.")
    parser.add_argument("--hflip", action='store_true', help="Vertically flip the camera image.")
    parser.add_argument("--rotate", metavar="ROTATION", type=int, choices=[0, 90, 180, 270], default=0, help="Rotate camera image (0, 90, 180, 270). If using libcamera, only 0 and 180 are supported. Default = 0")
    parser.add_argument("--port", type=int, default=5008, help="Which TCP port to use.")
    res = parser.parse_args()
    
    if res.driver == "libcamera":
        # Use libcamera to capture frames from the camera (more optimized for the pi camera than v4l2)
        # Then use gstreamer to create a tcp server
        # libcamera-vid does support a tcp server, however it exists after the first client disconnects
        # The libcamerasrc gstreamer plugin could be used, but does not appear to support the options libcamera-vid does
        cmd = "libcamera-vid -t 0 --inline --width {width} --height {height} --framerate {framerate} " \
                "--codec {format} --bitrate {bitrate} --profile {profile} --quality {quality} " \
                " {vflip} {hflip} --rotation {rotate} -n -o - | " \
                "gst-launch-1.0 fdsrc fd=0 ! tcpserversink host=0.0.0.0 port={port}".format(
                    width=res.width, height=res.height, framerate=res.framerate, format=res.format, 
                    bitrate=res.bitrate, profile=res.profile, quality=res.quality, port=res.port, 
                    rotate=res.rotate, vflip=("--vflip" if res.vflip else ""), hflip=("--hflip" if res.hflip else ""))
    elif res.driver == "raspicam":
        # Use raspicam (old stack) to capture frames from the camera (more optimized for the pi camera than v4l2)
        # Then use gstreamer to create a tcp server
        # raspivid does support a tcp server, however it exists after the first client disconnects
        # The raspicamsrc gstreamer plugin could be used, but does not appear to be easily installed on buster
        cmd = "raspivid -t 0 --inline --width {width} --height {height} --framerate {framerate} " \
                "--codec {format} --bitrate {bitrate} --profile {profile} " \
                " {vflip} {hflip} --rotation {rotate} -n -o - | " \
                "gst-launch-1.0 fdsrc fd=0 ! tcpserversink host=0.0.0.0 port={port}".format(
                    width=res.width, height=res.height, framerate=res.framerate, format=res.format.upper(), 
                    bitrate=res.bitrate, profile=res.profile, port=res.port, 
                    rotate=res.rotate, vflip=("--vflip" if res.vflip else ""), hflip=("--hflip" if res.hflip else ""))
    print(cmd)
    os.system(cmd)
