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
# script:      playstream.py
# description: Starts a stream using the Pi camera using the newer camera stack (libcamera).
#              The system must be configured for the new camera stack (if using buster or older).
# author:      Marcus Behel
# date:        1-2-2022
# version:     v1.0.0
####################################################################################################

import argparse
import os
import shutil


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Plays a camera stream over the network. Supports any type of stream started with the camstream script.")
        parser.add_argument("--netmode", type=str, choices=["tcp", "udp", "rtsp"], default="tcp", help="Which network mode the stream is using (tcp, udp, or rtsp). Default = tcp")
        parser.add_argument("--address", type=str, default="auto", help="For TCP or RTSP, address of the server. For UDP address the server is sending data to (generally localhost or 127.0.0.1). Default = 192.168.10.1 for TCP / RTSP, 127.0.0.1 for UDP")
        parser.add_argument("--port", type=int, default=0, help="Port for TCP server or RTSP server or port UDP data is being sent to. Default = 5008 for TCP or UDP, 8554 for RTSP")
        parser.add_argument("--rtspkey", type=str, default="stream", help="Path on rtsp server the stream to play is located at. Ignored for tcp and udp modes. Default = stream")
        parser.add_argument("--format", type=str, choices=["auto", "h264", "mjpeg"], default="auto", help="Format of the stream (either h264 of mjpeg). By default, this will be left unconfigured and the player will attempt to auto detect the format.")
        parser.add_argument("--player", type=str, choices=["auto", "ffplay", "mpv", "mplayer"], default="auto", help="Which player to play the stream with (ffplay, mpv, or mplayer). By default, the first located player will be used.")
        parser.add_argument("--framerate", type=int, default=60, help="Framerate for playback. Recommended to use twice the framerate of the stream to ensure newest frame is always displayed.")
        res = parser.parse_args()

        if res.address == "auto":
            if res.netmode == "udp":
                res.address = "127.0.0.1"
            else:
                res.address = "192.168.10.1"
        
        if res.port == 0:
            if res.netmode == "rtsp":
                res.port = 8554
            else:
                res.port = 5008

        if res.netmode == "tcp":
            url = "tcp://{0}:{1}".format(res.address, res.port)
        elif res.netmode == "udp":
            url = "udp://{0}:{1}".format(res.address, res.port)
        elif res.netmode == "rtsp":
            url = "rtsp://{0}:{1}/{2}".format(res.address, res.port, res.rtspkey)
        else:
            print("ERROR: Unknown netmode.")
            exit(1)

        if res.player == "auto":
            if shutil.which("ffplay") is not None:
                res.player = "ffplay"
            elif shutil.which("mpv") is not None:
                res.player = "mpv"
            elif shutil.which("mplayer") is not None:
                res.player = "mplayer"
            else:
                print("ERROR: No player found. Install either ffplay, mpv, or mplayer and make sure it is in your PATH.")
                exit(1)

        if res.player == "ffplay":
            if not shutil.which("ffplay"):
                print("ERROR: ffplay not found. Install ffmpeg and ensure ffplay is in your PATH.")
                exit(1)
            
            if res.netmode != "rtsp":
                cmd = "ffplay -probesize 32 -framerate {fps} -fflags nobuffer -flags low_delay -framedrop -sync ext {url}".format(fps=res.framerate, url=url)
            else:
                # Cannot use -framerate with rtsp
                cmd = "ffplay -probesize 32 -fflags nobuffer -flags low_delay -framedrop -sync ext {url}".format(url=url)
                    
        if res.player == "mpv":
            if not shutil.which("mpv"):
                print("ERROR: mpv not found. Install mpv and ensure it is in your PATH.")
                exit(1)
            
            # MPV cannot reliably detect MJPEG and rejects the stream by default
            # Using --demuxer-lavf-probescore=10 fixes this
            if res.format == "h264":
                extra = ""
            else:
                extra = "--demuxer-lavf-probescore=10"

            cmd = "mpv --no-cache --untimed --profile=low-latency --no-correct-pts --fps={fps} --osc=no {extra} {url}".format(fps=res.framerate, url=url, extra=extra)
        
        if res.player == "mplayer":
            if not shutil.which("mplayer"):
                print("ERROR: mplayer not found. Install mplayer and ensure it is in your PATH.")
                exit(1)
            if url.startswith("tcp") or url.startswith("udp"):
                url = "ffmpeg://{0}".format(url)
            
            if res.format == "auto":
                print("ERROR: mplayer cannot auto detect format. Specify a format using --format")
                exit(1)
            elif res.format == "mjpeg":
                cmd = "mplayer -benchmark -nocache -fps {fps} -demuxer lavf {url}".format(fps=res.framerate, url=url)
            elif res.format == "h264":
                cmd = "mplayer -benchmark -nocache -fps {fps} -demuxer h264es {url}".format(fps=res.framerate, url=url)
            else:
                print("ERROR: Unknown format specified.")
                exit(1)

        print(cmd)
        os.system(cmd)

    except KeyboardInterrupt:
        exit(2)

