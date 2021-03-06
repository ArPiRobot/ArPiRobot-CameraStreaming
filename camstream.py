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
# script:      camstream.py
# description: Starts a stream using a camera connected to a raspberry pi. Capable of using many 
#              camera stacks compatible with both Pi camera modules and USB webcams.
#              Supports many options to configure the stream. Designed for 
#              low latency / real-time streams
#              The system must be configured for the new camera stack (if using buster or older).
# author:      Marcus Behel
# date:        2-4-2022
# version:     v1.0.1
####################################################################################################

import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Starts a stream using the Pi camera using the newer camera stack (libcamera). The system must be configured for the new camera stack (if using buster or older).")
    parser.add_argument("--driver", type=str, choices=["libcamera", "raspicam", "v4l2"], default="libcamera", help="Which input device driver to use. V4L2 supports USB cameras. Libcamera and raspicam only support the pi camera modules (libcamera being the new stack). Default = libcamera")
    parser.add_argument("--device", type=str, default="", help="Device identifier for which camera to use (does not apply to libcamera or raspicam).")
    parser.add_argument("--iomode", metavar="IOMODE", type=str, default="auto", choices=["auto", "rw", "mmap", "userptr", "dmabuf", "dmabuf-import"], help="IO mode for v4l2 devices. If latency issues exist with USB webcam try using dmabuf. Default = auto")
    parser.add_argument("--h264encoder", metavar="ENCODER", type=str, choices=["libav-omx", "omx", "libx264"], default="libav-omx", help="Which h.264 encoder to use with V4L2 (no effect with libcamera or raspicam drivers) Choices = libav-omx, omx, libx264. Default = libav-omx.")
    parser.add_argument("--width", type=int, default=640, help="Width of the video stream (must be a supported resolution). Default = 640")
    parser.add_argument("--height", type=int, default=480, help="Height of the video stream (must be a supported resolution). Default = 480")
    parser.add_argument("--vconvert", action='store_true', help="Pass input through videoconvert element. Only applies to v4l2 pipeline.")
    parser.add_argument("--framerate", type=int, default=30, help="Video stream framerate (must be supported for the active resolution). Default = 30")
    parser.add_argument("--format", metavar="FORMAT", type=str, choices=["h264", "mjpeg"], default="h264", help="Format for the stream (h264 or mjpeg). Generally, H.264 is lower bandwidth, while MJPEG is lower latency. Default = h264")
    parser.add_argument("--bitrate", type=int, default=2048000, help="Bitrate for H.264 stream (does not apply to MJPEG, unless using raspicam driver). Default = 2048000")
    parser.add_argument("--profile", metavar="PROFILE", type=str, choices=["baseline", "main", "high"], default="baseline", help="Profile for H.264 stream (does not apply to MJPEG) Either baseline, main, or high. Default = baseline")
    parser.add_argument("--quality", metavar="QUALITY", type=int, choices=range(1, 100), default=50, help="JPEG image quality (1-100) for MPEG stream (does not apply to H.264, does not work with raspicam driver). Default = 50")
    parser.add_argument("--vflip", action='store_true', help="Vertically flip the camera image.")
    parser.add_argument("--hflip", action='store_true', help="Vertically flip the camera image.")
    parser.add_argument("--rotate", metavar="ROTATION", type=int, choices=[0, 90, 180, 270], default=0, help="Rotate camera image (0, 90, 180, 270). If using libcamera, only 0 and 180 are supported. Default = 0")
    parser.add_argument("--gain", type=float, default=10.0, help="Configure the gain of the camera. Affects brightness of the images. Default = 10.0")
    parser.add_argument("--netmode", type=str, choices=["tcp", "udp", "rtsp"], default="tcp", help="Chooses which networking protocol to use. TCP runs a server on the Pi that clients connect to and ensures packaet delivery and order. UDP sends frames to the client, but the Pi must know the client's IP address. UDP does not gaurentee packet delivery or order, but can prevent lag with bad quality connections. RTSP uses a server running on the Pi (another program) but is capable of using udp transports.")
    parser.add_argument("--address", type=str, default="0.0.0.0", help="Which IP address to either run the TCP server on or send UDP datagrams to. For RTSP this is the address of the RTSP server.")
    parser.add_argument("--port", type=int, default=5008, help="Which port to use for TCP server or which port to send UDP datagrams to. For RTSP, this is port of RTSP server.")
    parser.add_argument("--rtspkey", type=str, default="stream", help="Only applies to RTSP net mode. This is the key of the stream (name after server's URL).")
    res = parser.parse_args()
    
    if res.driver == "libcamera":
        # Use libcamera to capture frames from the camera (more optimized for the pi camera than v4l2)
        # Then use gstreamer to create a tcp server
        # libcamera-vid does support a tcp server, however it exists after the first client disconnects
        # The libcamerasrc gstreamer plugin could be used, but does not appear to support the options libcamera-vid does
        cmd = "libcamera-vid -t 0 --inline --width {width} --height {height} --framerate {framerate} " \
                "--codec {format} --bitrate {bitrate} --profile {profile} --quality {quality} " \
                " {vflip} {hflip} --rotation {rotate} --gain {gain} -n -o - | " \
                "gst-launch-1.0 --no-fault fdsrc fd=0".format(
                    width=res.width, height=res.height, framerate=res.framerate, format=res.format, 
                    bitrate=res.bitrate, profile=res.profile, quality=res.quality, 
                    rotate=res.rotate, vflip=("--vflip" if res.vflip else ""), hflip=("--hflip" if res.hflip else ""),
                    gain=res.gain)
    elif res.driver == "raspicam":
        # Use raspicam (old stack) to capture frames from the camera (more optimized for the pi camera than v4l2)
        # Then use gstreamer to create a tcp server
        # raspivid does support a tcp server, however it exists after the first client disconnects
        # The raspicamsrc gstreamer plugin could be used, but does not appear to be easily installed on buster

        # Gain is two controls with raspivid: analog and digital
        # Maximum analog gain (experimentally) seems to be 15
        # Use analog gain as much as possible. Use digital gain when required gain is too large for analog alone
        analog_gain = min(res.gain, 15.0)
        digital_gain = res.gain / analog_gain

        cmd = "raspivid -t 0 --inline --width {width} --height {height} --framerate {framerate} " \
                "--codec {format} --bitrate {bitrate} --profile {profile} " \
                " {vflip} {hflip} --rotation {rotate} --drc off --digitalgain {dg} --analoggain {ag} -n -o - | " \
                "gst-launch-1.0 --no-fault fdsrc fd=0".format(
                    width=res.width, height=res.height, framerate=res.framerate, format=res.format.upper(), 
                    bitrate=res.bitrate, profile=res.profile, 
                    rotate=res.rotate, vflip=("--vflip" if res.vflip else ""), hflip=("--hflip" if res.hflip else ""),
                    dg=digital_gain, ag=analog_gain)
    elif res.driver == "v4l2":
        # Gain is two controls with raspivid: analog and digital
        # Maximum analog gain (experimentally) seems to be 15
        # Use analog gain as much as possible. Use digital gain when required gain is too large for analog alone
        analog_gain = min(res.gain, 15.0)
        digital_gain = res.gain / analog_gain

        # Apply settings using v4l2-ctl
        # Some cameras may not support all settings
        # Note: When using new camera stack (libcamera) Pi camera will not work properly via v4l2
        os.system("v4l2-ctl -d {0} --set-ctrl=rotate={1}".format(res.device, res.rotate))
        os.system("v4l2-ctl -d {0} --set-ctrl=horizontal_flip={1}".format(res.device, 1 if res.hflip else 0))
        os.system("v4l2-ctl -d {0} --set-ctrl=vertical_flip={1}".format(res.device, 1 if res.vflip else 0))

        # Sometimes gain is split into two, other times it is one control. Sometimes it is not supported
        os.system("v4l2-ctl -d {0} --set-ctrl=analogue_gain={1}".format(res.device, analog_gain))
        os.system("v4l2-ctl -d {0} --set-ctrl=digital_gain={1}".format(res.device, digital_gain))
        os.system("v4l2-ctl -d {0} --set-ctrl=gain={1}".format(res.device, res.gain))
                

        if res.format == "mjpeg":
            enc = "jpegenc quality={0}".format(res.quality)
        elif res.format == "h264":
            if res.h264encoder == "libx264":
                enc = "x264enc tune=zerolatency speed-preset=ultrafast bitrate={0} ! video/x-h264,profile={1} ! h264parse config_interval=-1 ! video/x-h264,stream-format=byte-stream,alignment=au".format(int(res.bitrate / 1000.0), res.profile)
            elif res.h264encoder == "libav-omx":
                # Libav using HW accelerated OMX encoder.
                # Originally included because of issues setting bitrate with omxh264enc
                # Now included because it may be easier to get working in raspios bullseye
                enc = "avenc_h264_omx bitrate={0} profile={1} ! h264parse config-interval=-1".format(res.bitrate, res.profile)
            elif res.h264encoder == "omx":
                # Using omxh264enc
                # May not be easily available in raspios bullseye
                enc = "omxh264enc target-bitrate={0} control-rate=variable ! video/x-h264,profile={1} ! h264parse config-interval=-1".format(res.bitrate, res.profile)

        cmd = "gst-launch-1.0 --no-fault v4l2src device={device} io-mode={iomode} ! " \
                "video/x-raw,width={width},height={height},framerate={framerate}/1 ! {vconvert} ! " \
                "{enc}".format(device=res.device, iomode=res.iomode, 
                    width=res.width, height=res.height, framerate=res.framerate, enc=enc, 
                    vconvert= "videoconvert" if res.vconvert else "identity")

    if res.netmode == "tcp":
        cmd = "{cmd} ! tcpserversink host={address} port={port}".format(cmd=cmd, address=res.address, port=res.port)
    elif res.netmode == "udp":
        cmd = "{cmd} ! udpsink host={address} port={port}".format(cmd=cmd, address=res.address, port=res.port)
    elif res.netmode == "rtsp":
        if res.format == "h264":
            parser = "h264parse"
        elif res.format == "mjpeg":
            parser = "jpegparse"
        cmd = "{cmd} ! {parser} ! rtspclientsink name=s location=rtsp://{address}:{port}/{rtsp_key}".format(
            cmd=cmd, address=res.address, port=res.port, rtsp_key=res.rtspkey, parser=parser)

    print(cmd)
    os.system(cmd)
