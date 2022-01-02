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
# script:      start_mjpeg_native.sh
# description: Starts an MJPEG stream using JPEG frames from the camera (no encoding on the Pi).
#              The selected camera must support JPEG frames nativelly.
#              In practice, it is often better to encode frames on the Pi. Cameras tend to support 
#              JPEG frames to allow higher framerates between camera and computer, but there is not 
#              much control over compression level. As such, the bandwidth is often higher than 
#              desired for streaming
# author:      Marcus Behel
# date:        1-2-2022
# version:     v1.0.0
####################################################################################################

DIR=$(realpath $(dirname $0))

source "$DIR"/config.sh

gst-launch-1.0 v4l2src device=${VIDEO_DEVICE} io-mode=$V4L2_IOMODE ! \
    image/jpeg,width=${VIDEO_WIDTH},height=${VIDEO_HEIGHT},framerate=${VIDEO_FRAMERATE}/1 ! \
    multipartmux ! $SINK

exit $?