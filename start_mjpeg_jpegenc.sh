#!/usr/bin/env bash
####################################################################################################
#
# Copyright 2022 Marcus Behel
#
# This file is part of ArPiRobot-ImageScripts.
# 
# ArPiRobot-ImageScripts is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# ArPiRobot-ImageScripts is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with ArPiRobot-ImageScripts.  If not, see <https://www.gnu.org/licenses/>.
####################################################################################################
# script:      start_mjpeg_jpegenc.sh
# description: Starts an MJPEG stream using raw frames from the camera. Frames are encoded to JPEG
#              images on the Pi allowing for control of the quality.
# author:      Marcus Behel
# date:        1-2-2022
# version:     v1.0.0
####################################################################################################

# 1-100: 100 = best quality, 1 = smallest size
QUALITY=60

DIR=$(realpath $(dirname $0))

source "$DIR"/config.sh

gst-launch-1.0 v4l2src device=${VIDEO_DEVICE} io-mode=$V4L2_IOMODE ! \
    video/x-raw,width=${VIDEO_WIDTH},height=${VIDEO_HEIGHT},framerate=${VIDEO_FRAMERATE}/1 ! \
    jpegenc quality=$QUALITY ! multipartmux ! $SINK

exit $?